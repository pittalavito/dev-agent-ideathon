import { HttpStatusCode } from "axios";
import { apiClient } from "@/api/client/axios";
import { ApiError, handleAxiosError } from "@/api/client/errors";
import { UserOrderRequestDTO, UserOrderResponseDTO, UserOrderErrorResponseDTO } from "./entity.types";

interface UserOrderAPIMethods {
  createUserOrder: (
    userId: string,
    payload: UserOrderRequestDTO,
    notify?: boolean
  ) => Promise<UserOrderResponseDTO>;
}

export const useUserOrderAPI = (): UserOrderAPIMethods => {
  const createUserOrder = async (
    userId: string,
    payload: UserOrderRequestDTO,
    notify: boolean = false
  ): Promise<UserOrderResponseDTO> => {
    try {
      const response = await apiClient.post<UserOrderResponseDTO>(
        "/api/v1/users/${userId}/orders",
        payload,
        {
          params: { notify },
        }
      );

      if (response.status !== HttpStatusCode.Created) {
        throw new ApiError(response.status);
      }

      return response.data;
    } catch (error: unknown) {
      handleAxiosError(error);
    }
  };

  return {
    createUserOrder,
  };
};