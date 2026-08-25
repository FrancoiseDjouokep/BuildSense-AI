export interface RoomQuantity {
    name: string;
    area_m2: number;
    perimeter_m: number;
    wall_paint_area_m2: number;
    skirting_length_m: number;
  }
  
  export interface WallQuantity {
    gross_area_m2: number;
    opening_area_m2: number;
    net_area_m2: number;
    net_volume_m3: number;
    door_count: number;
    door_area_m2: number;
    window_count: number;
    window_area_m2: number;
  }
  
  export interface StairQuantity {
    concrete_volume_m3: number;
  }
  
  export interface BillOfQuantityItem {
    code: string;
    label: string;
    quantity: number;
    unit: "m2" | "m3" | "ml" | "unite" | "forfait";
    room_name: string | null;
  }
  
  export interface QuantitySurveyResponse {
    rooms: RoomQuantity[];
    walls: WallQuantity[];
    stairs: StairQuantity[];
    total_floor_area_m2: number;
    total_wall_net_area_m2: number;
    total_wall_net_volume_m3: number;
    total_stair_concrete_volume_m3: number;
    total_door_count: number;
    total_window_count: number;
    items: BillOfQuantityItem[];
  }