export interface Project {
    id: string;
    name: string;
    description: string | null;
    created_at: string;
    updated_at: string;
}

export interface ProjectCreateInput {
    name: string;
    description?: string;
}

export type PlanStatus = string; // ⚠️ enum réel non fourni (upload/models.py) — élargis si besoin

export interface Plan {
    id: string;
    project_id: string;
    original_filename: string;
    mime_type: string;
    size_bytes: number;
    checksum: string;
    status: PlanStatus;
    created_at: string;
    archived_at: string | null;
}

export interface PlanUploadResponse extends Plan {
    is_duplicate: boolean;
}

export type AnalysisStatus = "processing" | "completed" | "failed";

export interface PlanAnalysis {
    id: string;
    plan_id: string;
    status: AnalysisStatus;
    provider: string;
    model: string;
    prompt_version: string;
    result: unknown | null;
    error_message: string | null;
    started_at: string;
    completed_at: string | null;
    created_at: string;
}