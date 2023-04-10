import React from 'react';
// import { useNavigate } from "react-router-dom";
import logo from '../assets/img/logo.png';
import '../styles/navbar.css';


import { Link } from 'react-router-dom';


/**
 * Component for Navigation Bar.
 */
export const NavBar = ({ loginPage, showModal, setShowModal }) => {
  return (
    <div className="nav-container">
      <div className="nav-left">
        <Link to="/">
          <img src={logo} alt="site-logo" />
        </Link>
        <Link to="/features">
          <div id="features-tab">Features</div>
        </Link>
        <Link to="/pricing">
          <div id="pricing-tab">Pricing</div>
        </Link>
        <Link to="/community">
          <div id="community-tab">Community</div>
        </Link>
        <Link to="/support">
          <div id="support-tab">Support</div>
        </Link>
      </div>
      <div className="nav-right">
        {/* {!loginPage && <Link to="/login">
          <div id="login-btn">Login</div>
        </Link>} */}

        <button
          type="button"
          id="login-btn"
          onClick={() => setShowModal(true)}
        >
          Log In
        </button>
      </div>
    </div>
  )
}
