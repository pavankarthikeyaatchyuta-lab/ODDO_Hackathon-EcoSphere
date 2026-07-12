/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    const raw = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
    const backendUrl = raw.startsWith("http") ? raw : `https://${raw}`
    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/api/:path*`,
      },
    ]
  },
}
module.exports = nextConfig
