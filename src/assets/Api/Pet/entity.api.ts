import { HttpStatusCode } from "axios";
import { apiClient } from "@/api/client/axios";
import { ApiError, handleAxiosError } from "@/api/client/errors";
import { RequestDTO, ResponseDTO } from "./pet.types";

interface APIMethods {
  addPet: (payload: RequestDTO) => Promise<ResponseDTO>;
}

export const usePetAPI = (): APIMethods => {
  const addPet = async (payload: RequestDTO): Promise<ResponseDTO> => {
    try {
      const response = await apiClient.put<ResponseDTO>("/pet", payload);
      if (response.status !== HttpStatusCode.Ok) {
        throw new ApiError(response.status);
      }
      return response.data;
    } catch (error: unknown) {
      handleAxiosError(error);
      throw error;
    }
  };

  return {
    addPet,
  };
};