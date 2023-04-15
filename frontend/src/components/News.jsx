import {
  CircularProgress
} from '@mui/material';
import axios from 'axios';
import { default as React, useEffect, useState } from 'react';
import '../styles/News.css';

const News = ({ searchParams }) => {
  const [newsData, setNewsData] = useState({})

  useEffect(() => {
    getNewsData();
    // getStockGraph();
  }, [searchParams]);


  function getNewsData() {
    console.log(window.location.pathname)
    axios({
      method: 'GET',
      url: '/newsdata',
      params: { symbol: searchParams.get('symbol') },
    })
      .then(function (response) {
        const res = response.data
        setNewsData(({
          news_twitter: res.stock_news_twitter,
          news_reddit: res.stock_news_reddit,
        }))
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  return (
    <>
      {JSON.stringify(newsData) === '{}' ? <CircularProgress /> : (
        <div class='News-frame'>
          <div class='News-frame-header'>News Aggregation</div>
          <div class='News-frame-comments'>
            <NewsIndividual site='Twitter' newsinfo={newsData.news_twitter} />
            <NewsIndividual site='Reddit' newsinfo={newsData.news_reddit} />
          </div>

        </div>)}
    </>
  )
}

// default site set to reddit
function NewsIndividual({ site, newsinfo }) {
  // console.log('NEWS NEWSINFO');
  // console.log(newsinfo);
  return (
    <div id='News-frame'>
      <div id='News-site-name'>
        {site}
      </div>
      {console.log(newsinfo)}
      {newsinfo !== undefined && newsinfo.length > 0 && [...Array(newsinfo.length).keys()].map((idx, i) => (<Newsblock newsinfo={newsinfo[idx]} />))}
    </div>
  )
}

function Newsblock({ site, newsinfo: [title, description, date] }) {
  return (
    <div id='Newsblock-background'>
      <div id='Newsblock-title'>{title}</div>
      <hr></hr>
      <div id='Newsblock-description'>{description}</div>
      <div id='Newsblock-date'>{date}</div>
    </div>
  )
};

export default News;