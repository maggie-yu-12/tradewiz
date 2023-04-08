import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useLocation, useSearchParams } from 'react-router-dom';
import { NavBar } from '../components/NavBar';
import { News } from '../components/News';
import { Search } from '../components/Search';

import '../styles/Individual.css';

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
    price: 'Loading...',
    news: 'Loading...',
    price_momentum: 'Loading...',
    price_change_percent: 'Loading...',
    trade_volume: 'Loading...',
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
          price: res.stock_quote['Global Quote']['05. price'],
          news: res.stock_news,
          price_momentum: res.stock_quote['Global Quote']['09. change'],
          price_change_percent: res.stock_quote['Global Quote']['10. change percent'],
          trade_volume: res.stock_quote['Global Quote']['06. volume'],
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
    <div class='Individual-outer-container'>
      <NavBar />
      <br></br>
      <Search />
      <br></br>
      <br></br>
      <h3 id='Stock-name'>{stockData.name} ({stockData.symbol})</h3>
      <div id='Stock-description'>{stockData.description}</div>

      <br></br>

      <div class='Stock-data-frame'>
        <div class='Stock-data-border'>
          <div class='Stock-data-frame-component' id='Twitter-component'>
            <div class='Stock-data-frame-component-name'>Total Sentiment Score</div>
            <div class='Stock-data-frame-component-score'>TODO</div>
            <br></br>
            <div class='Stock-data-company-header'>Twitter Score</div>
            <div class='Stock-data-company-score'>TODO</div>
            <div class='Stock-data-company-header'>Reddit Score</div>
            <div class='Stock-data-company-score'>TODO</div>
            <div class='Stock-data-company-header'>Bloomberg Score</div>
            <div class='Stock-data-company-score'>TODO</div>
            <br></br>
          </div>
          <div class='Stock-data-frame-component' id='Reddit-component'>
            <div class='Stock-data-frame-component-name'>Total Activity</div>
            <div class='Stock-data-frame-component-score'>TODO</div>
            <br></br>
            <div class='Stock-data-company-header'>Twitter Activity</div>
            <div class='Stock-data-company-score'>TODO</div>
            <div class='Stock-data-company-header'>Reddit Activity</div>
            <div class='Stock-data-company-score'>TODO</div>
            <div class='Stock-data-company-header'>Bloomberg Activity</div>
            <div class='Stock-data-company-score'>TODO</div>
            <br></br>
          </div>
          <div class='Stock-data-frame-component' id='Bloomberg-component'>
            <div class='Stock-data-frame-component-name'>Last Price</div>
            <div class='Stock-data-frame-component-score'>{stockData.price}</div>
            <br></br>
            <div class='Stock-data-company-header'>Price Momentum</div>
            <div class='Stock-data-company-score'>{stockData.price_momentum}</div>
            <div class='Stock-data-company-header'>Price Change %</div>
            <div class='Stock-data-company-score'>{stockData.price_change_percent}</div>
            <div class='Stock-data-company-header'>Trade Volume</div>
            <div class='Stock-data-company-score'>{stockData.trade_volume}</div>
            <br></br>
          </div>
        </div>
      </div>


      <br></br>

      <div class='Graph-frame'>
        <div class='Graph-component'>
          Graph
        </div>
      </div>

      <br></br>

      <div class='News-frame'>
        <div class='News-frame-header'>News Aggregation</div>
        <div class='News-frame-comments'>
          <News site='Twitter' />
          <News site='Reddit' />
          <News site='Bloomberg' />
        </div>
      </div>

      <br></br>

      <div class='Comments-frame'>
        <div class='Comments-frame-header'>Comment Aggregation</div>
        <div class='Comments-frame-comments'>Comments</div>
      </div>
    </div>
  );
}
