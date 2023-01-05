import React from 'react'
import { useState } from 'react'
import axios from "axios";
import logo from './tradewiz-logo.png';
import './Individual.css';

function Individual() {

   // new line start
  const [profileData, setProfileData] = useState(null)

  // MAGGIE: am I dumb this doesn't work
  function getData() {
    axios({
      method: "GET",
      url:"/profile",
    })
    .then((response) => {
      const res =response.data
      setProfileData(({
        profile_name: res.name,
        about_me: res.about}))
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}
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

        {/* new line start*/}
        <p>To get your profile details: </p><button onClick={getData}>Click me</button>
        {profileData && <div>
              <p>Profile name: {profileData.profile_name}</p>
              <p>About me this is Individual: {profileData.about_me}</p>
            </div>
        }
         {/* end of new line */}
      </header>

      <body>
        <p>STOCK NAME (STC)</p>
        <p>NASDAQ # # #</p>
        <div classname="Sentiment-score-frame">
            Twitter Reddit Bloomberg Overall
        </div>

        <div classname="Graph"> 
            Graph
        </div>

        <br></br>

        <div classname="Comments-frame">
            <div classname="Comments-frame-child">Trending on...</div>
            <div classname="Comments-frame-child">Comments</div>
        </div>

      </body>
    </div>
  );
}

export default Individual;