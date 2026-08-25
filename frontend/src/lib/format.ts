export function formatNumber(value: number, options?: Intl.NumberFormatOptions) {
    return new Intl.NumberFormat("fr-FR", options).format(value);
  }
  
  export function formatCurrency(value: number, currency = "XAF") {
    return new Intl.NumberFormat("fr-FR", {
      style: "currency",
      currency,
      maximumFractionDigits: 0,
    }).format(value);
  }