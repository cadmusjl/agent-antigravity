import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// This middleware is optional for Supabase auth
// We handle auth checks client-side in page components
// But you can add server-side protection here if needed

export function middleware(request: NextRequest) {
  // For now, just allow all requests
  // Auth is handled client-side via useAuth hook
  return NextResponse.next()
}

// Only run middleware on specific paths if needed
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
