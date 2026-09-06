import assert from "node:assert/strict";
import { test } from "node:test";
import { App } from "aws-cdk-lib";
import { Match, Template } from "aws-cdk-lib/assertions";
import { readConfig } from "../lib/config.js";
import { DataStack } from "../lib/data-stack.js";
import { GitHubDeployStack } from "../lib/github-deploy-stack.js";
import { assertBuiltAsset } from "../lib/service-stack.js";

const env = { account: "111122223333", region: "us-east-1" };

test("retains protected user data", () => {
  const data = new DataStack(new App(), "TestData", { env });
  const dataTemplate = Template.fromStack(data);
  assert.equal(data.terminationProtection, true);
  dataTemplate.hasResource("AWS::DSQL::Cluster", {
    Properties: { DeletionProtectionEnabled: true },
    DeletionPolicy: "Retain",
    UpdateReplacePolicy: "Retain",
  });
  dataTemplate.hasResource("AWS::Cognito::UserPool", {
    Properties: Match.objectLike({ DeletionProtection: "ACTIVE" }),
    DeletionPolicy: "Retain",
  });
});

test("OIDC trust is one repository branch and imports an existing provider only", () => {
  const oidcApp = new App();
  const oidc = new GitHubDeployStack(oidcApp, "TestGitHub", {
    env,
    existingProviderArn:
      "arn:aws:iam::111122223333:oidc-provider/token.actions.githubusercontent.com",
    branch: "dev",
    bootstrapQualifier: "hnb659fds",
  });
  const oidcTemplate = Template.fromStack(oidc);
  oidcTemplate.resourceCountIs("AWS::IAM::OIDCProvider", 0);
  oidcTemplate.hasResourceProperties("AWS::IAM::Role", {
    AssumeRolePolicyDocument: {
      Version: "2012-10-17",
      Statement: [
        {
          Action: "sts:AssumeRoleWithWebIdentity",
          Effect: "Allow",
          Principal: {
            Federated:
              "arn:aws:iam::111122223333:oidc-provider/token.actions.githubusercontent.com",
          },
          Condition: {
            StringEquals: {
              "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
              "token.actions.githubusercontent.com:sub":
                "repo:tsuji-tomonori/RecipeWeave:ref:refs/heads/dev",
            },
          },
        },
      ],
    },
  });
  oidcTemplate.hasResourceProperties("AWS::IAM::Policy", {
    PolicyDocument: {
      Version: "2012-10-17",
      Statement: [
        {
          Action: "sts:AssumeRole",
          Effect: "Allow",
          Resource: [
            "deploy",
            "file-publishing",
            "image-publishing",
            "lookup",
          ].map((purpose) => ({
            "Fn::Join": [
              "",
              [
                "arn:",
                { Ref: "AWS::Partition" },
                `:iam::111122223333:role/cdk-hnb659fds-${purpose}-role-111122223333-us-east-1`,
              ],
            ],
          })),
        },
      ],
    },
  });
});

test("rejects wildcard deployment trust and missing actual build artifacts", () => {
  assert.throws(
    () => readConfig(new App({ context: { githubBranch: "*" } })),
    /exact branch/,
  );
  assert.throws(
    () => readConfig(new App({ context: { githubOidcProviderArn: "*" } })),
    /existing GitHub OIDC provider/,
  );
  assert.throws(
    () => assertBuiltAsset("/missing-recipeweave-build", "app/handler.py"),
    /real deployable asset/,
  );
});
