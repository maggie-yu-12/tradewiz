import FavoriteIcon from '@mui/icons-material/Favorite';
import { pink } from '@mui/material/colors';
import axios from 'axios';
import React, { lazy, Suspense, useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { NavBar } from '../components/NavBar';
// import { News } from '../components/News';

import '../styles/Individual.css';

const News = lazy(() => import('../components/News'))

export function Individual() {
  const [watchList, setWatchList] = useState(JSON.parse(JSON.parse(localStorage.getItem("user")).watchlist))
  const [searchParams] = useSearchParams();
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
  const [newsData, setNewsData] = useState({
    news_reddit: 'Loading...',
    news_twitter: 'Loading...',
  })
  const [graphData, setGraphData] = useState({
    img_path: 'Loading...',
  });

  function addToWatchList(company) {
    arr = watchList
    // Take care of any accidental double-clicks
    if (!arr.includes(company)) {
      arr.push(company)
      setWatchList(arr);
      user = JSON.parse(localStorage.getItem("user"))
      user.watchlist = JSON.stringify(arr);

      localStorage.setItem("user", JSON.stringify(user))
    }
  }

  function removeFromWatchList(company) {
    arr = watchList.filter(e => e !== company);
    setWatchList(arr);
    user = JSON.parse(localStorage.getItem("user"))
    user.watchlist = JSON.stringify(arr);

    localStorage.setItem("user", JSON.stringify(user))
  }


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
      params: { symbol: searchParams.get('symbol') },
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
      params: { symbol: searchParams.get('symbol') },
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
      params: { symbol: searchParams.get('symbol') },
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

  // function getNewsData() {
  //   console.log(window.location.pathname)
  //   axios({
  //     method: 'GET',
  //     url: '/newsdata',
  //     params: { symbol: searchParams.get('symbol') },
  //   })
  //     .then(function (response) {
  //       const res = response.data
  //       setNewsData(({
  //         news_twitter: res.stock_news_twitter,
  //         news_reddit: res.stock_news_reddit,
  //       }))
  //       console.log(response);
  //     })
  //     .catch(function (error) {
  //       console.log(error);
  //     });
  // }

  function getStockGraph() {
    axios({
      method: 'GET',
      url: '/stockgraph',
      params: { symbol: searchParams.get('symbol') },
    }).then(function (response) {
      const res = response.data
      setGraphData(({
        img_path: res.image,
      }))
      console.log(response);
    })
      .catch(function (error) {
        console.log(error);
      });
  }

  function displayImage(src, width, height) {
    var img = document.createElement("img");
    img.src = src;
    img.width = width;
    img.height = height;
    document.body.appendChild(img);
  }

  // Get stock information from Alpha Vantage API, third line makes it update with search query
  useEffect(() => {
    getStockDataOverview();
    getStockDataScore();
    getStockDataActivity();
    // getNewsData();
    // getStockGraph();
  }, [searchParams]);

  //end of new line 

  return (
    < div class='Individual-outer-container' >
      <NavBar />
      <div class='Individual-inner-container'>
        <div className="individual-group-one">
          <div id="stock-label">
            <div id="stock-name-box">
              <div id='Stock-name'>
                <p>{stockDataOverview.name} ({stockDataOverview.symbol})</p>
                {watchList.includes(stockDataOverview.symbol.toLowerCase()) ? <FavoriteIcon sx={{ color: pink[500] }} onClick={() => removeFromWatchList(stockDataOverview.symbol.toLowerCase())} /> : <FavoriteIcon color="action" onClick={() => addToWatchList(stockDataOverview.symbol.toLowerCase())} />}
              </div>
            </div>
            <div id="stock-desc-box">
              {stockDataOverview.description}
            </div>
          </div>

        </div>
        <div class='Stock-data-frame'>
          <div id="summary-title-box">
            <p id="summary-title">Summary</p>
          </div>
          <div id="summary-desc-box">
            <p id="summary-body">This is summary of the activity regarding {stockDataOverview.name} past week in Twitter and Reddit. Sentiment score ranges from -1 to 1, where -1
              means negative and 1 positive. Activity indicates the number of tweets/posts on these platforms.</p>
          </div>
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


        {/* <div> < img src={graphData.img_path} alt="Graph"> </img></div> */}

        {/* <div class='Graph-component'>

        </div> */}
        {/* <div class='News-frame'>
          <div class='News-frame-header'>News Aggregation</div>
          <div class='News-frame-comments'>
            <News site='Twitter' newsinfo={newsData.news_twitter} />
            <News site='Reddit' newsinfo={newsData.news_reddit} />
          </div>
        </div> */}
        <Suspense>
          <News searchParams={searchParams} />
        </Suspense>

        <br></br>

        {/* <div class='Comments-frame'>
          <div class='Comments-frame-header'>Comment Aggregation</div>
          <div class='Comments-frame-comments'>Comments</div>
        </div> */}
      </div>
    </div >
  );
}
