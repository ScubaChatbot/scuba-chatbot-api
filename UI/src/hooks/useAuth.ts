import { useState } from 'react';
import { loginApi, registerApi } from '../services/authApi';

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  function login(username: string, password: string) {
    loginApi(username, password).then(({ token }) => {
      if (token) {
        setIsAuthenticated(true);
      }
    });
  }

  function register(username: string, password: string) {
    registerApi(username, password).then(({ ok }) => {
      // You can add post-registration actions here
    });
  }

  function logout() {
    setIsAuthenticated(false);
    return true;
  }

  return { isAuthenticated, login, logout, register };
}