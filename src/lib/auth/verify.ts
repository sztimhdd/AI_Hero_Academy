/**
 * Centralized auth verification.
 *
 * In production: verifies the __session Firebase session cookie.
 * In LOCAL_UAT mode: accepts the magic cookie value "uat-bypass" and
 *   returns the test UID / email from environment variables — no Firebase
 *   Auth API call needed.
 *
 * This allows running full UAT against a real Firestore instance without
 * needing Identity Toolkit API or NEXT_PUBLIC_FIREBASE_* configured.
 */
import type { ReadonlyRequestCookies } from "next/dist/server/web/spec-extension/adapters/request-cookies";
import { getAdminAuth } from "@/lib/firebase/admin";

const UAT_COOKIE_VALUE = "uat-bypass";

export interface AuthResult {
  uid: string;
  email: string;
  displayName: string;
}

/**
 * Verify the session cookie and return {uid, email, displayName}.
 * Throws if the cookie is missing or invalid.
 */
export async function getAuthFromCookies(
  cookies: ReadonlyRequestCookies | { get: (name: string) => { value: string } | undefined }
): Promise<AuthResult> {
  const sessionCookie = cookies.get("__session")?.value;
  if (!sessionCookie) throw new Error("No session cookie");

  // LOCAL_UAT bypass — never active in production
  if (process.env.LOCAL_UAT === "true" && sessionCookie === UAT_COOKIE_VALUE) {
    return {
      uid: process.env.UAT_TEST_UID ?? "uat-test-uid",
      email: process.env.DEV_USER_EMAIL ?? "uat@dev.local",
      displayName: "UAT Test User",
    };
  }

  const decoded = await getAdminAuth().verifySessionCookie(sessionCookie, true);
  return {
    uid: decoded.uid,
    email: decoded.email ?? "",
    displayName: decoded.name ?? "",
  };
}
