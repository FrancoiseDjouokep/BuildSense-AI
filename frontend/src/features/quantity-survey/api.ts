import { useQuery } from "@tanstack/react-query";
import { apiClient } from "../../lib/api-client";
import type { QuantitySurveyResponse } from "./types";

export function useQuantitySurvey(planId: string | undefined) {
  return useQuery({
    queryKey: ["quantity-survey", planId],
    queryFn: async () => {
      const { data } = await apiClient.get<QuantitySurveyResponse>(`/quantity-surveys/by-plan/${planId}`);
      return data;
    },
    enabled: Boolean(planId),
  });
}