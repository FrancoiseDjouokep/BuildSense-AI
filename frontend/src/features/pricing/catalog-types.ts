export interface UnitPrice {
    id: string;
    code: string;
    label: string;
    unit: "m2" | "m3" | "ml" | "unite" | "forfait";
    unit_price: number;
    currency: string;
    category: string | null;
    is_fixed_line: boolean;
  }
  
  export interface UnitPriceCreateInput {
    code: string;
    label: string;
    unit: "m2" | "m3" | "ml" | "unite" | "forfait";
    unit_price: number;
    currency?: string;
    category?: string;
    is_fixed_line?: boolean;
  }
  
  export interface UnitPriceUpdateInput {
    label?: string;
    unit_price?: number;
    currency?: string;
  }