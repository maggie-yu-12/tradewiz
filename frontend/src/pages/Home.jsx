import { lazy, Suspense, useMemo } from 'react';
import Spinner from 'react-bootstrap/Spinner';
const RecommendedLongTable = lazy(() => import('../components/RecommendedLongTable'))
const RecommendedShortTable = lazy(() => import('../components/RecommendedShortTable'))

import sample_data from '../model/sample_data.json';

import '../styles/home.css';

const Home = () => {
  const data = useMemo(() => sample_data, [])

  return (
    <div className='home-container'>
      <Suspense>
        <h3> Recommended Longs </h3>
        <div className='table-container'>
          <RecommendedLongTable data={data} />
        </div>
      </Suspense>
      <Suspense>
        <h3> Recommended Shorts </h3>
        <div className='table-container'>
          <RecommendedShortTable data={data} />
        </div>
      </Suspense>
    </div>
  )
}

const LoadingSpinner = () => (
  <Spinner animation="grow">
    <span className="visually-hidden">Loading...</span>
  </Spinner >
)

export default Home