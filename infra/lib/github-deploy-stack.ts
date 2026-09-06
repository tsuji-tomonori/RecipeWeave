import { CfnOutput, Duration, Stack, aws_iam as iam } from "aws-cdk-lib";
import type { StackProps } from "aws-cdk-lib";
import type { Construct } from "constructs";

export interface GitHubDeployStackProps extends StackProps {
  readonly existingProviderArn: string;
  readonly stage?: string;
  readonly branch: string;
  readonly bootstrapQualifier: string;
}

/** 任意の構成。アカウント内の既存プロバイダーを参照し、アカウントの初期構築は行わない。 */
export class GitHubDeployStack extends Stack {
  public constructor(
    scope: Construct,
    id: string,
    props: GitHubDeployStackProps,
  ) {
    super(scope, id, props);
    const provider = iam.OpenIdConnectProvider.fromOpenIdConnectProviderArn(
      this,
      "ExistingGitHubProvider",
      props.existingProviderArn,
    );
    const role = new iam.Role(this, "GitHubDeployRole", {
      assumedBy: new iam.OpenIdConnectPrincipal(provider, {
        StringEquals: {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
          "token.actions.githubusercontent.com:sub": `repo:tsuji-tomonori/RecipeWeave:ref:refs/heads/${props.branch}`,
        },
      }),
      maxSessionDuration: Duration.hours(1),
      description:
        "Exact RecipeWeave branch only; assumes existing CDK bootstrap roles.",
    });
    role.addToPolicy(
      new iam.PolicyStatement({
        actions: ["sts:AssumeRole"],
        resources: [
          "deploy",
          "file-publishing",
          "image-publishing",
          "lookup",
        ].map((purpose) =>
          this.formatArn({
            service: "iam",
            region: "",
            resource: "role",
            resourceName: `cdk-${props.bootstrapQualifier}-${purpose}-role-${this.account}-${this.region}`,
          }),
        ),
      }),
    );
    // 配備後のスキーマ移行はこの環境の専用関数だけに限定する。
    role.addToPolicy(
      new iam.PolicyStatement({
        actions: ["lambda:InvokeFunction"],
        resources: [
          this.formatArn({
            service: "lambda",
            resource: "function",
            resourceName: `RecipeWeave-${props.stage ?? "dev"}-Service-Migration`,
          }),
        ],
      }),
    );
    new CfnOutput(this, "GitHubDeployRoleArn", { value: role.roleArn });
  }
}
