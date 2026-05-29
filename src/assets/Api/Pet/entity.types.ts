import { HttpStatusCode } from "axios";

export interface Pet {
  id: number;
  name: string;
  age: number;
  type: string;
}

export interface RequestDTO {
  Pet: Pet;
}

export interface ResponseDTO {
  Pet: Pet;
}