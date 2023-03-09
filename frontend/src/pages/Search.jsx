import React, { useState } from 'react';
import { createSearchParams, useNavigate } from "react-router-dom";
import '../styles/Individual.css';


export function Search() {
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
  // TODO: Code below is a Stackoverflow incorrect snippet of autocomplete

  // const textInput = "hi";
  // useEffect(() => {
  //   const getSymbols = async () => {
  //     const searchURL = `https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=${textInput}&apikey=${process.env.REACT_APP_ALPHA_VANTAGE_API_KEY}`

  //     const res = await axios.get(searchURL);

  //     if (res) {
  //       setSecurity(res.data.bestMatches);
  //       if (security !== undefined && security.length > 0) {
  //         let symbols = security.map(sec => sec['1. symbol'])
  //         setAllSymbol(symbols);
  //       }
  //     }
  //   }

  //   getSymbols();

  // }, [])

  // const inputHandler = (e) => {
  //   setTextInput(e.target.value);

  //   let matches = [];

  //   if (textInput.length > 0) {
  //     matches = allSymbol.filter(sym => {
  //       const regex = new RegExp(`${textInput}`, "gi");
  //       return sym.match(regex);
  //     })
  //     setSuggestion(matches);

  //   }
  //   console.log(suggestion);
  //   setTextInput(e.target.value);
  // }

  // const showData = async (e) => {
  //   e.preventDefault();
  //   const searchURL = `https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=${textInput}&apikey=${process.env.REACT_APP_ALPHA_VANTAGE_API_KEY}`
  //   const monthlyURL = `https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=${textInput}&apikey=${process.env.REACT_APP_ALPHA_VANTAGE_API_KEY}`

  //   try {
  //     const res = await axios.get(searchURL);
  //     const data = await axios.get(monthlyURL);

  //     if (res) {
  //       setTickers(res.data.bestMatches[0]);
  //       setSymbol(res.data.bestMatches[0]['1. symbol']);
  //       setSecurity(res.data.bestMatches);

  //       if (data) {
  //         const monthlyTimeSeries = Object.values(data.data['Monthly Time Series']);
  //         const result = [monthlyTimeSeries[1]];
  //         const resultValues = Object.keys(result[0]).map(key => {
  //           return Math.floor(result[0][key]);
  //         })
  //         setPrices(resultValues);
  //       }
  //     }

  //   } catch (err) {
  //     console.log(err)
  //   }

  //   // setDailyPrices([]);
  //   // setWeeklyPrices([]);
  //   // setIntraPrices([]);
  // }

  return (
    <div className="Search">
      <h1>Search Stock Abbreviation Below</h1>
      <form onSubmit={onSubmitHandler} className="search-form">
        <input type="text" value={searchInput} onChange={inputHandler} placeholder='Enter Stock Symbol (GOOG, MSFT)' />
        <button type="submit">Search</button>
      </form>
    </div>

  )
}