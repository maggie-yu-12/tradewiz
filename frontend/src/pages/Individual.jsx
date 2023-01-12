import axios from "axios";
import React, { useEffect, useState } from 'react';
import { useLocation, useSearchParams } from 'react-router-dom';
import { Search } from './Search';

import '../styles/Individual.css';
import logo from '../tradewiz-logo.png';

export function Individual() {

  // new line start
  // TODO: Get stock abbreviation from search enter.

  // search result as a stock abbreviation
  const stockAbbreviation = useLocation();
  const [searchParams] = useSearchParams();

  console.log(searchParams.get('symbol'))
  const [profileData, setProfileData] = useState(null)
  const [stockData, setStockData] = useState({
    name: "hi",
    description: "ho",
    symbol: "he",
  });
  axios.defaults.baseURL = "http://localhost:8000";
  axios.interceptors.request.use(request => {
    console.log('Starting Request', JSON.stringify(request, null, 2))
    return request
  })
  axios.interceptors.response.use(response => {
    console.log('Response:', JSON.stringify(response, null, 2))
    return response
  })

  function getStockData() {
    console.log(window.location.pathname)
    axios({
      method: "GET",
      url: window.location.pathname,
      params: { symbol: searchParams.get('symbol') },
    })
      .then(function (response) {
        const res = response.data
        setStockData(({
          name: res.Name,
          description: res.Description,
          symbol: res.Symbol,
        }))
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  // Get stock information from Alpha Vantage API, third line makes it update with search query
  useEffect(() => {
    getStockData();
  }, [searchParams]);

  //end of new line 

  return (
    <div className="Individual">
      <header className="Individual-header">

        <img src={logo} className="Individual-logo" alt="logo" />

        <Search></Search>

      </header>

      <body>
        <div class="Stock-data-frame">
          <h3 id="Stock-name">{stockData.name} ({stockData.symbol})</h3>
          <div id="Stock-description">{stockData.description}</div>
        </div>

        <p>NASDAQ # # #</p>
        <div className="Sentiment-score-frame">
          Twitter Reddit Bloomberg Overall
        </div>

        <div className="Graph">
          Graph
        </div>

        <br></br>

        <div className="Comments-frame">
          <div className="Comments-frame-child">Trending on...</div>
          <div className="Comments-frame-child">Comments</div>
        </div>
        {/* new line start*/}
        {/* <p>To get your profile details: </p><button onClick={getData}>Click me</button>
        {profileData && <div>
          <p>Profile name: {profileData.profile_name}</p>
          <p>About me this is: {profileData.about_me}</p>
        </div>
        } */}
        {/* end of new line */}
      </body>
    </div>
  );
}
