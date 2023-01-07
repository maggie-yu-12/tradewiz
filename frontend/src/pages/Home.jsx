import { useMemo } from 'react';
import { RecommendedLongTable } from '../components/RecommendedTable';

import sample_data from '../model/sample_data.json';

import '../styles/home.css';

const Home = () => {
  const data = useMemo(() => sample_data, [])

  return (
    <div className='home-container'>
      <div className='long-table-container'>
        <RecommendedLongTable data={data} />
      </div>
    </div>
  )
}

export default Home