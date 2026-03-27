import { cookies, headers } from "next/headers";
import { redirect } from "next/navigation";
import { getAdminAuth } from "@/lib/firebase/admin";
import { getUser } from "@/lib/firestore/db";

export default async function DashboardPage() {
  // Verify session (middleware already guards this route, but double-check here
  // to get the uid for Firestore lookup)
  const sessionCookie = (await cookies()).get("__session")?.value;
  if (!sessionCookie) redirect("/");

  let uid: string;
  try {
    const decoded = await getAdminAuth().verifySessionCookie(sessionCookie, true);
    uid = decoded.uid;
  } catch {
    redirect("/");
  }

  // Check if user has completed onboarding
  const user = await getUser(uid);
  if (!user?.program_started_at) {
    redirect("/onboarding");
  }

  // Read forwarded headers from middleware
  const headersList = await headers();
  const userEmail = headersList.get("x-email") ?? user.user_email;

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-2xl space-y-8 text-center">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold text-white">
            Welcome back, {user.display_name || userEmail.split("@")[0]}
          </h1>
          <p className="text-slate-400">Your AI transformation journey continues.</p>
        </div>

        {/* Pillar grid stub */}
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          {["P1", "P2", "P3", "P4", "P5", "P6"].map((p, idx) => (
            <div
              key={p}
              className={`rounded-2xl p-5 border text-center ${
                idx === 0
                  ? "bg-blue-600/30 border-blue-500/50"
                  : "bg-white/5 border-white/10 opacity-60"
              }`}
            >
              <div className="text-2xl font-bold text-white">{p}</div>
              <div className="text-xs text-slate-400 mt-1">
                {idx === 0 ? "Unlocked" : "Locked"}
              </div>
            </div>
          ))}
        </div>

        <p className="text-slate-500 text-sm">
          Full dashboard coming in Sprint 4. For now, Day 1 is ready to begin.
        </p>

        <form action="/api/auth/logout" method="POST">
          <button
            type="submit"
            className="text-slate-500 hover:text-slate-300 text-sm underline transition-colors"
          >
            Sign out
          </button>
        </form>
      </div>
    </main>
  );
}
