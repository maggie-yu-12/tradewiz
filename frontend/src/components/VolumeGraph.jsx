import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';

const SentimentVolumeGraph = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('sample_volume_data.json')
      .then(response => response.json())
      .then(jsonData => setData(jsonData))
      .catch(error => console.error(error));
  }, []);

  const chartData = {
    labels: data.map(datum => datum.date),
    datasets: [
      {
        label: 'Sentiment Activity',
        backgroundColor: '#82ca9d',
        data: data.map(datum => datum.sentimentActivity)
      },
      {
        label: 'Trade Volume',
        type: 'line',
        fill: false,
        backgroundColor: '#8884d8',
        borderColor: '#8884d8',
        data: data.map(datum => datum.tradeVolume)
      }
    ]
  };

  return (
    <Bar
      data={chartData}
      options={{
        scales: {
          xAxes: [{
            stacked: true
          }],
          yAxes: [{
            stacked: true
          }]
        }
      }}
    />
  );
};

export default SentimentVolumeGraph;
