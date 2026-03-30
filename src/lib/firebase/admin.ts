import { initializeApp, getApps, cert, applicationDefault } from "firebase-admin/app";
import { getAuth, Auth } from "firebase-admin/auth";
import * as fs from "fs";
import * as path from "path";

// Lazy-initialized — only runs on first actual server-side call, not at build time.
let _adminAuth: Auth | null = null;

function buildCredential() {
  // Option 1: Explicit env vars (CI / production)
  if (
    process.env.FIREBASE_ADMIN_PROJECT_ID &&
    process.env.FIREBASE_ADMIN_CLIENT_EMAIL &&
    (process.env.FIREBASE_ADMIN_PRIVATE_KEY_B64 || process.env.FIREBASE_ADMIN_PRIVATE_KEY)
  ) {
    // Prefer B64-encoded key (safe across YAML/env var newline handling);
    // fall back to the raw key with \n → newline conversion.
    const privateKey = process.env.FIREBASE_ADMIN_PRIVATE_KEY_B64
      ? Buffer.from(process.env.FIREBASE_ADMIN_PRIVATE_KEY_B64, "base64").toString("utf8")
      : process.env.FIREBASE_ADMIN_PRIVATE_KEY!.replace(/\\n/g, "\n");

    return cert({
      projectId: process.env.FIREBASE_ADMIN_PROJECT_ID,
      clientEmail: process.env.FIREBASE_ADMIN_CLIENT_EMAIL,
      privateKey,
    });
  }

  // Option 2: GOOGLE_APPLICATION_CREDENTIALS path (local dev)
  const credPath = process.env.GOOGLE_APPLICATION_CREDENTIALS;
  if (credPath) {
    const resolved = path.isAbsolute(credPath)
      ? credPath
      : path.join(process.cwd(), credPath);
    if (fs.existsSync(resolved)) {
      const sa = JSON.parse(fs.readFileSync(resolved, "utf-8"));
      return cert({
        projectId: sa.project_id,
        clientEmail: sa.client_email,
        privateKey: sa.private_key,
      });
    }
  }

  // Option 3: Application Default Credentials (GCP managed environments)
  return applicationDefault();
}

export function getAdminAuth(): Auth {
  if (_adminAuth) return _adminAuth;

  const app = getApps().length ? getApps()[0] : initializeApp({ credential: buildCredential() });

  _adminAuth = getAuth(app);
  return _adminAuth;
}
