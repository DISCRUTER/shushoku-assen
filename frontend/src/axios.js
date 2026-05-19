import axios from 'axios';
import { useAuthStore } from './stores/auth';

const apiClient = axios.create({
  withCredentials: true,
  xsrfCookieName: 'csrf_access_token',
  xsrfHeaderName: 'X-CSRF-TOKEN',
});

// function getCookie(name) {
//   const value = `; ${document.cookie}`;
//   const parts = value.split(`; ${name}=`);
//   if (parts.length === 2) return parts.pop().split(';').shift();
// }

// apiClient.interceptors.request.use((config) => {
//   const token = getCookie('csrf_access_token');
//   if (token) {
//     config.headers['X-CSRF-TOKEN'] = token;
//   }

//   if (config.noCsrf) {
//     if (config.headers.delete) {
//       config.headers.delete('X-CSRF-TOKEN');
//     } else {
//       delete config.headers['X-CSRF-TOKEN'];
//     }
//   }
//   return config;
// });

apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 419 || error.response?.status === 401) {
      // Clear store and redirect
      const auth = useAuthStore();
      auth.logout();
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export default apiClient;