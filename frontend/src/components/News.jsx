import React from 'react';
import '../styles/News.css';

// default site set to reddit
export function News({ site, newsinfo }) {
  // console.log('NEWS NEWSINFO');
  // console.log(newsinfo);
  return (
    <div id='News-frame'>
      <div id='News-site-name'>
        {site}
      </div>
      <Newsblock newsinfo={newsinfo[0]} />
      <Newsblock newsinfo={newsinfo[1]} />
      <Newsblock newsinfo={newsinfo[2]} />
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