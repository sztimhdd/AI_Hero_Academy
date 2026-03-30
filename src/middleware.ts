import { NextRequest, NextResponse } from "next/server";

const SESSION_COOKIE_NAME = "__session";

// Routes that don't need auth
const PUBLIC_PATHS = ["/", "/api/auth/session", "/api/auth/logout", "/api/auth/dev-login", "/demo", "/api/auth/demo-login"];

/**
 * Lightweight Edge-compatible middleware.
 * Only checks cookie PRESENCE here — actual JWT verification happens in each
 * server component and API route (Node.js runtime) via firebase-admin.
 *
 * This is intentional: firebase-admin requires Node.js and cannot run in the
 * Edge runtime. Security is enforced at the page/route level.
 */
export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;

  // Always allow public routes and Next.js internals
  if (
    PUBLIC_PATHS.includes(pathname) ||
    pathname.startsWith("/demo") ||
    pathname.startsWith("/_next/") ||
    pathname.startsWith("/favicon")
  ) {
    // Optimistic redirect: if cookie exists, send logged-in users away from /
    // If the cookie turns out to be invalid, /dashboard will redirect back to /
    if (pathname === "/") {
      const sessionCookie = req.cookies.get(SESSION_COOKIE_NAME)?.value;
      if (sessionCookie) {
        return NextResponse.redirect(new URL("/dashboard", req.url));
      }
    }
    return NextResponse.next();
  }

  // Protected routes — require session cookie to be present
  const sessionCookie = req.cookies.get(SESSION_COOKIE_NAME)?.value;
  if (!sessionCookie) {
    return NextResponse.redirect(new URL("/", req.url));
  }

  // Pass through — the page/API route will verify the cookie with firebase-admin
  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico).*)",
  ],
};
