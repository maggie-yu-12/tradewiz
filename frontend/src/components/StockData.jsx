import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Link } from "react-router-dom";

import '../styles/Individual.css';

export const StockData = ({ company, companyData }) => {
  const [stockDataOverview, setStockDataOverview] = useState({
    name: 'Loading...',
    description: 'Loading...',
    symbol: 'Loading...',
    price: 'Loading...',
    price_momentum: 'Loading...',
    price_change_percent: 'Loading...',
    trade_volume: 'Loading...',
  })
  const [stockDataScore, setStockDataScore] = useState({
    total_score: 'Loading...',
    twitter_score: 'Loading...',
    reddit_score: 'Loading...',
  });

  const [stockDataActivity, setStockDataActivity] = useState({
    total_activity: 'Loading...',
    twitter_activity: 'Loading...',
    reddit_activity: 'Loading...',
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

  function getStockDataOverview() {
    console.log(window.location.pathname)
    axios({
      method: 'GET',
      url: '/stockdataoverview',
      params: { symbol: company },
    })
      .then(function (response) {
        const res = response.data
        setStockDataOverview(({
          name: res.stock_overview.Name,
          description: res.stock_overview.Description,
          symbol: res.stock_overview.Symbol,
          price: res.stock_quote['Global Quote']['05. price'],
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

  function getStockDataScore() {
    axios({
      method: 'GET',
      url: '/stockdatascore',
      params: { symbol: company },
    })
      .then(function (response) {
        const res = response.data
        setStockDataScore(({
          total_score: res.total_score,
          twitter_score: res.twitter_score,
          reddit_score: res.reddit_score,
        }))
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  function getStockDataActivity() {
    axios({
      method: 'GET',
      url: '/stockdataactivity',
      params: { symbol: company },
    })
      .then(function (response) {
        const res = response.data
        setStockDataActivity(({
          total_activity: res.total_activity,
          twitter_activity: res.twitter_activity,
          reddit_activity: res.reddit_activity,
        }))
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  // Get stock information from Alpha Vantage API, third line makes it update with search query
  useEffect(() => {
    getStockDataOverview();
    getStockDataScore();
    getStockDataActivity();
    // getStockGraph();
  }, [company]);

  //end of new line 

  return (
    <div class='stock-data'>
      <Link to={"/stockdata?symbol=" + JSON.parse(companyData).Company.substring(1)}>
        <p id="favorite-stock-name">{stockDataOverview.name}&nbsp;({JSON.parse(companyData).Company})</p>
      </Link>


      <div class='Stock-data-frame'>
        <div class='Stock-data-border'>
          <div class='Stock-data-frame-component'>
            <div class='Stock-data-frame-component-name'>Total Sentiment Score</div>
            <div class='Stock-data-frame-component-score'>{stockDataScore.total_score}</div>
            <br></br>
            <div class='Stock-data-company-header'>Twitter Score</div>
            <div class='Stock-data-company-score'>{stockDataScore.twitter_score}</div>
            <div class='Stock-data-company-header'>Reddit Score</div>
            <div class='Stock-data-company-score'>{stockDataScore.reddit_score}</div>
            {/* <div class='Stock-data-company-header'>Bloomberg Score</div>
              <div class='Stock-data-company-score'>TODO</div> */}
            <br></br>
          </div>
          <div class='Stock-data-frame-component'>
            <div class='Stock-data-frame-component-name'>Total Activity</div>
            <div class='Stock-data-frame-component-score'>{stockDataActivity.total_activity}</div>
            <br></br>
            <div class='Stock-data-company-header'>Twitter Activity</div>
            <div class='Stock-data-company-score'>{stockDataActivity.twitter_activity}</div>
            <div class='Stock-data-company-header'>Reddit Activity</div>
            <div class='Stock-data-company-score'>{stockDataActivity.reddit_activity}</div>
            {/* <div class='Stock-data-company-header'>Bloomberg Activity</div>
              <div class='Stock-data-company-score'>TODO</div> */}
            <br></br>
          </div>
          <div class='Stock-data-frame-component'>
            <div class='Stock-data-frame-component-name'>Last Price</div>
            <div class='Stock-data-frame-component-score'>{stockDataOverview.price}</div>
            <br></br>
            <div class='Stock-data-company-header'>Price Momentum</div>
            <div class='Stock-data-company-score'>{stockDataOverview.price_momentum}</div>
            <div class='Stock-data-company-header'>Price Change %</div>
            <div class='Stock-data-company-score'>{stockDataOverview.price_change_percent}</div>
            <div class='Stock-data-company-header'>Trade Volume</div>
            <div class='Stock-data-company-score'>{stockDataOverview.trade_volume}</div>
            <br></br>
          </div>
        </div>
      </div>
    </div >
  );
}
