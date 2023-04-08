import { React, useRef } from 'react';


import '../styles/login.css';

export const RegisterCard = () => {
  // eslint-disable-next-line prefer-const
  let username = useRef('');
  // eslint-disable-next-line prefer-const
  let password = useRef('');
  // eslint-disable-next-line prefer-const

  function handleOnChangeUser(e) {
    username.current = e.target.value;
  }

  function handleOnChangePass(e) {
    password.current = e.target.value;
  }

  return (
    <div className="login-card">
      {/* <div className="title">
            <img id="login-logo" src={logo} alt="site-logo" />
          </div> */}
      <div className="input-box">
        <input type="text" onChange={handleOnChangeUser} placeholder="Username" />
        <br />
        <br />
        <input type="password" onChange={handleOnChangePass} placeholder="Password" />
      </div>
      <br />
      <br />
      <div className="login-btn-container">
        <div id="signup-btn">
          Create a new account
        </div>
      </div>
      {/* <div className="text">
            <p> Need to create a new account? </p>
            <Link
              to="/register"
            >
              <p className="text">Create Account</p>
            </Link>
          </div> */}
    </div>
  )
}