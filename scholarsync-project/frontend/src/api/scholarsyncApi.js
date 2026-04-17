import axios from "axios";
import { API_BASE_URL, API_ENDPOINTS } from "../config/apiConfig";

const api = axios.create({
  baseURL: API_BASE_URL,
});

export async function loginUser(credentials) {
  const response = await api.post(API_ENDPOINTS.LOGIN, credentials);
  return response.data;
}

export async function registerUser(payload) {
  const response = await api.post(API_ENDPOINTS.REGISTER, payload);
  return response.data;
}

export async function fetchStudents(userId, searchTerm = "") {
  const response = await api.get(API_ENDPOINTS.STUDENTS_LIST, {
    params: {
      user_id: userId,
      search: searchTerm,
    },
  });
  return response.data;
}

export async function createStudent(userId, payload) {
  const response = await api.post(API_ENDPOINTS.STUDENT_ADD, payload, {
    params: { user_id: userId },
  });
  return response.data;
}

export async function updateStudent(userId, studentId, payload) {
  const response = await api.put(API_ENDPOINTS.STUDENT_UPDATE(studentId), payload, {
    params: { user_id: userId },
  });
  return response.data;
}

export async function removeStudent(userId, studentId) {
  const response = await api.delete(API_ENDPOINTS.STUDENT_DELETE(studentId), {
    params: { user_id: userId },
  });
  return response.data;
}

export function getApiError(error, fallbackMessage) {
  const responseData = error?.response?.data;
  const message =
    responseData?.error ||
    responseData?.email?.[0] ||
    responseData?.full_name?.[0] ||
    responseData?.password?.[0] ||
    fallbackMessage;

  return Array.isArray(message) ? message[0] : message;
}
