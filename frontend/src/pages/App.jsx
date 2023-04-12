import { React, useEffect } from 'react';
import { Route, Routes, useNavigate } from "react-router-dom";
import { Search } from '../components/Search';
import { Home } from './Home';
import { Individual } from './Individual';
import { Login } from './Login';

export function App() {
  // localStorage.clear();
  const navigate = useNavigate();
  useEffect(() => {
    if (localStorage.getItem("user") === null) {
      navigate('/')
    }
  }, [])
  return (
    <div className="App">
      <Routes>
        {/* TODO: Regex for search/STOCKNAME */}
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="search" element={<Search />} />
        <Route path="stockdata" element={<Individual />} />
        {/* <Route path="register" element={<Register />} /> */}
      </Routes>
    </div>
  )
}