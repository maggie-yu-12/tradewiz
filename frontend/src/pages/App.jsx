import React from 'react';
import { Route, Routes } from "react-router-dom";
import { Home } from "./Home";
import { Individual } from './Individual';

export function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="MSFT" element={<Individual />} />
      </Routes>
    </div>
  )
}