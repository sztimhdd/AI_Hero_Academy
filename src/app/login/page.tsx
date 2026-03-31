"use client";

import { useState } from "react";
import { firebaseApp } from "@/lib/firebase/client";
import {
  getAuth,
  signInWithPopup,
  GoogleAuthProvider,
  FacebookAuthProvider,
  OAuthProvider,
} from "firebase/auth";
import { en } from "@/lib/i18n/en";
import { zh } from "@/lib/i18n/zh";
import { useRouter } from "next/navigation";
import Link from "next/link";

type Lang = "en" | "zh";
type T = typeof en;

function t(copy: T, key: keyof T, vars?: Record<string, string | number>) {
  let str = copy[key] as string;
  if (vars) {
    for (const [k, v] of Object.entries(vars)) {
      str = str.replace(`{${k}}`, String(v));
    }
  }
  return str;
}

export default function LoginPage() {
  const [lang, setLang] = useState<Lang>("en");
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const copy = lang === "en" ? en : (zh as unknown as T);

  async function signInWith(providerName: "google" | "facebook" | "linkedin") {
    setError(null);
    setLoading(providerName);
    const auth = getAuth(firebaseApp);
    try {
      let provider;
      if (providerName === "google") {
        provider = new GoogleAuthProvider();
      } else if (providerName === "facebook") {
        provider = new FacebookAuthProvider();
      } else {
        provider = new OAuthProvider("oidc.linkedin");
      }

      const result = await signInWithPopup(auth, provider);
      const idToken = await result.user.getIdToken();

      const res = await fetch("/api/auth/session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idToken }),
      });

      if (!res.ok) throw new Error("Session creation failed");

      router.push("/dashboard");
    } catch (err) {
      console.error("Sign-in error:", err);
      setError(t(copy, "common.error"));
    } finally {
      setLoading(null);
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 flex flex-col items-center justify-center px-4">
      {/* Lang toggle */}
      <button
        type="button"
        onClick={() => setLang(lang === "en" ? "zh" : "en")}
        className="absolute top-4 right-4 text-sm text-slate-400 hover:text-white transition-colors"
      >
        {t(copy, "landing.lang_toggle")}
      </button>

      <div className="w-full max-w-md space-y-8 text-center">
        {/* Back to home */}
        <Link
          href="/"
          className="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-300 transition-colors"
        >
          ← {lang === "en" ? "Back" : "返回"}
        </Link>

        {/* Title */}
        <div className="space-y-2">
          <h1 className="text-3xl font-bold text-white">
            {lang === "en" ? "Sign in to continue" : "登录以继续"}
          </h1>
          <p className="text-slate-400 text-sm">
            {t(copy, "landing.tagline")}
          </p>
        </div>

        {/* Auth buttons */}
        <div className="space-y-3">
          <AuthButton
            label={t(copy, "landing.signin_google")}
            loading={loading === "google"}
            onClick={() => signInWith("google")}
            icon={<GoogleIcon />}
          />
          <AuthButton
            label={t(copy, "landing.signin_linkedin")}
            loading={loading === "linkedin"}
            onClick={() => signInWith("linkedin")}
            icon={<LinkedInIcon />}
          />
          <AuthButton
            label={t(copy, "landing.signin_facebook")}
            loading={loading === "facebook"}
            onClick={() => signInWith("facebook")}
            icon={<FacebookIcon />}
          />
        </div>

        {error && (
          <p className="text-red-400 text-sm">{error}</p>
        )}

        <p className="text-slate-500 text-xs">{t(copy, "landing.terms")}</p>
      </div>
    </main>
  );
}

interface AuthButtonProps {
  label: string;
  loading: boolean;
  onClick: () => void;
  icon: React.ReactNode;
}

function AuthButton({ label, loading, onClick, icon }: AuthButtonProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={loading}
      className="w-full flex items-center gap-3 bg-white/10 hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium py-3 px-5 rounded-xl transition-all duration-150 border border-white/10"
    >
      <span className="w-5 h-5 flex-shrink-0">{icon}</span>
      <span className="flex-1 text-left">
        {loading ? "…" : label}
      </span>
    </button>
  );
}

function GoogleIcon() {
  return (
    <svg viewBox="0 0 24 24" className="w-5 h-5">
      <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
      <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
      <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
      <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
    </svg>
  );
}

function LinkedInIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="#0A66C2" className="w-5 h-5">
      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
    </svg>
  );
}

function FacebookIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="#1877F2" className="w-5 h-5">
      <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
    </svg>
  );
}
