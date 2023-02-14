import axios from 'axios';
import { lazy, Suspense, useEffect, useState } from 'react';
import HomeSearch from '../components/HomeSearch';
import NavBar from '../components/NavBar';

// import Spinner from 'react-bootstrap/Spinner';
const RecommendedLongTable = lazy(() => import('../components/RecommendedLongTable'))
const RecommendedShortTable = lazy(() => import('../components/RecommendedShortTable'))

import company_list from '../model/company_list.json';

// import 'semantic-ui-css/semantic.min.css';
import '../styles/home.css';
import '../styles/homesearch.css';
import '../styles/navbar.css';
import '../styles/table.css';

const Home = () => {
  // const data = useMemo(() => getData(), [])
  const [data, setData] = useState([])

  useEffect(() => getData(), [])

  function getData() {
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
            Object.keys(company_list).forEach(function (key) {
              company_name = company_list[key];
              obj = {
                "company": company_name,
                "week": weekly_res[key]['sentiment'],
                "month": monthly_res[key]['sentiment'],
                "activity": activity_res[key]['day_tweets'],
                "sentiment": weekly_res[key]['sentiment_change']
              }
              final_res.push(obj);
              setData(final_res);
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
      <NavBar />
      <HomeSearch />
      <div className='home-container'>
        {/* <Suspense>
          <h3> Recommended Longs </h3>
          <div className='table-container'>
            <RecommendedLongTable data={data} />
          </div>
        </Suspense> */}
        <Suspense>
          <div className='table-container'>
            <RecommendedShortTable data={data} />
          </div>
        </Suspense>
      </div>
    </div>
  )
}

// const LoadingSpinner = () => (
//   <Spinner animation="grow">
//     <span className="visually-hidden">Loading...</span>
//   </Spinner >
// )

export default Home