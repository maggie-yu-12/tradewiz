import axios from 'axios';
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
  const [stockData, setStockData] = useState({
    name: 'Loading...',
    description: 'Loading...',
    symbol: 'Loading...',
    quote: 'Loading...',
  });

  axios.defaults.baseURL = 'http://localhost:8000';
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
      method: 'GET',
      url: window.location.pathname,
      params: { symbol: searchParams.get('symbol') },
    })
      .then(function (response) {
        const res = response.data
        setStockData(({
          name: res.stock_overview.Name,
          description: res.stock_overview.Description,
          symbol: res.stock_overview.Symbol,
          quote: res.stock_quote['Global Quote']['05. price']
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
    <div class='Individual'>
      <header class='Individual-header'>

        <img src={logo} class='Individual-logo' alt='logo' />

        <Search></Search>

      </header>

      <body>
        <div class='Stock-data-frame'>
          <h3 id='Stock-name'>{stockData.name} ({stockData.symbol})</h3>
          <div id='Stock-description'>{stockData.description}</div>
          <br></br>
          <h3 id='Stock-quote'>NASDAQ: {stockData.quote} (Other params here)</h3>
        </div>

        <br></br>

        <div class='Sentiment-score-frame'>
          <div class='Sentiment-score-frame-component' id='Twitter-component'>
            <div class='Sentiment-score-frame-component-name'>Twitter</div>
            <div class='Sentiment-score-frame-component-score'>10.0</div>
          </div>
          <div class='Sentiment-score-frame-component' id='Reddit-component'>
            <div class='Sentiment-score-frame-component-name'>Reddit</div>
            <div class='Sentiment-score-frame-component-score'>10.0</div>
          </div>
          <div class='Sentiment-score-frame-component' id='Bloomberg-component'>
            <div class='Sentiment-score-frame-component-name'>Bloomberg</div>
            <div class='Sentiment-score-frame-component-score'>10.0</div>
          </div>
          <div class='Sentiment-score-frame-component' id='Overall-component'>
            <div class='Sentiment-score-frame-component-name'>Overall</div>
            <div class='Sentiment-score-frame-component-score'>10.0</div>
          </div>
        </div>

        <br></br>

        <div class='Graph-frame'>
          <div class='Graph-component'>
            Graph
          </div>
        </div>

        <br></br>

        <div class='Comments-frame'>
          <div class='Comments-frame-child'>Trending on...</div>
          <div class='Comments-frame-child'>Comments</div>
        </div>
      </body>
    </div>
  );
}
