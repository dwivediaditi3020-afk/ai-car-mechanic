import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  skipTrailingSlashRedirect: true,

  async rewrites() {
    return [
      {
        source: "/api/chat/",
        destination:
          "http://ai-car-mechanic-env.eba-mrgpjfrd.ap-south-1.elasticbeanstalk.com/api/chat/",
      },
      {
        source: "/api/upload/",
        destination:
          "http://ai-car-mechanic-env.eba-mrgpjfrd.ap-south-1.elasticbeanstalk.com/api/upload/",
      },
      {
        source: "/api/diagnosis/",
        destination:
          "http://ai-car-mechanic-env.eba-mrgpjfrd.ap-south-1.elasticbeanstalk.com/api/diagnosis/",
      },
      {
        source: "/api/booking/",
        destination:
          "http://ai-car-mechanic-env.eba-mrgpjfrd.ap-south-1.elasticbeanstalk.com/api/booking/",
      },
      {
        source: "/api/booking/:booking_id/",
        destination:
          "http://ai-car-mechanic-env.eba-mrgpjfrd.ap-south-1.elasticbeanstalk.com/api/booking/:booking_id/",
      },
      {
        source: "/media/:path*",
        destination:
          "http://ai-car-mechanic-env.eba-mrgpjfrd.ap-south-1.elasticbeanstalk.com/media/:path*",
      },
    ];
  },
};

export default nextConfig;