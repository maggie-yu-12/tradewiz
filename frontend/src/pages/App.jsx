import React from 'react';
import { Route, Routes } from "react-router-dom";
import { Search } from '../components/Search';
import { Home } from './Home';
import { Individual } from './Individual';

export function App() {
  return (
    <div className="App">
      <Routes>
        {/* TODO: Regex for search/STOCKNAME */}
        <Route path="/" element={<Home />} />
        <Route path="search" element={<Search />} />
        <Route path="stockdata" element={<Individual />} />
      </Routes>
    </div>
  )
}