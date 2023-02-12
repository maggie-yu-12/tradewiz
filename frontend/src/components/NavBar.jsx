

import logo from '../assets/img/logo.png';

/**
 * Component for Navigation Bar.
 */
const NavBar = () => {
  return (
    <div className="nav-container">
      <img src={logo} alt="site-logo" />
      <div id="features-tab">Features</div>
      <div id="pricing-tab">Pricing</div>
      <div id="community-tab">Community</div>
      <div id="support-tab">Support</div>
    </div>
  )
}

export default NavBar;