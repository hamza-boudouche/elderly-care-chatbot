import React, { useEffect } from 'react';
import NavBar from './components/Navbar';
import Chatbot from './components/Chatbot';
import { HashRouter, Routes, Route } from "react-router-dom";
import history from "./utils/history";
import './style.css';
import initFontAwesome from "./utils/initFontAwesome";
import { useAuth0 } from "@auth0/auth0-react";
import Loading from "./components/Loading"
import Profile from './components/Profile';
import Home from './components/Home';

initFontAwesome();

export default function App() {
  const { isLoading, error } = useAuth0();

  if (error) {
    return <div>Oops... {error.message}</div>;
  }

  if (isLoading) {
    return <Loading />;
  }

  return (
    <HashRouter history={history}>
      <NavBar />
      <Routes>
        <Route path="/" exact element={<Home />} />
        <Route path="/chatbot" exact element={<Chatbot />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </HashRouter>
  );
}
