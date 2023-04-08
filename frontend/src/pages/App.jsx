import React from 'react';
import { Route, Routes } from "react-router-dom";
import { Search } from '../components/Search';
import { Home } from './Home';
import { Individual } from './Individual';
import { Login } from './Login';
import { Register } from './Register';

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