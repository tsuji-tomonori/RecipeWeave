import tseslint from "typescript-eslint";
import awscdk from "eslint-plugin-awscdk";

export default tseslint.config(
  { ignores: ["node_modules/**", "cdk.out/**"] },
  ...tseslint.configs.strict,
  {
    files: ["**/*.ts"],
    plugins: { awscdk },
    rules: {
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/consistent-type-imports": "error",
      "awscdk/no-mutable-property-of-props-interface": "error",
      "awscdk/no-import-private": "error",
    },
  },
);
