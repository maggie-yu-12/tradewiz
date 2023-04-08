import React from 'react';
import '../styles/News.css';

// default site set to reddit
export function News({ site = 'Reddit' }) {
  return (
    <div id="News-frame">
      <div id="News-site-name">
        {site}
      </div>
      <Newsblock />
      <Newsblock />
      <Newsblock />
    </div>
  )
}

function Newsblock({ site = 'reddit' }) {
  return (
    <div id="Newsblock-background">
      <div id="Newsblock-title">title</div>
      <div id="Newsblock-line">------------------</div>
      <div id="Newsblock-date">date</div>
    </div>
  )
};