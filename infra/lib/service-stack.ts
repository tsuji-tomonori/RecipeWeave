import { existsSync } from "node:fs";
import { join } from "node:path";
import {
  CfnOutput,
  CfnParameter,
  Duration,
  RemovalPolicy,
  Stack,
  aws_apigatewayv2 as apigateway,
  aws_apigatewayv2_authorizers as authorizers,
  aws_apigatewayv2_integrations as integrations,
  aws_cloudfront as cloudfront,
  aws_cloudfront_origins as origins,
  aws_iam as iam,
  aws_lambda as lambda,
  aws_logs as logs,
  aws_s3 as s3,
  aws_s3_deployment as deployment,
} from "aws-cdk-lib";
import type { StackProps } from "aws-cdk-lib";
import type { Construct } from "constructs";
import type { DataStack } from "./data-stack.js";

export interface ServiceStackProps extends StackProps {
  readonly data: DataStack;
  readonly repositoryRoot: string;
}

export function assertBuiltAsset(
  directory: string,
  requiredFile: string,
): string {
  if (!existsSync(join(directory, requiredFile))) {
    throw new Error(
      `Build the real deployable asset first: ${join(directory, requiredFile)}`,
    );
  }
  return directory;
}

export class ServiceStack extends Stack {
  public readonly apiFunction: lambda.Function;
  public readonly httpApi: apigateway.HttpApi;
  public readonly distribution: cloudfront.Distribution;
  public readonly migrationRole: iam.Role;

