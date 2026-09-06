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

test("全APIをFastAPIの認証・所有権判定へ転送し本番local認証を許可しない", () => {
  template.resourceCountIs("AWS::ApiGatewayV2::Route", 1);
  template.hasResourceProperties("AWS::ApiGatewayV2::Route", {
    RouteKey: "ANY /api/{proxy+}",
  });
  template.hasResourceProperties("AWS::Lambda::Function", {
    Handler: "app.handler.handler",
    Environment: {
      Variables: Match.objectLike({
        AUTH_MODE: "cognito",
        ENVIRONMENT: "production",
        DATABASE_SSLMODE: "require",
      }),
    },
  });
  dataTemplate.hasResourceProperties("AWS::Cognito::UserPoolClient", {
    GenerateSecret: false,
    EnableTokenRevocation: true,
    AllowedOAuthFlows: ["code"],
    AllowedOAuthFlowsUserPoolClient: true,
    AllowedOAuthScopes: ["openid", "email", "profile"],
    CallbackURLs: Match.anyValue(),
    LogoutURLs: Match.anyValue(),
  });
});

test("never caches private state and forwards Authorization without the viewer Host", () => {
  template.hasResourceProperties("AWS::CloudFront::Distribution", {
    DistributionConfig: Match.objectLike({
      CacheBehaviors: Match.arrayWith([
        Match.objectLike({
          PathPattern: "/api/*",
          // AWS管理のCachingDisabledでは、最小・既定・最大TTLがすべて0になる。
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
});

test("API実行と管理者移行を別Lambda・別secret権限に分離する", () => {
  template.hasResourceProperties("AWS::Lambda::Function", {
    Handler: "app.handler.handler",
    Runtime: "python3.12",
    ReservedConcurrentExecutions: 10,
    VpcConfig: Match.objectLike({
      SecurityGroupIds: Match.anyValue(),
      SubnetIds: Match.anyValue(),
    }),
  });
  template.hasResourceProperties("AWS::Lambda::Function", {
    Handler: "app.integrations.database.migration_handler.handler",
    ReservedConcurrentExecutions: 1,
    Timeout: 900,
  });
  const policies = template.findResources("AWS::IAM::Policy");
  const apiPolicies = Object.values(policies).filter((value) =>
    JSON.stringify(value.Properties.Roles).includes("ApiServiceRole"),
  );
  if (apiPolicies.length !== 1)
    throw new Error("APIの権限が一つに定まりません");
  const statements = apiPolicies[0]?.Properties.PolicyDocument.Statement as {
    Action: string | string[];
    Resource: unknown;
  }[];
  const secretStatements = statements.filter((value) =>
    JSON.stringify(value.Action).includes("secretsmanager:GetSecretValue"),
  );
  if (
    secretStatements.length !== 1 ||
    JSON.stringify(secretStatements).includes("RelationalClusterSecret")
  )
    throw new Error("APIにDB管理者secretへの権限があります");
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
