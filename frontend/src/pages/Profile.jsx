import { React, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Avatar from '@mui/material/Avatar';
import { NavBar } from '../components/NavBar';
import '../styles/profile.css';



export const Profile = () => {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [update, setUpdate] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    user = localStorage.getItem("user")
    if (user == null) {
      navigate('/home')
    }

    user = JSON.parse(localStorage.getItem("user"))
    curr_email = user.email
    curr_username = user.username
    curr_password = user.password

    setEmail(curr_email)
    setUsername(curr_username)
    setPassword(curr_password)

  }, [])

  function handleConfirmUpdate(e) {
    user = JSON.parse(localStorage.getItem("user"))
    user.username = username;
    user.password = password;

    localStorage.setItem("user", JSON.stringify(user))
    setUpdate(false)
  }

  function handleOnChangePass(e) {
    setPassword(e.target.value);
  }

  function handleOnChangeUsername(e) {
    setUsername(e.target.value);
  }


  return (
    <>
      <NavBar />
      <div className="profile-background">
        <div className="profile-card">
          <div className="left-profile-side">
            <Avatar sx={{ width: 250, height: 250, fontSize: 100 }}>{username.substring(0, 1)}</Avatar>

            {!update && <div id="update-profile-button" onClick={() => setUpdate(!update)}>
              Update information
            </div>}
            {update && <div id="confirm-update-profile-button" onClick={handleConfirmUpdate}>
              Confirm update
            </div>}
          </div>
          <div className="user-info">
            <div id="info-container">
              <p id="update-label">Email</p>
              <p>{email}</p>
            </div>
            <div id="info-container">
              <p id="update-label">Username</p>
              <p>{update ? <input type="text" onChange={handleOnChangeUsername} placeholder="Username" /> : username}</p>
            </div>
            <div id="info-container">
              <p id="update-label">Password</p>
              <p>{update ? <input type="password" onChange={handleOnChangePass} placeholder="Password" /> : "*".repeat(password.length)}</p>
            </div>
          </div>

          {/* {update && <>
            <div className="user-update-input-box">
              <input type="text" onChange={handleOnChangeUsername} placeholder="Username" />
              <input type="password" onChange={handleOnChangePass} placeholder="Password" />
            </div>
            <br />
            <br />
            <div className="login-btn-container">
              <div id="login-btn" onClick={handleRegister}>
                Register
              </div>
            </div>
          </>
          } */}
        </div >
      </div>
    </>);
}