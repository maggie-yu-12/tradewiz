import axios from "axios";
import React, { useEffect, useState } from 'react';
import './Individual.css';
import logo from './tradewiz-logo.png';

export function Individual() {

  // new line start
  const [profileData, setProfileData] = useState(null)
  axios.defaults.baseURL = "http://localhost:8000";

  function getData() {
    axios({
      method: "GET",
      url: "/profile",
    })
      .then((response) => {
        const res = response.data
        setProfileData(({
          profile_name: res.name,
          about_me: res.about
        }))
      }).catch((error) => {
        if (error.response) {
          console.log(error.response)
          console.log(error.response.status)
          console.log(error.response.headers)
        }
      })
  }

  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    // fetch('http://localhost:8000/time').then(res => res.json()).then(data => {
    //   setCurrentTime(data.time)
    // });
    axios.get('/time').then(res => res.data).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  // Using useEffect for single rendering
  useEffect(() => {
    // Using fetch to fetch the api from 
    // flask server it will be redirected to proxy
    fetch('/stockname').then((res) =>
      res.json().then((data) => {
        // Setting a data from api
        setStockData({
          name: data.name,
          description: data.about,
        });
      })
    );
  }, []);

  const [count, setCount] = useState(0);

  // useEffect(() => {
  //   setTimeout(() => {
  //     setCount((count) => count + 1);
  //   }, 1000);
  // });

  // function getStockInfo() {
  //   axios({
  //     method: "GET",
  //     url: "/stock-name",
  //   })
  //     .then((response) => {
  //       const res = response.data
  //       setStockData(({
  //         name: res.name,
  //         description: res.about
  //       }))
  //     }).catch((error) => {
  //       if (error.response) {
  //         console.log(error.response)
  //         console.log(error.response.status)
  //         console.log(error.response.headers)
  //       }
  //     })
  // }
  //end of new line 

  return (
    <div className="Individual">
      <header className="Individual-header">



        <img src={logo} className="Individual-logo" alt="logo" />
        <a
          className="Individual-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Search Bar goes here
        </a>

      </header>

      <body>
        {/* <p>Time is: {stockData.name}</p> */}
        <h1>I've rendered {currentTime} times!</h1>
        {/* <p>Stock description: {stockData.description}</p> */}
        <p>NASDAQ # # #</p>
        <div className="Sentiment-score-frame">
          Twitter Reddit Bloomberg Overall
        </div>

        <div className="Graph">
          Graph
        </div>

        <br></br>

        <div className="Comments-frame">
          <div className="Comments-frame-child">Trending on...</div>
          <div className="Comments-frame-child">Comments</div>
        </div>
        {/* new line start*/}
        <p>To get your profile details: </p><button onClick={getData}>Click me</button>
        {profileData && <div>
          <p>Profile name: {profileData.profile_name}</p>
          <p>About me this is: {profileData.about_me}</p>
        </div>
        }
        {/* end of new line */}
      </body>
    </div>
  );
}
