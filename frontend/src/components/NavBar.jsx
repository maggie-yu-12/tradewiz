import React from 'react';
import { useNavigate } from "react-router-dom";
import logo from '../assets/img/logo.png';
import '../styles/navbar.css';

/**
 * Component for Navigation Bar.
 */
export function NavBar() {
  const navigate = useNavigate();

  onClickHandler = (e) => {
    e.preventDefault();
    navigate({
      pathname: '/',
    });
  }

  return (
    <div className="nav-container">
      <button class="submit" onClick={onClickHandler}>
        <img src={logo} id="site-logo" alt="site-logo" />
      </button>

      <div id="features-tab">Features</div>
      <div id="pricing-tab">Pricing</div>
      <div id="community-tab">Community</div>
      <div id="support-tab">Support</div>
    </div>
  )
}