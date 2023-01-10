import axios from "axios";
import React, { useEffect, useState } from 'react';
import { useNavigate } from "react-router-dom";
import '../styles/Individual.css';
import logo from '../tradewiz-logo.png';

export function Individual() {

  // new line start
  // TODO: Get stock abbreviation from search enter.

  const stockAbbreviation = "MSFT"
  const navigate = useNavigate();
  const [profileData, setProfileData] = useState(null)
  const [stockData, setStockData] = useState({
    name: "hi",
    description: "ho",
  });
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

  // Using useEffect for single rendering
  useEffect(() => {
    // Using fetch to fetch the api from 
    // flask server it will be redirected to proxy
    axios.get('/stockdata').then(res => res.data).then(data => {
      // Setting a data from api
      setStockData({
        name: data.name,
        description: data.about,
      });
    })
  }, []);

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
        <div class="Stock-data-frame">
          <div id="Stock-name">Stock name is: {stockData.name}</div>
          <div id="Stock-description">Stock description: {stockData.description}</div>
        </div>

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
        {/* <p>To get your profile details: </p><button onClick={getData}>Click me</button>
        {profileData && <div>
          <p>Profile name: {profileData.profile_name}</p>
          <p>About me this is: {profileData.about_me}</p>
        </div>
        } */}
        {/* end of new line */}
      </body>
    </div>
  );
}
