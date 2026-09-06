import {
  CfnOutput,
  Duration,
  RemovalPolicy,
  Stack,
  aws_cognito as cognito,
  aws_ec2 as ec2,
  aws_rds as rds,
  aws_secretsmanager as secretsmanager,
} from "aws-cdk-lib";
import type { StackProps } from "aws-cdk-lib";
import type { Construct } from "constructs";

/** 状態を保持するリソースは独立したライフサイクルで管理し、自動削除しない。 */
export class DataStack extends Stack {
  public readonly cluster: rds.DatabaseCluster;
  public readonly vpc: ec2.Vpc;
  public readonly clientSecurityGroup: ec2.SecurityGroup;
  public readonly applicationSecret: secretsmanager.Secret;
  public readonly userPool: cognito.UserPool;
  public readonly userPoolClient: cognito.UserPoolClient;
  public readonly cognitoIssuer: string;

  public constructor(scope: Construct, id: string, props: StackProps) {
    super(scope, id, { ...props, terminationProtection: true });

    // PL/pgSQL、遅延制約、RLSを実DBで実行するためAurora PostgreSQLを使う。
    this.vpc = new ec2.Vpc(this, "DatabaseVpc", {
      maxAzs: 2,
      natGateways: 1,
      subnetConfiguration: [
        { name: "Public", subnetType: ec2.SubnetType.PUBLIC },
        { name: "Application", subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
        { name: "Database", subnetType: ec2.SubnetType.PRIVATE_ISOLATED },
      ],
    });
    this.clientSecurityGroup = new ec2.SecurityGroup(this, "DatabaseClients", {
      vpc: this.vpc,
      description: "APIと移行関数のDB接続元",
      allowAllOutbound: true,
    });
    this.cluster = new rds.DatabaseCluster(this, "RelationalCluster", {
      engine: rds.DatabaseClusterEngine.auroraPostgres({
        version: rds.AuroraPostgresEngineVersion.VER_16_6,
      }),
      credentials: rds.Credentials.fromGeneratedSecret("recipeweave_owner"),
      defaultDatabaseName: "recipeweave",
      writer: rds.ClusterInstance.serverlessV2("Writer", {
        publiclyAccessible: false,
      }),
      readers: [
        rds.ClusterInstance.serverlessV2("Reader", {
          publiclyAccessible: false,
          scaleWithWriter: true,
        }),
      ],
      serverlessV2MinCapacity: 0.5,
      serverlessV2MaxCapacity: 8,
      vpc: this.vpc,
      vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_ISOLATED },
      storageEncrypted: true,
      deletionProtection: true,
      backup: { retention: Duration.days(14) },
      removalPolicy: RemovalPolicy.RETAIN,
      copyTagsToSnapshot: true,
      parameters: { "rds.force_ssl": "1" },
    });
    this.cluster.connections.allowDefaultPortFrom(this.clientSecurityGroup);
    this.applicationSecret = new secretsmanager.Secret(
      this,
      "ApplicationDatabaseSecret",
      {
        description: "RLSを迂回できないRecipeWeave実行ロールの資格情報",
        generateSecretString: {
          secretStringTemplate: JSON.stringify({ username: "recipeweave_app" }),
          generateStringKey: "password",
          passwordLength: 40,
          excludePunctuation: true,
        },
        removalPolicy: RemovalPolicy.RETAIN,
      },
    );

    this.userPool = new cognito.UserPool(this, "Users", {
      selfSignUpEnabled: true,
      signInAliases: { email: true },
      autoVerify: { email: true },
      accountRecovery: cognito.AccountRecovery.EMAIL_ONLY,
      passwordPolicy: {
        minLength: 12,
        requireLowercase: true,
        requireUppercase: true,
        requireDigits: true,
        requireSymbols: true,
      },
      deletionProtection: true,
      removalPolicy: RemovalPolicy.RETAIN,
    });
    // SRPで発行するアクセストークンにはaws.cognito.signin.user.adminが付く。
    // ホスト型ログイン画面とOAuthのコールバック設定は、今後のクラウド認証画面で導入する。
    this.userPoolClient = this.userPool.addClient("WebClient", {
      generateSecret: false,
      authFlows: { userSrp: true },
      preventUserExistenceErrors: true,
      enableTokenRevocation: true,
      accessTokenValidity: Duration.minutes(15),
      idTokenValidity: Duration.minutes(15),
      refreshTokenValidity: Duration.days(7),
    });
    this.cognitoIssuer = `https://cognito-idp.${this.region}.${this.urlSuffix}/${this.userPool.userPoolId}`;

    new CfnOutput(this, "DatabaseHost", {
      value: this.cluster.clusterEndpoint.hostname,
    });
    new CfnOutput(this, "DatabaseClusterArn", {
      value: this.cluster.clusterArn,
    });
    new CfnOutput(this, "ApplicationDatabaseSecretArn", {
      value: this.applicationSecret.secretArn,
    });
    new CfnOutput(this, "UserPoolId", { value: this.userPool.userPoolId });
    new CfnOutput(this, "CognitoClientId", {
      value: this.userPoolClient.userPoolClientId,
    });
    new CfnOutput(this, "CognitoIssuer", {
      value: this.cognitoIssuer,
    });
  }
}
