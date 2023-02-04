import React from 'react';
import {Bar, Line} from 'react-chartjs-2';

const PriceGraph = ({data}) => {
  const chartData = {
    labels: data.map(datum => datum.date),
    datasets: [
      {
        label: 'Sentiment Score',
        backgroundColor: '#82ca9d',
        data: data.map(datum => datum.sentimentScore)
      },
      {
        label: 'Price Change Percentage',
        type: 'line',
        fill: false,
        backgroundColor: '#8884d8',
        borderColor: '#8884d8',
        data: data.map(datum => datum.pricePercentageChange)
      },
      {
        label: 'Trade Volatility',
        type: 'line',
        fill: false,
        backgroundColor: '#82ca9d',
        borderColor: '#82ca9d',
        data: data.map(datum => datum.volatility)
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

export default PriceGraph;