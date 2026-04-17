export const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/api";

export const API_ENDPOINTS = {
  LOGIN: "/auth/login/",
  REGISTER: "/auth/register/",
  STUDENTS_LIST: "/students/",
  STUDENT_ADD: "/students/add/",
  STUDENT_UPDATE: (studentId) => `/students/update/${studentId}/`,
  STUDENT_DELETE: (studentId) => `/students/delete/${studentId}/`,
};
