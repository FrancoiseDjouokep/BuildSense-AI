import { useState } from "react";
import { useForm } from "react-hook-form";
import { Plus, Trash2 } from "lucide-react";
import { Button, Card } from "../../components/ui";
import { DimensionDivider } from "../../components/ui/DimensionDivider";
import { useCreateUnitPrice, useDeleteUnitPrice, useUnitPrices, useUpdateUnitPrice } from "./catalog-api";
import type { UnitPrice, UnitPriceCreateInput } from "./catalog-types";

const UNITS = ["m2", "m3", "ml", "unite", "forfait"] as const;

export function PriceCatalogPage() {
    const { data: prices, isLoading, isError } = useUnitPrices();
    const [showForm, setShowForm] = useState(false);
    const createUnitPrice = useCreateUnitPrice();
    const { register, handleSubmit, reset } = useForm<UnitPriceCreateInput>({
        defaultValues: { unit: "m2", currency: "XAF" },
    });

    const onCreate = (values: UnitPriceCreateInput) => {
        createUnitPrice.mutate(
            { ...values, unit_price: Number(values.unit_price) },
            { onSuccess: () => { reset(); setShowForm(false); } }
        );
    };

    return (
        <div className="max-w-3xl">
            <div className="flex items-center justify-between">
                <div>
                    <p className="font-mono text-xs uppercase tracking-wider text-forest">Catalogue</p>
                    <h1 className="font-display text-2xl font-semibold">Vos prix unitaires</h1>
                </div>
                <Button onClick={() => setShowForm((v) => !v)}>
                    <Plus className="h-4 w-4" /> Nouveau tarif
                </Button>
            </div>

            <p className="mt-2 text-sm text-ink/60">
                Ces prix servent à chiffrer automatiquement les devis. Modifie-les à tout moment — le changement
                s'applique aux prochains devis générés.
            </p>

            {showForm && (
                <Card className="mt-4 p-4">
                    <form onSubmit={handleSubmit(onCreate)} className="grid grid-cols-2 gap-3">
                        <div>
                            <label className="font-mono text-xs uppercase tracking-wide text-ink/60">Code</label>
                            <input
                                {...register("code", { required: true })}
                                className="mt-1 w-full rounded-sm border border-line px-3 py-2 text-sm font-mono outline-none focus:border-forest"
                                placeholder="SOL-CARRELAGE"
                            />
                        </div>
                        <div>
                            <label className="font-mono text-xs uppercase tracking-wide text-ink/60">Désignation</label>
                            <input
                                {...register("label", { required: true })}
                                className="mt-1 w-full rounded-sm border border-line px-3 py-2 text-sm outline-none focus:border-forest"
                                placeholder="Carrelage grès cérame"
                            />
                        </div>
                        <div>
                            <label className="font-mono text-xs uppercase tracking-wide text-ink/60">Unité</label>
                            <select
                                {...register("unit", { required: true })}
                                className="mt-1 w-full rounded-sm border border-line px-3 py-2 text-sm outline-none focus:border-forest"
                            >
                                {UNITS.map((u) => (
                                    <option key={u} value={u}>{u}</option>
                                ))}
                            </select>
                        </div>
                        <div>
                            <label className="font-mono text-xs uppercase tracking-wide text-ink/60">Prix unitaire (XAF)</label>
                            <input
                                type="number"
                                step="0.01"
                                {...register("unit_price", { required: true, valueAsNumber: true, min: 0 })}
                                className="mt-1 w-full rounded-sm border border-line px-3 py-2 text-sm font-mono outline-none focus:border-forest"
                                placeholder="8000"
                            />
                        </div>
                        <div className="col-span-2 flex justify-end">
                            <Button type="submit" disabled={createUnitPrice.isPending}>
                                {createUnitPrice.isPending ? "Ajout…" : "Ajouter au catalogue"}
                            </Button>
                        </div>
                    </form>
                </Card>
            )}

            <DimensionDivider />

            {isLoading && <p className="font-mono text-sm text-ink/60">Chargement…</p>}
            {isError && <p className="font-mono text-sm text-brick">Impossible de charger le catalogue.</p>}

            {prices && prices.length > 0 && (
                <Card className="overflow-hidden">
                    <table className="w-full text-sm">
                        <thead className="bg-paper text-left font-mono text-xs uppercase tracking-wide text-ink/60">
                            <tr>
                                <th className="px-4 py-3">Code</th>
                                <th className="px-4 py-3">Désignation</th>
                                <th className="px-4 py-3">Unité</th>
                                <th className="px-4 py-3">Catégorie</th>
                                <th className="px-4 py-3 text-right">Prix unitaire</th>
                                <th className="px-4 py-3" />
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-line">
                            {prices.map((price) => (
                                <PriceRow key={price.id} price={price} />
                            ))}
                        </tbody>
                    </table>
                </Card>
            )}
        </div>
    );
}

function PriceRow({ price }: { price: UnitPrice }) {
    const [value, setValue] = useState(String(price.unit_price));
    const updateUnitPrice = useUpdateUnitPrice();
    const deleteUnitPrice = useDeleteUnitPrice();

    const commit = () => {
        const parsed = Number(value);
        if (!Number.isNaN(parsed) && parsed !== price.unit_price) {
            updateUnitPrice.mutate({ id: price.id, unit_price: parsed });
        }
    };

    return (
        <tr>
            <td className="px-4 py-3 font-mono text-xs">{price.code}</td>
            <td className="px-4 py-3">{price.label}</td>
            <td className="px-4 py-3 font-mono text-xs text-ink/60">{price.unit}</td>
            <td className="px-4 py-3 text-xs text-ink/50">{price.category ?? "—"}</td>
            <td className="px-4 py-3 text-right">
                <input
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                    onBlur={commit}
                    onKeyDown={(e) => e.key === "Enter" && (e.currentTarget as HTMLInputElement).blur()}
                    className="w-28 rounded-sm border border-line px-2 py-1 text-right font-mono text-sm outline-none focus:border-forest"
                />
            </td>
            <td className="px-4 py-3 text-right">
                <button onClick={() => deleteUnitPrice.mutate(price.id)} className="text-ink/30 hover:text-brick" aria-label="Supprimer">
                    <Trash2 className="h-4 w-4" />
                </button>
            </td>
        </tr>
    );
}