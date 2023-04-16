import { Alert } from '@mui/material';
import { React, useEffect, useRef, useState } from 'react';

import { useNavigate } from 'react-router-dom';

import logo from '../assets/img/logo.png';
import '../styles/login.css';
import { Register } from './Register';


import axios from "axios";

export const Login = ({ showModal, setShowModal }) => {
  const [login, setLogin] = useState(true);
  const navigate = useNavigate();
  useEffect(() => {

    if (localStorage.getItem("user") !== null) {
      navigate('/home')
    }

  }, [])
  return (
    // <div className="login-card">
    //   <div className="left-side-card">
    //     <img id="logo" src={logo} alt="site-logo" />
    //   </div>
    //   <div className="right-side-card">
    //     <LoginTab login={login} setLogin={setLogin} />
    //     {login && <LoginCard />}
    //     {!login && <RegisterCard />}
    //   </div>
    // </div >);
    <div className="login-card">
      <div className="left-side-card">
        <img id="logo" src={logo} alt="site-logo" />
      </div>
      <div className="right-side-card">
        {/* <LoginTab login={login} setLogin={setLogin} /> */}
        {login && <LoginCard login={login} setLogin={setLogin} />}
        {!login && <Register login={login} setLogin={setLogin} />}
      </div>
    </div >);
}

const LoginCard = ({ login, setLogin }) => {
  // eslint-disable-next-line prefer-const
  let email = useRef('');
  // eslint-disable-next-line prefer-const
  let password = useRef('');

  const [showNoAccountWarning, setShowNoAccountWarning] = useState(false)
  const [showWrongPassError, setShowWrongPassError] = useState(false)
  const navigate = useNavigate();


  function handleOnChangeEmail(e) {
    email.current = e.target.value;
  }

  function handleOnChangePass(e) {
    password.current = e.target.value;
  }


  function handleLogin(e) {
    setShowNoAccountWarning(false);
    setShowWrongPassError(false);
    axios.defaults.baseURL = process.env.REACT_APP_DOMAIN;
    axios({
      method: "POST",
      url: "/login",
      data: { email: email.current, password: password.current }
    })
      .then((res) => {
        data = res.data
        if (data.code == 404) {
          setShowNoAccountWarning(true)
        } else if (data.code == 401) {
          setShowWrongPassError(true)
        } else {
          localStorage.setItem('user', JSON.stringify({ email: email.current, password: password.current, username: data.username, watchlist: JSON.stringify(data.watchlist) }))
          navigate('/home')
        }
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }


  return (
    <div className="login-background">
      <p id="welcome-msg">Welcome back!</p>
      <div id="login-alert-box">
        {showWrongPassError && <Alert severity="error" sx={{ width: '400px' }} >Wrong password!</Alert>}
        {showNoAccountWarning && <Alert severity="warning" sx={{ width: '400px' }}>Couldn't find an account asssociated with this email. Please register first.</Alert>}
      </div>
      <div className="input-box">
        <input type="email" onChange={handleOnChangeEmail} placeholder="Email" />
        <br />
        <br />
        <input type="password" onChange={handleOnChangePass} placeholder="Password" />
      </div>
      <br />
      <br />
      <div className="login-btn-container">
        <div id="login-btn" onClick={handleLogin}>
          Log In
        </div>
      </div>
      <div id="register-link">
        <p>Don't have an account yet? &nbsp;</p>
        <p id="register-click" onClick={() => setLogin(false)}> Register here!</p>
      </div>
    </div>
  )
}