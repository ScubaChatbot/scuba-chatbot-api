// src/services/authApi.ts
import { saveJwtToken } from './jwtStorage';

export async function loginApi(username: string, password: string): Promise<{ token: string }> {
  // Simulate API call and JWT response
  return new Promise(resolve => {
    setTimeout(() => {
      const token = 'mock-jwt-token-for-' + username;
      saveJwtToken(token);
      resolve({ token });
    }, 500);
  });
}

export async function registerApi(username: string, password: string): Promise<{ ok: boolean }> {
  // Simulate API call and registration response
  return new Promise(resolve => {
    setTimeout(() => {
      resolve({ ok: true });
    }, 500);
  });
}
