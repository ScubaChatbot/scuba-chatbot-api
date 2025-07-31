import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../contexts/authContext';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const { login, isAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.username || !form.password) {
      setError('Please enter username and password');
      return;
    }
    login(form.username, form.password);
  };

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/chat');
    }
  }, [isAuthenticated, navigate]);

  return (
    <div className="flex items-center justify-center min-h-screen w-full bg-gradient-to-br from-blue-100 via-pink-100 to-yellow-100">
      <div className="bg-white rounded-2xl shadow-2xl p-10 w-full max-w-[50vw] mx-auto flex flex-col gap-8">
        <h2 className="text-3xl font-bold mb-8 text-blue-700 text-center">Login</h2>
        <form onSubmit={handleLogin} className="flex flex-col gap-6">
          <label className="text-sm font-medium text-blue-700" htmlFor="login-username">Username</label>
          <input id="login-username" type="text" placeholder="Username" className="border rounded-2xl px-4 py-5 shadow-md focus:shadow-lg transition" value={form.username} onChange={e => setForm(f => ({ ...f, username: e.target.value }))} required />
          <label className="text-sm font-medium text-blue-700" htmlFor="login-password">Password</label>
          <input id="login-password" type="password" placeholder="Password" className="border rounded-2xl px-4 py-5 shadow-md focus:shadow-lg transition" value={form.password} onChange={e => setForm(f => ({ ...f, password: e.target.value }))} required />
          {error && <span className="text-red-500 text-sm mt-2">{error}</span>}
          <button type="submit" className="bg-blue-700 text-white px-6 py-3 rounded font-semibold hover:bg-blue-800 transition mt-2">Login</button>
      </form>
        <div className="mt-6 text-center">
          <span>Don't have an account? </span>
          <button className="text-blue-700 underline font-semibold" onClick={() => navigate('/register')}>Register</button>
        </div>
      </div>
    </div>
  );
};
export default Login;
