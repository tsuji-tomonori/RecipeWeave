import {
  CfnOutput,
  Duration,
  RemovalPolicy,
  Stack,
  aws_cognito as cognito,
  aws_dsql as dsql,
} from "aws-cdk-lib";
import type { StackProps } from "aws-cdk-lib";
import type { Construct } from "constructs";

/** Stateful resources have separate lifecycle and never use auto-delete. */
export class DataStack extends Stack {
  public readonly cluster: dsql.CfnCluster;
  public readonly userPool: cognito.UserPool;
  public readonly userPoolClient: cognito.UserPoolClient;
  public readonly cognitoIssuer: string;

  public constructor(scope: Construct, id: string, props: StackProps) {
    super(scope, id, { ...props, terminationProtection: true });

    this.cluster = new dsql.CfnCluster(this, "InventoryCluster", {
      deletionProtectionEnabled: true,
    });
    this.cluster.applyRemovalPolicy(RemovalPolicy.RETAIN);

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
    // SRP issues access tokens with aws.cognito.signin.user.admin. Hosted-login UI
    // and OAuth callback configuration belong to a later cloud-auth UI release.
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

    new CfnOutput(this, "DsqlHost", { value: this.cluster.attrEndpoint });
    new CfnOutput(this, "DsqlClusterArn", {
      value: this.cluster.attrResourceArn,
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
