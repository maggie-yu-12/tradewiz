import { lazy, Suspense, useMemo } from 'react';
import HomeSearch from '../components/HomeSearch';
import NavBar from '../components/NavBar';
// import Spinner from 'react-bootstrap/Spinner';
const RecommendedLongTable = lazy(() => import('../components/RecommendedLongTable'))
const RecommendedShortTable = lazy(() => import('../components/RecommendedShortTable'))

import sample_data from '../model/sample_data.json';

import '../styles/home.css';
import '../styles/homesearch.css';
import '../styles/navbar.css';
import '../styles/table.css';

const Home = () => {
  const data = useMemo(() => sample_data, [])

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