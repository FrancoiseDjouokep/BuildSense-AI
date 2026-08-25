import { useState } from "react";
import { Link } from "react-router-dom";
import { useForm } from "react-hook-form";
import { Plus } from "lucide-react";
import { Button, Card } from "../../components/ui";
import { DimensionDivider } from "../../components/ui/DimensionDivider";
import { useCreateProject, useProjects } from "./api";
import type { ProjectCreateInput } from "./types";

export function ProjectsListPage() {
  const [showForm, setShowForm] = useState(false);
  const { data: projects, isLoading, isError } = useProjects();
  const { register, handleSubmit, reset } = useForm<ProjectCreateInput>();
  const createProject = useCreateProject();

  const onSubmit = (values: ProjectCreateInput) => {
    createProject.mutate(values, {
      onSuccess: () => {
        reset();
        setShowForm(false);
      },
    });
  };

  return (
    <div className="max-w-3xl">
      <div className="flex items-center justify-between">
        <div>
          <p className="font-mono text-xs uppercase tracking-wider text-forest">Projets</p>
          <h1 className="font-display text-2xl font-semibold">Vos projets</h1>
        </div>
        <Button onClick={() => setShowForm((v) => !v)}>
          <Plus className="h-4 w-4" /> Nouveau projet
        </Button>
      </div>

      {showForm && (
        <Card className="mt-4 p-4">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
            <div>
              <label className="font-mono text-xs uppercase tracking-wide text-ink/60">Nom du projet</label>
              <input
                {...register("name", { required: true, minLength: 3 })}
                className="mt-1 w-full rounded-sm border border-line px-3 py-2 text-sm outline-none focus:border-forest"
                placeholder="Villa Bonamoussadi"
              />
            </div>
            <div>
              <label className="font-mono text-xs uppercase tracking-wide text-ink/60">Description (optionnel)</label>
              <input
                {...register("description")}
                className="mt-1 w-full rounded-sm border border-line px-3 py-2 text-sm outline-none focus:border-forest"
                placeholder="Villa R+1, 4 chambres"
              />
            </div>
            <div className="flex justify-end">
              <Button type="submit" disabled={createProject.isPending}>
                {createProject.isPending ? "Création…" : "Créer"}
              </Button>
            </div>
          </form>
        </Card>
      )}

      <DimensionDivider />

      {isLoading && <p className="font-mono text-sm text-ink/60">Chargement…</p>}
      {isError && <p className="font-mono text-sm text-brick">Impossible de charger les projets.</p>}

      {projects && projects.length === 0 && (
        <Card className="px-6 py-12 text-center">
          <p className="text-sm text-ink/60">Aucun projet pour l'instant. Créez-en un pour commencer.</p>
        </Card>
      )}

      {projects && projects.length > 0 && (
        <Card className="divide-y divide-line">
          {projects.map((project) => (
            <Link
              key={project.id}
              to={`/projects/${project.id}`}
              className="flex items-center justify-between px-4 py-3 text-sm hover:bg-paper"
            >
              <div>
                <span className="font-medium">{project.name}</span>
                {project.description && <p className="text-xs text-ink/50">{project.description}</p>}
              </div>
              <span className="font-mono text-xs text-ink/40">Ouvrir →</span>
            </Link>
          ))}
        </Card>
      )}
    </div>
  );
}