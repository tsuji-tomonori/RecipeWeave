import { fileURLToPath } from "node:url";
import { test } from "node:test";
import { App } from "aws-cdk-lib";
import { Match, Template } from "aws-cdk-lib/assertions";
import { DataStack } from "../lib/data-stack.js";
import { ServiceStack } from "../lib/service-stack.js";

const env = { account: "111122223333", region: "us-east-1" };
const app = new App();
const data = new DataStack(app, "TestData", { env });
const service = new ServiceStack(app, "TestService", {
  env,
  data,
  repositoryRoot: fileURLToPath(new URL("../../", import.meta.url)),
});
const dataTemplate = Template.fromStack(data);
const template = Template.fromStack(service);

test("prohibits public static storage and restricts reads to its OAC distribution", () => {
  template.hasResource("AWS::S3::Bucket", {
    Properties: Match.objectLike({
      BucketEncryption: {
        ServerSideEncryptionConfiguration: [
          { ServerSideEncryptionByDefault: { SSEAlgorithm: "AES256" } },
        ],
      },
      PublicAccessBlockConfiguration: {
        BlockPublicAcls: true,
        BlockPublicPolicy: true,
        IgnorePublicAcls: true,
        RestrictPublicBuckets: true,
      },
      VersioningConfiguration: { Status: "Enabled" },
    }),
    DeletionPolicy: "Retain",
  });
  template.hasResourceProperties("AWS::CloudFront::OriginAccessControl", {
    OriginAccessControlConfig: Match.objectLike({
      OriginAccessControlOriginType: "s3",
      SigningBehavior: "always",
      SigningProtocol: "sigv4",
    }),
  });
  template.hasResourceProperties("AWS::S3::BucketPolicy", {
    PolicyDocument: {
      Statement: Match.arrayWith([
        Match.objectLike({
          Principal: { Service: "cloudfront.amazonaws.com" },
          Action: "s3:GetObject",
          Condition: { StringEquals: { "AWS:SourceArn": Match.anyValue() } },
        }),
      ]),
      Version: "2012-10-17",
    },
  });
});

test("requires Cognito access-token scope on both private state methods", () => {
  template.resourceCountIs("AWS::ApiGatewayV2::Route", 6);
  for (const method of ["GET", "PUT"]) {
    template.hasResourceProperties("AWS::ApiGatewayV2::Route", {
      RouteKey: `${method} /api/state`,
      AuthorizationType: "JWT",
      AuthorizerId: Match.anyValue(),
      AuthorizationScopes: ["aws.cognito.signin.user.admin"],
    });
  }
  for (const path of [
    "/api/health",
    "/api/foods",
    "/api/recipes",
    "/api/recipes/{id}",
  ]) {
    template.hasResourceProperties("AWS::ApiGatewayV2::Route", {
      RouteKey: `GET ${path}`,
      AuthorizationType: "NONE",
    });
  }
  dataTemplate.hasResourceProperties("AWS::Cognito::UserPoolClient", {
    GenerateSecret: false,
    EnableTokenRevocation: true,
    ExplicitAuthFlows: ["ALLOW_USER_SRP_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"],
  });
  template.hasResourceProperties("AWS::ApiGatewayV2::Authorizer", {
    AuthorizerType: "JWT",
    IdentitySource: ["$request.header.Authorization"],
    JwtConfiguration: { Audience: Match.anyValue(), Issuer: Match.anyValue() },
  });
});

test("never caches private state and forwards Authorization without the viewer Host", () => {
  template.hasResourceProperties("AWS::CloudFront::Distribution", {
    DistributionConfig: Match.objectLike({
      CacheBehaviors: Match.arrayWith([
        Match.objectLike({
          PathPattern: "/api/*",
          // AWS managed CachingDisabled: minimum/default/maximum TTL are all 0.
          // https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-managed-cache-policies.html#managed-cache-policy-caching-disabled
          CachePolicyId: "4135ea2d-6df8-44a3-9df3-4b5a84be39ad",
          OriginRequestPolicyId: "b689b0a8-53d0-40ab-baf2-68738e2966ac",
          AllowedMethods: [
            "GET",
            "HEAD",
            "OPTIONS",
            "PUT",
            "PATCH",
            "POST",
            "DELETE",
          ],
          ViewerProtocolPolicy: "https-only",
        }),
      ]),
      CustomErrorResponses: [
        400, 403, 404, 405, 414, 500, 501, 502, 503, 504,
      ].map((ErrorCode) => ({ ErrorCode, ErrorCachingMinTTL: 0 })),
    }),
  });
  template.hasResourceProperties("AWS::CloudFront::CachePolicy", {
    CachePolicyConfig: Match.objectLike({
      MinTTL: 0,
      DefaultTTL: 30,
      MaxTTL: 60,
      ParametersInCacheKeyAndForwardedToOrigin: Match.objectLike({
        QueryStringsConfig: { QueryStringBehavior: "all" },
        CookiesConfig: { CookieBehavior: "none" },
        HeadersConfig: { HeaderBehavior: "none" },
      }),
    }),
  });
});

test("separates cluster-scoped runtime access from migration administration", () => {
  template.hasResourceProperties("AWS::IAM::Policy", {
    PolicyDocument: Match.objectLike({
      Statement: Match.arrayWith([
        {
          Action: "dsql:DbConnect",
          Effect: "Allow",
          Resource: { "Fn::ImportValue": Match.anyValue() },
        },
      ]),
    }),
    Roles: [{ Ref: Match.stringLikeRegexp("ApiServiceRole.*") }],
  });
  template.hasResourceProperties("AWS::IAM::Policy", {
    PolicyDocument: {
      Version: "2012-10-17",
      Statement: [
        {
          Action: "dsql:DbConnectAdmin",
          Effect: "Allow",
          Resource: { "Fn::ImportValue": Match.anyValue() },
        },
      ],
    },
    Roles: [{ Ref: Match.stringLikeRegexp("DsqlMigrationRole.*") }],
  });
  template.hasResourceProperties("AWS::IAM::Role", {
    AssumeRolePolicyDocument: {
      Version: "2012-10-17",
      Statement: [
        {
          Action: "sts:AssumeRole",
          Effect: "Allow",
          Principal: { AWS: { Ref: "MigrationOperatorArn" } },
        },
      ],
    },
    Description:
      "DSQL schema migrations only; the API runtime cannot assume this role.",
  });
  template.hasResourceProperties("AWS::Lambda::Function", {
    Handler: "app.handler.handler",
    Runtime: "python3.12",
    Architectures: ["x86_64"],
    Environment: {
      Variables: Match.objectLike({
        STATE_BACKEND: "dsql",
        DSQL_DATABASE_USER: "recipeweave_app",
      }),
    },
    ReservedConcurrentExecutions: 10,
  });
});

test("limits API load and avoids identity, tokens, images and request bodies in access logs", () => {
  template.hasResourceProperties("AWS::ApiGatewayV2::Stage", {
    DefaultRouteSettings: { ThrottlingBurstLimit: 30, ThrottlingRateLimit: 10 },
    AccessLogSettings: Match.objectLike({
      Format: JSON.stringify({
        requestId: "$context.requestId",
        routeKey: "$context.routeKey",
        status: "$context.status",
        responseLength: "$context.responseLength",
        integrationLatency: "$context.integrationLatency",
      }),
    }),
  });
  template.allResourcesProperties("AWS::Logs::LogGroup", {
    RetentionInDays: 30,
  });
});
