import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin("./src/i18n/request.ts");

const nextConfig: NextConfig = {
  output: "standalone",
  // Exclude Python files from being treated as Next.js page routes.
  // The legacy Streamlit `pages/` directory at the repo root contains .py files
  // that Next.js would otherwise try to parse as Pages Router routes.
  pageExtensions: ["tsx", "ts", "jsx", "js"],
};

export default withNextIntl(nextConfig);
