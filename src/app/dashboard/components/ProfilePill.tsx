"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import Image from "next/image";

interface Props {
  displayName: string;
  profilePhotoUrl: string;
  lang: "en" | "zh";
  userEmail: string;
}

export function ProfilePill({ displayName, profilePhotoUrl, lang, userEmail }: Props) {
  const t = useTranslations("dashboard");
  const tCommon = useTranslations("common");
  const [currentLang, setCurrentLang] = useState<"en" | "zh">(lang);
  const [langLoading, setLangLoading] = useState(false);
  const router = useRouter();

  async function toggleLang() {
    const newLang = currentLang === "en" ? "zh" : "en";
    setLangLoading(true);
    try {
      await fetch("/api/user/lang", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lang: newLang }),
      });
      // Set NEXT_LOCALE cookie so next-intl picks up the new locale on refresh
      document.cookie = `NEXT_LOCALE=${newLang}; path=/; max-age=31536000; SameSite=Lax`;
      setCurrentLang(newLang);
      router.refresh();
    } finally {
      setLangLoading(false);
    }
  }

  const initials = (displayName || userEmail)
    .split(/[\s@]/)
    .filter(Boolean)
    .slice(0, 2)
    .map((s) => s[0].toUpperCase())
    .join("");

  return (
    <div className="flex items-center justify-between gap-4 rounded-2xl bg-white/5 border border-white/10 px-5 py-3">
      {/* Avatar + name */}
      <div className="flex items-center gap-3 min-w-0">
        <div className="w-9 h-9 rounded-full overflow-hidden bg-blue-600 flex-none flex items-center justify-center">
          {profilePhotoUrl ? (
            <Image
              src={profilePhotoUrl}
              alt={displayName}
              width={36}
              height={36}
              className="object-cover w-full h-full"
              unoptimized
            />
          ) : (
            <span className="text-xs font-bold text-white">{initials}</span>
          )}
        </div>
        <span className="text-sm text-white font-medium truncate">
          {displayName || userEmail}
        </span>
      </div>

      {/* Controls */}
      <div className="flex items-center gap-3 flex-none">
        {/* EN/ZH toggle */}
        <button
          type="button"
          onClick={toggleLang}
          disabled={langLoading}
          className="text-xs font-semibold px-4 py-2.5 min-h-[44px] min-w-[44px] rounded-lg bg-white/10 hover:bg-white/15 text-slate-300 hover:text-white transition-colors disabled:opacity-50"
          aria-label="Toggle language"
        >
          {langLoading ? "…" : currentLang === "en" ? t("toggleLang") : t("toggleLangZh")}
        </button>

        {/* Logout */}
        <form action="/api/auth/logout" method="POST">
          <button
            type="submit"
            className="text-xs text-slate-500 hover:text-slate-300 transition-colors px-3 py-2.5 min-h-[44px] rounded-lg hover:bg-white/5"
          >
            {tCommon("signOut")}
          </button>
        </form>
      </div>
    </div>
  );
}
