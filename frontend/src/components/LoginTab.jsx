import { Link } from 'react-router-dom';

export const LoginTab = ({ login }) => {
  return (
    <div className="tab-container">
      <Link to="/login">
        <div id={login ? "login-tab-light" : "login-tab-dark"}>
          Log In
        </div>
      </Link>
      <Link to="/register">
        <div id={!login ? "login-tab-light" : "login-tab-dark"}>
          Sign Up
        </div>
      </Link>
    </div>
  )
}