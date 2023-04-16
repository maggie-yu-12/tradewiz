import { Alert } from '@mui/material';
import { React, useRef, useState } from 'react';

import { useNavigate } from 'react-router-dom';

import axios from "axios";
import '../styles/login.css';

export const Register = ({ login, setLogin }) => {
  // eslint-disable-next-line prefer-const
  let email = useRef('');
  // eslint-disable-next-line prefer-const
  let password = useRef('');
  // eslint-disable-next-line prefer-const
  let username = useRef('')

  const [showNoAccountWarning, setShowNoAccountWarning] = useState(false)
  const [showWrongPassError, setShowWrongPassError] = useState(false)

  const navigate = useNavigate();

  function handleOnChangeEmail(e) {
    email.current = e.target.value;
  }

  function handleOnChangePass(e) {
    password.current = e.target.value;
  }

  function handleOnChangeUsername(e) {
    username.current = e.target.value;
  }

  function handleRegister(e) {
    axios.defaults.baseURL = process.env.REACT_APP_DOMAIN;
    axios({
      method: "POST",
      url: "/register",
      data: { email: email.current, password: password.current, username: username.current }
    })
      .then((res) => {
        data = res.data
        if (data.code == 409) {
          setShowWrongPassError(true)
        } else {
          localStorage.setItem('user', JSON.stringify({ email: email.current, password: password.current, username: username.current, watchlist: JSON.stringify([]) }))
        }
        email.current = ""
        password.current = ""
        navigate('/home')
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
      <p id="welcome-msg">Welcome!</p>
      {showWrongPassError && <Alert severity="error">This is an error alert — check it out!</Alert>}
      {showNoAccountWarning && <Alert severity="warning">This is a warning alert — check it out!</Alert>}
      <div className="input-box">
        <input type="email" pattern="/^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/" onChange={handleOnChangeEmail} placeholder="Email" />
        <br />
        <br />
        <input type="text" onChange={handleOnChangeUsername} placeholder="Username" />
        <br />
        <br />
        <input type="password" onChange={handleOnChangePass} placeholder="Password" />
      </div>
      <br />
      <br />
      <div className="login-btn-container">
        <div id="login-btn" onClick={handleRegister}>
          Register
        </div>
      </div>
      <div id="register-link">
        <p>Have an account already?</p>
        <p id="register-click" onClick={() => setLogin(true)}> Log in here!</p>
      </div>
    </div>
  )
}