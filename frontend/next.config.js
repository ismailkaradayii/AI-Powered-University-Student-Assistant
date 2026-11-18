/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: "/pages/login",
        destination: "/login",
      },
      {
        source: "/pages/dashboard",
        destination: "/dashboard",
      },
      {
        source: "/pages/admin",
        destination: "/admin",
      },
    ];
  },
};

module.exports = nextConfig;
