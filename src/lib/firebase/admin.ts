import { initializeApp, getApps, cert } from "firebase-admin/app";
import { getAuth, Auth } from "firebase-admin/auth";

// Lazy-initialized — only runs on first actual server-side call, not at build time.
let _adminAuth: Auth | null = null;

export function getAdminAuth(): Auth {
  if (_adminAuth) return _adminAuth;

  const app = getApps().length
    ? getApps()[0]
    : initializeApp({
        credential: cert({
          projectId: process.env.FIREBASE_ADMIN_PROJECT_ID!,
          clientEmail: process.env.FIREBASE_ADMIN_CLIENT_EMAIL!,
          privateKey: process.env.FIREBASE_ADMIN_PRIVATE_KEY?.replace(/\\n/g, "\n"),
        }),
      });

  _adminAuth = getAuth(app);
  return _adminAuth;
}
