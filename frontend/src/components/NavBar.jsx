import React from 'react';
// import { useNavigate } from "react-router-dom";
import logo from '../assets/img/logo.png';
import '../styles/navbar.css';


import { Link } from 'react-router-dom';
import { ProfileMenu } from './ProfileMenu';
import { SearchNavBar } from './SearchNavBar';


/**
 * Component for Navigation Bar.
 */
export const NavBar = ({ home }) => {
  // const [showProfileMenu, setShowProfileMenu] = useState(false)
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
        {!home && <SearchNavBar />}
      </div>
      <div className="nav-right">
        {/* <AccountCircleOutlinedIcon fontSize='large' onClick={() => setShowProfileMenu(!showProfileMenu)} /> */}
        {/* <ListItemIcon>
            <PersonAdd fontSize="small" onClick={() => setShowProfileMenu(!showProfileMenu)} />
          </ListItemIcon> */}
        <div id="navbar-profile">
          <ProfileMenu />
        </div>
      </div>
    </div>
  )
}