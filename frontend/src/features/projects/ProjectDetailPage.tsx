import { useParams, Link } from "react-router-dom";
import { useRef } from "react";
import { UploadCloud } from "lucide-react";
import { Button, Card, StatusPill } from "../../components/ui";
import { DimensionDivider } from "../../components/ui/DimensionDivider";
import { useAnalysePlan, usePlanAnalyses, usePlans, useProject, useUploadPlan } from "./api";
import type { Plan } from "./types";

export function ProjectDetailPage() {
  const { projectId } = useParams();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { data: project } = useProject(projectId);
  const { data: plans, isLoading, isError } = usePlans(projectId);
  const uploadPlan = useUploadPlan(projectId);

  return (
    <div className="max-w-3xl">
      <p className="font-mono text-xs uppercase tracking-wider text-forest">Projet</p>
      <h1 className="font-display text-2xl font-semibold">{project?.name ?? "…"}</h1>

      <Card className="mt-6 border-dashed px-6 py-8 text-center">
        <UploadCloud className="mx-auto h-6 w-6 text-forest" />
        <p className="mt-2 text-sm text-ink/70">Dépose un plan (PDF, PNG, JPG)</p>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.png,.jpg,.jpeg,.tiff"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) uploadPlan.mutate(file);
            e.target.value = "";
          }}
        />
        <Button variant="secondary" className="mt-4" onClick={() => fileInputRef.current?.click()} disabled={uploadPlan.isPending}>
          {uploadPlan.isPending ? "Envoi…" : "Choisir un fichier"}
        </Button>
        {uploadPlan.isError && <p className="mt-2 font-mono text-xs text-brick">Échec de l'envoi — vérifie le format du fichier.</p>}
      </Card>

      <DimensionDivider label="Plans" />

      {isLoading && <p className="font-mono text-sm text-ink/60">Chargement…</p>}
      {isError && <p className="font-mono text-sm text-brick">Impossible de charger les plans.</p>}

      {plans && plans.length === 0 && (
        <Card className="px-6 py-12 text-center">
          <p className="text-sm text-ink/60">Aucun plan encore déposé.</p>
        </Card>
      )}

      {plans && plans.length > 0 && (
        <Card className="divide-y divide-line">
          {plans.map((plan) => (
            <PlanRow key={plan.id} projectId={projectId!} plan={plan} />
          ))}
        </Card>
      )}
    </div>
  );
}

function PlanRow({ projectId, plan }: { projectId: string; plan: Plan }) {
  const { data: analyses, isLoading } = usePlanAnalyses(projectId, plan.id);
  const analysePlan = useAnalysePlan(projectId);

  const latest =
    analyses && analyses.length > 0
      ? [...analyses].sort((a, b) => b.created_at.localeCompare(a.created_at))[0]
      : undefined;

  return (
    <div className="flex items-center justify-between px-4 py-3 text-sm">
      <span className="font-medium">{plan.original_filename}</span>
      <div className="flex items-center gap-3">
        {isLoading && <span className="font-mono text-xs text-ink/40">…</span>}

        {!isLoading && !latest && (
          <Button variant="secondary" onClick={() => analysePlan.mutate(plan.id)} disabled={analysePlan.isPending}>
            {analysePlan.isPending ? "Analyse en cours…" : "Lancer l'analyse"}
          </Button>
        )}

        {latest && <StatusPill status={latest.status} />}

        {latest?.status === "failed" && (
          <Button variant="ghost" onClick={() => analysePlan.mutate(plan.id)} disabled={analysePlan.isPending}>
            Réessayer
          </Button>
        )}

        {latest?.status === "completed" && (
          <>
            <Link to={`/plans/${plan.id}/metre`} className="font-mono text-xs text-forest hover:underline">
              Métré →
            </Link>
            <Link to={`/plans/${plan.id}/devis`} className="font-mono text-xs text-forest hover:underline">
              Devis →
            </Link>
          </>
        )}
      </div>
    </div>
  );
}