import { getRequestConfig } from "next-intl/server";
import { cookies } from "next/headers";

export default getRequestConfig(async () => {
  // Locale comes from NEXT_LOCALE cookie (set on lang toggle) or defaults to "en"
  const cookieStore = await cookies();
  const locale = cookieStore.get("NEXT_LOCALE")?.value ?? "en";
  const safeLocale = locale === "zh" ? "zh" : "en";

  const messages = (
    await import(`./messages/${safeLocale}.json`)
  ).default;

  return {
    locale: safeLocale,
    messages,
  };
});
