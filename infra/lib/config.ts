import type { App, Environment } from "aws-cdk-lib";

export interface DeployConfig {
  readonly stage: string;
  readonly env: Environment;
  readonly githubOidcProviderArn?: string;
  readonly githubBranch: string;
  readonly bootstrapQualifier: string;
}

function contextString(
  app: App,
  name: string,
  fallback?: string,
): string | undefined {
  const value: unknown = app.node.tryGetContext(name);
  if (value === undefined) return fallback;
  if (typeof value !== "string" || value.length === 0) {
    throw new Error(`${name} must be a non-empty string`);
  }
  return value;
}

export function readConfig(app: App): DeployConfig {
  const stage = contextString(app, "stage", "dev") ?? "dev";
  if (!/^[a-z][a-z0-9-]{0,15}$/.test(stage)) {
    throw new Error(
      "stage must use lowercase letters, digits and hyphens (1–16 characters)",
    );
  }
  const githubBranch = contextString(app, "githubBranch", "dev") ?? "dev";
  if (!/^[A-Za-z0-9_./-]+$/.test(githubBranch) || githubBranch.includes("..")) {
    throw new Error(
      "githubBranch must be one exact branch; wildcards are forbidden",
    );
  }
  const bootstrapQualifier =
    contextString(app, "bootstrapQualifier", "hnb659fds") ?? "hnb659fds";
  if (!/^[a-zA-Z0-9]{1,10}$/.test(bootstrapQualifier)) {
    throw new Error("bootstrapQualifier must be 1–10 alphanumeric characters");
  }
  const githubOidcProviderArn = contextString(app, "githubOidcProviderArn");
  if (
    githubOidcProviderArn !== undefined &&
    !/^arn:aws:iam::[0-9]{12}:oidc-provider\/token\.actions\.githubusercontent\.com$/.test(
      githubOidcProviderArn,
    )
  ) {
    throw new Error(
      "githubOidcProviderArn must identify an existing GitHub OIDC provider",
    );
  }
  const account = process.env.CDK_DEFAULT_ACCOUNT;
  const env: Environment = {
    region: process.env.CDK_DEFAULT_REGION ?? "us-east-1",
    ...(account === undefined ? {} : { account }),
  };
  return {
    stage,
    env,
    githubBranch,
    bootstrapQualifier,
    ...(githubOidcProviderArn === undefined ? {} : { githubOidcProviderArn }),
  };
}
