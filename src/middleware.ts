import { NextRequest, NextResponse } from "next/server";
import { getAdminAuth } from "@/lib/firebase/admin";

const SESSION_COOKIE_NAME = "__session";

// Routes that don't need auth
const PUBLIC_PATHS = ["/", "/api/auth/session", "/api/auth/logout"];

export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;

  // Always allow public routes and Next.js internals
  if (
    PUBLIC_PATHS.includes(pathname) ||
    pathname.startsWith("/_next/") ||
    pathname.startsWith("/favicon")
  ) {
    // If authenticated user hits landing page, redirect to dashboard
    if (pathname === "/") {
      const sessionCookie = req.cookies.get(SESSION_COOKIE_NAME)?.value;
      if (sessionCookie) {
        try {
          await getAdminAuth().verifySessionCookie(sessionCookie, true);
          return NextResponse.redirect(new URL("/dashboard", req.url));
        } catch {
          // Invalid cookie — fall through and show landing page
        }
      }
    }
    return NextResponse.next();
  }

  // Protected routes — require valid session cookie
  const sessionCookie = req.cookies.get(SESSION_COOKIE_NAME)?.value;
  if (!sessionCookie) {
    return NextResponse.redirect(new URL("/", req.url));
  }

  try {
    const decoded = await getAdminAuth().verifySessionCookie(sessionCookie, true);

    // New users without program_started_at go to onboarding
    if (pathname.startsWith("/dashboard")) {
      // The dashboard page itself will check Firestore for program_started_at
      // and redirect to /onboarding if needed — handled server-side in the page
    }

    // Attach uid to request headers for downstream server components
    const requestHeaders = new Headers(req.headers);
    requestHeaders.set("x-uid", decoded.uid);
    requestHeaders.set("x-email", decoded.email ?? "");

    return NextResponse.next({ request: { headers: requestHeaders } });
  } catch {
    // Session cookie invalid or revoked
    const res = NextResponse.redirect(new URL("/", req.url));
    res.cookies.set(SESSION_COOKIE_NAME, "", { maxAge: 0, path: "/" });
    return res;
  }
}

export const config = {
  matcher: [
    /*
     * Match all paths except:
     * - _next/static (static files)
     * - _next/image (image optimization)
     * - favicon.ico
     */
    "/((?!_next/static|_next/image|favicon.ico).*)",
  ],
};
