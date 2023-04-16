import { useEffect, useState } from "react";
import { Carousel } from 'react-responsive-carousel';
import "react-responsive-carousel/lib/styles/carousel.min.css"; // requires a loader
import { TransformComponent, TransformWrapper } from "react-zoom-pan-pinch";
import { FavoritesList } from "../components/FavoritesList";
import { NavBar } from "../components/NavBar";
import { StockData } from "../components/StockData";

import axios from "axios";

import '../styles/watchlist.css';

export const WatchList = () => {
  const [favorites, setFavorites] = useState([])
  const [selectedCompany, setSelectedCompany] = useState("")
  const [companyData, setCompanyData] = useState("")

  useEffect(() => {
    const companies = JSON.parse(JSON.parse(localStorage.getItem("user")).watchlist)
    setFavorites(companies)
    setSelectedCompany(companies[0])
  }, [])

  useEffect(() => {
    axios.defaults.baseURL = process.env.REACT_APP_DOMAIN;
    if (selectedCompany !== '') {
      axios({
        method: "GET",
        url: "/get_company_data",
        params: { company: selectedCompany }
      })
        .then((res) => {
          data = res.data
          setCompanyData(JSON.stringify(data))
          console.log(data)
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response);
            console.log(error.response.status);
            console.log(error.response.headers);
          }
        });
    }
  }, [selectedCompany])

  return (
    <div className="watchlist">
      <NavBar />
      <div className="watchlist-background">
        <div className="my-favorites">
          <div className="my-favorites-bg">
            <p id="my-favorites-label">My favorites</p>
            <FavoritesList favorites={favorites} setSelectedCompany={setSelectedCompany} />
          </div>
        </div>
        <div className="company-data">
          {companyData !== "" && (<>

            <StockData company={JSON.parse(companyData).Company.substring(1)} companyData={companyData} />
            <p id="favorite-week">Sentiment Visualizations (Updated for {(new Date(JSON.parse(companyData)['1_StartDate'].substring(0, JSON.parse(companyData)['1_StartDate'].indexOf('#') == -1 ? JSON.parse(companyData)['1_StartDate'].length : JSON.parse(companyData)['1_StartDate'].indexOf('#')))).toString().slice(0, 15)} &nbsp;~&nbsp;
              {(new Date(JSON.parse(companyData)['1_EndDate'].substring(0, JSON.parse(companyData)['1_EndDate'].indexOf('#') == -1 ? JSON.parse(companyData)['1_EndDate'].length : JSON.parse(companyData)['1_EndDate'].indexOf('#')))).toString().slice(0, 15)})
            </p>
            <Carousel>
              <div id="favorite-graph">
                <p>Sentiment Score Change</p>
                <TransformWrapper>
                  <TransformComponent>
                    <img id="favorite-wordcloud" src={JSON.parse(companyData)['SentimentScoreChangeGraph']} />
                  </TransformComponent>
                </TransformWrapper>
              </div>
              {/* <p id="favorite-week">Visuals for Week of {(new Date(JSON.parse(companyData)['1_StartDate'].substring(0, JSON.parse(companyData)['1_StartDate'].indexOf('#')))).toString().slice(0, 15)} &nbsp;~&nbsp;
                {(new Date(JSON.parse(companyData)['1_EndDate'].substring(0, JSON.parse(companyData)['1_StartDate'].indexOf('#')))).toString().slice(0, 15)}
              </p> */}
              {/* <div id="favorite-graphs-group"> */}
              <div id="favorite-graph">
                <p>WordCloud</p>
                <TransformWrapper>
                  <TransformComponent>
                    <img id="favorite-wordcloud" src={JSON.parse(companyData)['WordCloud']} />
                  </TransformComponent>
                </TransformWrapper>
              </div>
              <div id="favorite-graph">
                <p>Sentiment Score Distribution</p>
                <TransformWrapper>
                  <TransformComponent>
                    <img id="favorite-wordcloud" src={JSON.parse(companyData)['SentimentFreqBarChart']} />
                  </TransformComponent>
                </TransformWrapper>
              </div>
              {/* </div> */}
            </Carousel>
          </>)}


        </div>
      </div>
    </div >
  )
}