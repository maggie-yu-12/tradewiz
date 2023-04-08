import axios from 'axios';
import { lazy, Suspense, useEffect, useState } from 'react';
import HomeSearch from '../components/HomeSearch';
import NavBar from '../components/NavBar';
<<<<<<< HEAD

// import Spinner from 'react-bootstrap/Spinner';
const RecommendedLongTable = lazy(() => import('../components/RecommendedLongTable'))
const RecommendedShortTable = lazy(() => import('../components/RecommendedShortTable'))

import company_list from '../model/company_list.json';
=======

// import Spinner from 'react-bootstrap/Spinner';
// const RecommendedLongTable = lazy(() => import('../components/RecommendedLongTable'))
const BiggestSentimentMoversTable = lazy(() => import('../components/BiggestSentimentMoversTable'))

import company_list from '../model/company_list.json';

import 'bootstrap/dist/css/bootstrap.min.css';
>>>>>>> 21aac1f90caedffd2dfd277e1c04b048ad63f262

// import 'semantic-ui-css/semantic.min.css';
import '../styles/home.css';
import '../styles/homesearch.css';
<<<<<<< HEAD
import '../styles/navbar.css';
import '../styles/table.css';

const Home = () => {
  // const data = useMemo(() => getData(), [])
  const [data, setData] = useState([])

  useEffect(() => getData(), [])

  function getData() {
=======
import '../styles/login.css';
import '../styles/navbar.css';
import '../styles/searchbar.css';
import '../styles/table.css';
import { Login } from './Login';


const Home = () => {
  // const data = useMemo(() => getData(), [])
  const [data, setData] = useState([]);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    let isMounted = true;
    if (isMounted) {
      getData(isMounted)
    }

    return () => { isMounted = false };
  }, []);

  function getData(isMounted) {
>>>>>>> 21aac1f90caedffd2dfd277e1c04b048ad63f262
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
<<<<<<< HEAD
                "activity": activity_res[key]['day_tweets'],
                "sentiment": weekly_res[key]['sentiment_change']
              }
              final_res.push(obj);
              setData(final_res);
=======
                "activity": activity_res[key]['week_tweets'],
                "sentiment": weekly_res[key]['sentiment_change']
              }
              final_res.push(obj);
              if (isMounted) {
                setData(final_res);
              }

>>>>>>> 21aac1f90caedffd2dfd277e1c04b048ad63f262
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
<<<<<<< HEAD
      <NavBar />
=======
      <NavBar show={showModal} setShowModal={setShowModal} />
      {showModal && <Login showModal={showModal} setShowModal={setShowModal} />}
>>>>>>> 21aac1f90caedffd2dfd277e1c04b048ad63f262
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
<<<<<<< HEAD
            <RecommendedShortTable data={data} />
=======
            <BiggestSentimentMoversTable data={data} />
>>>>>>> 21aac1f90caedffd2dfd277e1c04b048ad63f262
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