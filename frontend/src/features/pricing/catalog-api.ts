import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "../../lib/api-client";
import type { UnitPrice, UnitPriceCreateInput, UnitPriceUpdateInput } from "./catalog-types";

export function useUnitPrices() {
  return useQuery({
    queryKey: ["unit-prices"],
    queryFn: async () => {
      const { data } = await apiClient.get<UnitPrice[]>("/pricing/unit-prices");
      return data;
    },
  });
}

export function useCreateUnitPrice() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (input: UnitPriceCreateInput) => {
      const { data } = await apiClient.post<UnitPrice>("/pricing/unit-prices", input);
      return data;
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["unit-prices"] }),
  });
}

export function useUpdateUnitPrice() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, ...input }: UnitPriceUpdateInput & { id: string }) => {
      const { data } = await apiClient.patch<UnitPrice>(`/pricing/unit-prices/${id}`, input);
      return data;
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["unit-prices"] }),
  });
}

export function useDeleteUnitPrice() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      await apiClient.delete(`/pricing/unit-prices/${id}`);
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["unit-prices"] }),
  });
}