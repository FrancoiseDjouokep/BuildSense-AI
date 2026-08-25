import { useQuery } from "@tanstack/react-query";
import { apiClient } from "../../lib/api-client";
import type { PricingResponse } from "./types";

export function useDevis(planId: string | undefined) {
  return useQuery({
    queryKey: ["devis", planId],
    queryFn: async () => {
      const { data } = await apiClient.get<PricingResponse>(`/pricing/by-plan/${planId}`);
      return data;
    },
    enabled: Boolean(planId),
  });
}