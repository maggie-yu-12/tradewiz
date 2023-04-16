import React, { useState } from 'react';
import { BiSearchAlt } from 'react-icons/bi';
import { createSearchParams, useNavigate } from "react-router-dom";
// import '../styles/Search.css';

/**
 * Component for greeting message and search on Home Page.
 */
export const SearchNavBar = () => {
  const navigate = useNavigate();
  const [searchInput, setSearchInput] = useState("");
  // const [searchParams, setSearchParams] = useSearchParams();

  const inputHandler = (e) => {
    e.preventDefault();
    setSearchInput(e.target.value);
  };

  onSubmitHandler = (e) => {
    e.preventDefault();
    navigate({
      pathname: '/stockdata',
      search: createSearchParams({
        symbol: searchInput,
      }).toString()
    });
  }

  return (

    <div class="search-nav-bar-frame">

      <form onSubmit={onSubmitHandler} class="search-form">
        <div className="search-nav-bar">
          <input id="home-search-input" class="text" value={searchInput} onChange={inputHandler} placeholder='Enter Stock Symbol (AAPL, MSFT)' />
          <button id="home-search-button" class="submit">
            <BiSearchAlt fontSize={22} />
          </button>
        </div>
      </form>
    </div>
  )
}
