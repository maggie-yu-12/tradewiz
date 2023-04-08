import React from 'react';
import { Route, Routes } from "react-router-dom";
import Home from './Home';
import { Individual } from './Individual';
import { Login } from './Login';
import { Register } from './Register';
import { Search } from './Search';

export function App() {
  return (
    <div className="App">
      <Routes>
        {/* TODO: Regex for search/STOCKNAME */}
        <Route path="/" element={<Home />} />
        <Route path="search" element={<Search />} />
        <Route path="stockdata" element={<Individual />} />
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
      </Routes>
    </div>
  )
}