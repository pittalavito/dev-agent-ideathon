/**
 * =========================================================
 * API TEMPLATE
 * =========================================================
 *
 * THIS FILE IS THE SINGLE SOURCE OF TRUTH
 * FOR ALL API IMPLEMENTATIONS.
 *
 * ANY GENERATED API MUST STRICTLY FOLLOW
 * THIS STRUCTURE.
 *
 * =========================================================
 * REQUIRED RULES
 * =========================================================
 *
 * - Use ONLY axios via apiClient
 * - Never use fetch
 * - Never call axios directly inside components
 * - Always use async/await
 * - Always type request and response DTOs
 * - Always validate response.status
 * - Always use handleAxiosError
 * - Always throw ApiError on invalid status
 * - Always return response.data
 * - Never use any
 * - Never duplicate logic
 * - Keep API methods isolated and reusable
 *
 * =========================================================
 * FILE NAMING CONVENTIONS
 * =========================================================
 *
 * entity.api.ts
 * entity.types.ts
 *
 * =========================================================
 * IMPORTS
 * =========================================================
 */

import { HttpStatusCode } from "axios";

import { apiClient } from "@/api/client/axios";
import { ApiError, handleAxiosError } from "@/api/client/errors";

/**
 * =========================================================
 * DTOs
 * =========================================================
 */

export interface RequestDTO {}

export interface ResponseDTO {}

/**
 * =========================================================
 * API METHODS CONTRACT
 * =========================================================
 */

interface APIMethods {
  methodName: (payload?: RequestDTO) => Promise<ResponseDTO>;
}

/**
 * =========================================================
 * API IMPLEMENTATION
 * =========================================================
 */

export const useExampleAPI = (): APIMethods => {
  /**
   * =====================================================
   * METHOD TEMPLATE
   * =====================================================
   */

  const methodName = async (payload?: RequestDTO): Promise<ResponseDTO> => {
    try {
      /**
       * =================================================
       * AXIOS CALL
       * =================================================
       *
       * Replace:
       * - METHOD
       * - ENDPOINT
       * - REQUEST TYPE
       * - RESPONSE TYPE
       */

      const response = await apiClient.METHOD<ResponseDTO>("ENDPOINT", payload);

      /**
       * =================================================
       * STATUS VALIDATION
       * =================================================
       */

      if (response.status !== HttpStatusCode.Ok) {
        throw new ApiError(response.status);
      }

      /**
       * =================================================
       * RETURN DATA
       * =================================================
       */

      return response.data;
    } catch (error: unknown) {
      /**
       * =================================================
       * ERROR HANDLING
       * =================================================
       */

      handleAxiosError(error);
    }
  };

  /**
   * =====================================================
   * EXPOSE METHODS
   * =====================================================
   */

  return {
    methodName,
  };
};

/**
 * =========================================================
 * EXAMPLES
 * =========================================================
 *
 * GET:
 *
 * apiClient.get<ResponseDTO>(
 *   "/users"
 * );
 *
 * POST:
 *
 * apiClient.post<ResponseDTO>(
 *   "/users",
 *   payload
 * );
 *
 * PUT:
 *
 * apiClient.put<ResponseDTO>(
 *   `/users/${id}`,
 *   payload
 * );
 *
 * PATCH:
 *
 * apiClient.patch<ResponseDTO>(
 *   `/users/${id}`,
 *   payload
 * );
 *
 * DELETE:
 *
 * apiClient.delete<ResponseDTO>(
 *   `/users/${id}`
 * );
 *
 * =========================================================
 * FORBIDDEN PATTERNS
 * =========================================================
 *
 * NEVER:
 *
 * - use fetch
 * - use any
 * - skip typings
 * - skip error handling
 * - skip status validation
 * - call APIs inside components
 * - duplicate axios configuration
 * - create inline axios instances
 *
 * =========================================================
 */
