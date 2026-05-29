import { HttpStatusCode } from "axios";

export interface UserOrderRequestDTO {
  product_id: string;
  quantity: number;
  note: string;
}

export interface UserOrderResponseDTO {
  order_id: string;
  user_id: string;
  product_id: string;
  quantity: number;
  status: string;
  created_at: string;
}

export interface UserOrderErrorResponseDTO {
  error: string;
  details: string;
}