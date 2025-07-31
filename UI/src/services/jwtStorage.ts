// src/services/jwtStorage.ts

export function saveJwtToken(token: string) {
  sessionStorage.setItem('authToken', token);
}

export function readJwtToken(): string | null {
  return sessionStorage.getItem('authToken');
}
