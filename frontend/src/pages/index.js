import { useEffect } from "react";
import { useRouter } from "next/router";
import { getAccessToken } from "../lib/api";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const token = getAccessToken();
    if (token) {
      router.replace("/pages/dashboard");
    } else {
      router.replace("/pages/login");
    }
  }, [router]);

  return null;
}
