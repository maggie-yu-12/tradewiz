import axios from 'axios';
import { lazy, Suspense, useEffect, useState } from 'react';
import { NavBar } from '../components/NavBar';
import { Search } from '../components/Search';

// import Spinner from 'react-bootstrap/Spinner';
// const RecommendedLongTable = lazy(() => import('../components/RecommendedLongTable'))
const BiggestSentimentMoversTable = lazy(() => import('../components/BiggestSentimentMoversTable'))

import company_list from '../model/company_list.json';

import 'bootstrap/dist/css/bootstrap.min.css';

// import 'semantic-ui-css/semantic.min.css';
import '../styles/home.css';
import '../styles/homesearch.css';
import '../styles/login.css';
import '../styles/navbar.css';
import '../styles/searchbar.css';
import '../styles/table.css';


const DefaultPage = () => {
  // const data = useMemo(() => getData(), [])
  const [data, setData] = useState([]);

  useEffect(() => {
    let isMounted = true;
    if (isMounted) {
      getData(isMounted)
    }

    return () => { isMounted = false };
  }, []);

  function getData(isMounted) {
    axios.defaults.baseURL = "http://localhost:8000";
    axios({
      method: "GET",
      url: "/weekly_sentiment",
    })
      .then((weekly_response) => {
        const weekly_res = weekly_response.data;

        axios({
          method: "GET",
          url: "/month_sentiment",
        }).then((monthly_response) => {
          const monthly_res = monthly_response.data;

          axios({
            method: "GET",
            url: "/activity",
          }).then((activity_response) => {
            const activity_res = activity_response.data;

            final_res = []
            Object.keys(company_list).forEach(function (name) {
              company_key = name
              company_name = company_list[company_key];
              obj = {
                "company": company_name,
                "ticker": name,
                "week": weekly_res[company_key]['sentiment'],
                "month": monthly_res[company_key]['sentiment'],
                "activity": activity_res[company_key]['weekly_tweets'],
                "sentiment": weekly_res[company_key]['sentiment_change']
              }
              final_res.push(obj);
              if (isMounted) {
                setData(final_res);
              }

            })

          })
        })
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }

  return (
    <div className='home-outer-container'>
      {/* <img src="https://tweetwordcloud.s3.amazonaws.com/%23googl.png?AWSAccessKeyId=AKIA4MVBRATKCMDQMUU3&Signature=NZU923dX3KbMKnN8oTXFOrWZPUo%3D&Expires=1681935162" /> */}
      <NavBar />
      <div className="search-container">
        <div className="h-greeting">
          <p id="h-main-greeting">Never miss a big stock movement</p>
          <p id="h-sub-greeting">Everything you need for sentiment analysis</p>
        </div>
        <Search />
      </div>
      <div className='home-container'>
        {/* <Suspense>
          <h3> Recommended Longs </h3>
          <div className='table-container'>
            <RecommendedLongTable data={data} />
          </div>
        </Suspense> */}
        <Suspense>
          <div className='table-container'>
            <BiggestSentimentMoversTable data={data} />
          </div>
        </Suspense>
      </div>
    </div>
  )
}

export const Home = () => {
  return (
    <DefaultPage />
  )
}

// const LoadingSpinner = () => (
//   <Spinner animation="grow">
//     <span className="visually-hidden">Loading...</span>
//   </Spinner >
// )

export default Home