  public constructor(scope: Construct, id: string, props: ServiceStackProps) {
    super(scope, id, props);
    const { data, repositoryRoot } = props;
    const lambdaAsset = assertBuiltAsset(
      join(repositoryRoot, "backend/.build/lambda"),
      "app/handler.py",
    );
    const frontendAsset = assertBuiltAsset(
      join(repositoryRoot, "frontend/dist"),
      "index.html",
    );

    // ビルド成果物は再現可能。スタック間の循環参照を避けるため、静的ファイル用バケットと
    // OACを使う配信ポリシーを同じスタックに置き、スタック削除時もバケットは保持する。
    const webBucket = new s3.Bucket(this, "WebAssets", {
      encryption: s3.BucketEncryption.S3_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      objectOwnership: s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
      enforceSSL: true,
      versioned: true,
      removalPolicy: RemovalPolicy.RETAIN,
      autoDeleteObjects: false,
    });

    const functionLogs = new logs.LogGroup(this, "ApiLogs", {
      retention: logs.RetentionDays.ONE_MONTH,
      removalPolicy: RemovalPolicy.RETAIN,
    });
    this.apiFunction = new lambda.Function(this, "Api", {
      runtime: lambda.Runtime.PYTHON_3_12,
      architecture: lambda.Architecture.X86_64,
      handler: "app.handler.handler",
      code: lambda.Code.fromAsset(lambdaAsset),
      memorySize: 512,
      timeout: Duration.seconds(25),
      reservedConcurrentExecutions: 10,
      logGroup: functionLogs,
      environment: {
        STATE_BACKEND: "dsql",
        DSQL_HOST: data.cluster.attrEndpoint,
        DSQL_DATABASE_USER: "recipeweave_app",
        COGNITO_ISSUER: data.cognitoIssuer,
        COGNITO_CLIENT_ID: data.userPoolClient.userPoolClientId,
      },
    });
    this.apiFunction.addToRolePolicy(
      new iam.PolicyStatement({
        actions: ["dsql:DbConnect"],
        resources: [data.cluster.attrResourceArn],
      }),
    );

    const migrationOperatorArn = new CfnParameter(
      this,
      "MigrationOperatorArn",
      {
        type: "String",
        description:
          "Existing IAM operator role allowed to assume the dedicated DSQL migration role.",
        allowedPattern: "^arn:aws:iam::[0-9]{12}:role/[A-Za-z0-9+=,.@_/-]+$",
      },
    );
    this.migrationRole = new iam.Role(this, "DsqlMigrationRole", {
      assumedBy: new iam.ArnPrincipal(migrationOperatorArn.valueAsString),
      maxSessionDuration: Duration.hours(1),
      description:
        "DSQL schema migrations only; the API runtime cannot assume this role.",
    });
    this.migrationRole.addToPolicy(
      new iam.PolicyStatement({
        actions: ["dsql:DbConnectAdmin"],
        resources: [data.cluster.attrResourceArn],
      }),
    );

    this.httpApi = new apigateway.HttpApi(this, "HttpApi", {
      apiName: `${this.stackName}-api`,
      description:
        "RecipeWeave sample catalog and authenticated per-user state.",
      createDefaultStage: false,
    });
    const accessLogs = new logs.LogGroup(this, "HttpAccessLogs", {
      retention: logs.RetentionDays.ONE_MONTH,
      removalPolicy: RemovalPolicy.RETAIN,
    });
    new apigateway.CfnStage(this, "ApiStage", {
      apiId: this.httpApi.httpApiId,
      stageName: "$default",
      autoDeploy: true,
      defaultRouteSettings: {
        throttlingBurstLimit: 30,
        throttlingRateLimit: 10,
      },
      accessLogSettings: {
        destinationArn: accessLogs.logGroupArn,
        format: JSON.stringify({
          requestId: "$context.requestId",
          routeKey: "$context.routeKey",
          status: "$context.status",
          responseLength: "$context.responseLength",
          integrationLatency: "$context.integrationLatency",
        }),
      },
    });

    const integration = new integrations.HttpLambdaIntegration(
      "FastApi",
      this.apiFunction,
    );
    for (const path of [
      "/api/health",
      "/api/foods",
      "/api/recipes",
      "/api/recipes/{id}",
    ]) {
      this.httpApi.addRoutes({
        path,
        methods: [apigateway.HttpMethod.GET],
        integration,
      });
    }
    const jwtAuthorizer = new authorizers.HttpJwtAuthorizer(
      "CognitoAccessToken",
      data.cognitoIssuer,
      {
        jwtAudience: [data.userPoolClient.userPoolClientId],
      },
    );
    this.httpApi.addRoutes({
      path: "/api/state",
      methods: [apigateway.HttpMethod.GET, apigateway.HttpMethod.PUT],
      integration,
      authorizer: jwtAuthorizer,
      authorizationScopes: ["aws.cognito.signin.user.admin"],
    });

    const catalogCache = new cloudfront.CachePolicy(this, "CatalogCache", {
      minTtl: Duration.seconds(0),
      defaultTtl: Duration.seconds(30),
      maxTtl: Duration.seconds(60),
      queryStringBehavior: cloudfront.CacheQueryStringBehavior.all(),
      cookieBehavior: cloudfront.CacheCookieBehavior.none(),
      headerBehavior: cloudfront.CacheHeaderBehavior.none(),
      enableAcceptEncodingGzip: true,
      enableAcceptEncodingBrotli: true,
    });
    const staticCache = new cloudfront.CachePolicy(this, "StaticCache", {
      minTtl: Duration.seconds(0),
      defaultTtl: Duration.minutes(5),
      maxTtl: Duration.days(1),
      enableAcceptEncodingGzip: true,
      enableAcceptEncodingBrotli: true,
    });
    const apiOrigin = new origins.HttpOrigin(
      `${this.httpApi.httpApiId}.execute-api.${this.region}.${this.urlSuffix}`,
      {
        protocolPolicy: cloudfront.OriginProtocolPolicy.HTTPS_ONLY,
        readTimeout: Duration.seconds(30),
      },
    );
    const apiBase = {
      origin: apiOrigin,
      viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.HTTPS_ONLY,
      responseHeadersPolicy: cloudfront.ResponseHeadersPolicy.SECURITY_HEADERS,
      compress: true,
    };
    this.distribution = new cloudfront.Distribution(this, "Web", {
      defaultRootObject: "index.html",
      // エラーレスポンスには独立した最小TTLがあるため、0にする。
      // ステータスコードは変更せず、APIの失敗を代替HTMLへ置き換えない。
      errorResponses: [400, 403, 404, 405, 414, 500, 501, 502, 503, 504].map(
        (httpStatus) => ({ httpStatus, ttl: Duration.seconds(0) }),
      ),
      defaultBehavior: {
        origin: origins.S3BucketOrigin.withOriginAccessControl(webBucket),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        cachePolicy: staticCache,
        responseHeadersPolicy:
          cloudfront.ResponseHeadersPolicy.SECURITY_HEADERS,
        compress: true,
      },
      additionalBehaviors: {
        "/api/foods": { ...apiBase, cachePolicy: catalogCache },
        "/api/recipes": { ...apiBase, cachePolicy: catalogCache },
        "/api/recipes/*": { ...apiBase, cachePolicy: catalogCache },
        "/api/*": {
          ...apiBase,
          allowedMethods: cloudfront.AllowedMethods.ALLOW_ALL,
          cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED,
          // Authorizationを転送し、閲覧側のHostヘッダーはAPI配信元のホストに置き換える。
          // 利用者固有の状態は共有キャッシュに保存しない。
          originRequestPolicy:
            cloudfront.OriginRequestPolicy.ALL_VIEWER_EXCEPT_HOST_HEADER,
        },
      },
    });
    new deployment.BucketDeployment(this, "DeployWeb", {
      sources: [deployment.Source.asset(frontendAsset)],
      destinationBucket: webBucket,
      distribution: this.distribution,
      distributionPaths: ["/*"],
      cacheControl: [deployment.CacheControl.maxAge(Duration.minutes(5))],
      prune: false,
      retainOnDelete: true,
      logGroup: new logs.LogGroup(this, "WebDeploymentLogs", {
        retention: logs.RetentionDays.ONE_MONTH,
        removalPolicy: RemovalPolicy.RETAIN,
      }),
    });

    new CfnOutput(this, "WebUrl", {
      value: `https://${this.distribution.distributionDomainName}`,
    });
    new CfnOutput(this, "ApiUrl", { value: this.httpApi.apiEndpoint });
    const apiRole = this.apiFunction.role;
    if (apiRole === undefined)
      throw new Error("The API requires an execution role");
    new CfnOutput(this, "DsqlAppIamArn", { value: apiRole.roleArn });
    new CfnOutput(this, "DsqlMigrationIamArn", {
      value: this.migrationRole.roleArn,
    });
    new CfnOutput(this, "WebBucketName", { value: webBucket.bucketName });
  }
}
