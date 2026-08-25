import { useParams } from "react-router-dom";
import { useDevis } from "./api";
import { Card } from "../../components/ui";
import { DimensionDivider } from "../../components/ui/DimensionDivider";
import { formatCurrency, formatNumber } from "../../lib/format";
import type { PricingLineItem } from "./types";

export function DevisPage() {
  const { planId } = useParams();
  const { data, isLoading, isError } = useDevis(planId);

  if (isLoading) return <p className="font-mono text-sm text-ink/60">Génération du devis…</p>;
  if (isError || !data)
    return <p className="font-mono text-sm text-brick">Impossible de générer le devis pour ce plan.</p>;

  const groups = groupByCategory(data.lines);

  return (
    <div className="max-w-4xl">
      <p className="font-mono text-xs uppercase tracking-wider text-forest">Devis estimatif</p>
      <h1 className="font-display text-2xl font-semibold">Devis quantitatif et estimatif</h1>

      {groups.map(([category, lines]) => (
        <div key={category}>
          <DimensionDivider label={category} />
          <Card className="overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-paper text-left font-mono text-xs uppercase tracking-wide text-ink/60">
                <tr>
                  <th className="px-4 py-3">Désignation</th>
                  <th className="px-4 py-3">Localisation</th>
                  <th className="px-4 py-3 text-right">Quantité</th>
                  <th className="px-4 py-3 text-right">P.U.</th>
                  <th className="px-4 py-3 text-right">Montant</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line">
                {lines.map((line) => (
                  <tr key={`${line.code}-${line.room_name ?? "global"}`}>
                    <td className="px-4 py-3">{line.label}</td>
                    <td className="px-4 py-3 text-ink/60">{line.room_name ?? "—"}</td>
                    <td className="px-4 py-3 text-right font-mono">
                      {formatNumber(line.quantity)} {line.unit}
                    </td>
                    <td className="px-4 py-3 text-right font-mono">{formatCurrency(line.unit_price, data.currency)}</td>
                    <td className="px-4 py-3 text-right font-mono font-medium">
                      {formatCurrency(line.amount, data.currency)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        </div>
      ))}

      <Card className="mt-4 bg-paper px-4 py-4">
        <div className="flex justify-between">
          <span className="font-display font-semibold">Total estimatif (HT)</span>
          <span className="font-display text-lg font-semibold text-forest-deep">
            {formatCurrency(data.subtotal, data.currency)}
          </span>
        </div>
      </Card>

      {data.unpriced_codes.length > 0 && (
        <Card className="mt-4 border-amber/40 bg-amber/5 px-4 py-3">
          <p className="font-mono text-xs uppercase tracking-wide text-amber">Ouvrages sans prix ou unité incohérente</p>
          <p className="mt-1 text-sm text-ink/70">{data.unpriced_codes.join(", ")}</p>
        </Card>
      )}

      <p className="mt-6 font-mono text-xs text-ink/40">
        TVA non incluse. Devis généré automatiquement, à valider par un métreur.
      </p>
    </div>
  );
}

function groupByCategory(lines: PricingLineItem[]): [string, PricingLineItem[]][] {
  const map = new Map<string, PricingLineItem[]>();
  for (const line of lines) {
    const key = line.category ?? "Autres";
    if (!map.has(key)) map.set(key, []);
    map.get(key)!.push(line);
  }
  return [...map.entries()].sort(([a], [b]) => a.localeCompare(b));
}