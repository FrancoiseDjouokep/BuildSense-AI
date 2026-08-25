import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "../../lib/api-client";
import type { Plan, PlanAnalysis, PlanUploadResponse, Project, ProjectCreateInput } from "./types";

export function useProjects() {
  return useQuery({
    queryKey: ["projects"],
    queryFn: async () => {
      const { data } = await apiClient.get<Project[]>("/projects/");
      return data;
    },
  });
}

export function useCreateProject() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (input: ProjectCreateInput) => {
      const { data } = await apiClient.post<Project>("/projects/", input);
      return data;
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["projects"] }),
  });
}

export function useProject(projectId: string | undefined) {
  return useQuery({
    queryKey: ["project", projectId],
    queryFn: async () => {
      const { data } = await apiClient.get<Project>(`/projects/${projectId}`);
      return data;
    },
    enabled: Boolean(projectId),
  });
}

export function usePlans(projectId: string | undefined) {
  return useQuery({
    queryKey: ["plans", projectId],
    queryFn: async () => {
      const { data } = await apiClient.get<Plan[]>(`/projects/${projectId}/plans`);
      return data;
    },
    enabled: Boolean(projectId),
  });
}

export function useUploadPlan(projectId: string | undefined) {
    const queryClient = useQueryClient();
    return useMutation({
      mutationFn: async (file: File) => {
        const formData = new FormData();
        formData.append("file", file);
        const { data } = await apiClient.post<PlanUploadResponse>(`/projects/${projectId}/plans`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        return data;
      },
      onSuccess: () => queryClient.invalidateQueries({ queryKey: ["plans", projectId] }),
    });
}

export function usePlanAnalyses(projectId: string | undefined, planId: string | undefined) {
  return useQuery({
    queryKey: ["plan-analyses", projectId, planId],
    queryFn: async () => {
      const { data } = await apiClient.get<PlanAnalysis[]>(
        `/plan-analysis/projects/${projectId}/plans/${planId}/analyses`
      );
      return data;
    },
    enabled: Boolean(projectId && planId),
  });
}

export function useAnalysePlan(projectId: string | undefined) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (planId: string) => {
      const { data } = await apiClient.post<PlanAnalysis>(
        `/plan-analysis/projects/${projectId}/plans/${planId}/analyse`
      );
      return data;
    },
    onSuccess: (_data, planId) => {
      queryClient.invalidateQueries({ queryKey: ["plan-analyses", projectId, planId] });
    },
  });
}