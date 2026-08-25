export interface PricingLineItem {
  code: string;
  label: string;
  quantity: number;
  unit: string;
  unit_price: number;
  amount: number;
  room_name: string | null;
  category: string | null;
}
  
  export interface PricingResponse {
    lines: PricingLineItem[];
    unpriced_codes: string[];
    subtotal: number;
    currency: string;
  }