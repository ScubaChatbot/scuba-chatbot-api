import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Chat from './pages/Chat';
import './App.css';

function App() {
  return (
    <Router>
      <header className="bg-gradient-to-r from-blue-700 to-purple-700 text-white px-8 h-24 flex items-center justify-center shadow-lg">
        <div className="w-full flex justify-center">
          <span className="font-extrabold text-7xl tracking-wide text-center">Dive Tours Chat</span>
        </div>
      </header>
      <main className="pt-12 min-h-[calc(100vh-5rem)] w-full flex justify-center items-center bg-gradient-to-br from-blue-50 to-purple-100">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
