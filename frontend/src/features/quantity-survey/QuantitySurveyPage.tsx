import { useParams, Link } from "react-router-dom";
import { useQuantitySurvey } from "./api";
import { Card, Button } from "../../components/ui";
import { DimensionDivider } from "../../components/ui/DimensionDivider";
import { formatNumber } from "../../lib/format";

export function QuantitySurveyPage() {
  const { planId } = useParams();
  const { data, isLoading, isError } = useQuantitySurvey(planId);

  if (isLoading) return <p className="font-mono text-sm text-ink/60">Calcul du métré…</p>;
  if (isError || !data)
    return (
      <p className="font-mono text-sm text-brick">
        Impossible de charger le métré. L'analyse du plan est-elle terminée ?
      </p>
    );

  return (
    <div className="max-w-4xl">
      <div className="flex items-center justify-between">
        <div>
          <p className="font-mono text-xs uppercase tracking-wider text-forest">Métré</p>
          <h1 className="font-display text-2xl font-semibold">Quantités calculées</h1>
        </div>
        <Link to={`/plans/${planId}/devis`}>
          <Button>Voir le devis chiffré</Button>
        </Link>
      </div>

      <div className="mt-8 grid grid-cols-2 gap-4 md:grid-cols-4">
        <Metric label="Surface habitable" value={`${formatNumber(data.total_floor_area_m2)} m²`} />
        <Metric label="Murs (net)" value={`${formatNumber(data.total_wall_net_area_m2)} m²`} />
        <Metric label="Portes" value={data.total_door_count} />
        <Metric label="Fenêtres" value={data.total_window_count} />
      </div>

      <DimensionDivider label="Pièces" />
      <Card className="overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-paper text-left font-mono text-xs uppercase tracking-wide text-ink/60">
            <tr>
              <th className="px-4 py-3">Pièce</th>
              <th className="px-4 py-3 text-right">Surface</th>
              <th className="px-4 py-3 text-right">Périmètre</th>
              <th className="px-4 py-3 text-right">Peinture (murs)</th>
              <th className="px-4 py-3 text-right">Plinthes</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {data.rooms.map((room) => (
              <tr key={room.name}>
                <td className="px-4 py-3 font-medium">{room.name}</td>
                <td className="px-4 py-3 text-right font-mono">{formatNumber(room.area_m2)} m²</td>
                <td className="px-4 py-3 text-right font-mono">{formatNumber(room.perimeter_m)} m</td>
                <td className="px-4 py-3 text-right font-mono">{formatNumber(room.wall_paint_area_m2)} m²</td>
                <td className="px-4 py-3 text-right font-mono">{formatNumber(room.skirting_length_m)} ml</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>

      {data.stairs.length > 0 && (
        <>
          <DimensionDivider label="Escaliers" />
          <Card className="overflow-hidden">
            <table className="w-full text-sm">
              <tbody className="divide-y divide-line">
                {data.stairs.map((stair, i) => (
                  <tr key={i}>
                    <td className="px-4 py-3">Escalier {i + 1}</td>
                    <td className="px-4 py-3 text-right font-mono">{formatNumber(stair.concrete_volume_m3)} m³ béton</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        </>
      )}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string | number }) {
  return (
    <Card className="px-4 py-3">
      <p className="font-mono text-[11px] uppercase tracking-wider text-ink/50">{label}</p>
      <p className="font-display text-xl font-semibold text-forest-deep">{value}</p>
    </Card>
  );
}