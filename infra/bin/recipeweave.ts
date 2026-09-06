import { fileURLToPath } from "node:url";
import { App, DefaultStackSynthesizer, Tags } from "aws-cdk-lib";
import { readConfig } from "../lib/config.js";
import { DataStack } from "../lib/data-stack.js";
import { GitHubDeployStack } from "../lib/github-deploy-stack.js";
import { ServiceStack } from "../lib/service-stack.js";

const app = new App();
const config = readConfig(app);
const stackProps = () => ({
  env: config.env,
  synthesizer: new DefaultStackSynthesizer({
    qualifier: config.bootstrapQualifier,
  }),
});
const data = new DataStack(
  app,
  `RecipeWeave-${config.stage}-Data`,
  stackProps(),
);
new ServiceStack(app, `RecipeWeave-${config.stage}-Service`, {
  ...stackProps(),
  data,
  repositoryRoot: fileURLToPath(new URL("../../", import.meta.url)),
});
if (config.githubOidcProviderArn !== undefined) {
  new GitHubDeployStack(app, `RecipeWeave-${config.stage}-GitHubDeploy`, {
    ...stackProps(),
    existingProviderArn: config.githubOidcProviderArn,
    branch: config.githubBranch,
    bootstrapQualifier: config.bootstrapQualifier,
  });
}
Tags.of(app).add("Project", "RecipeWeave");
Tags.of(app).add("Environment", config.stage);
app.synth();
