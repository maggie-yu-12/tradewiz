import { React, useRef } from 'react';
import { LoginTab } from '../components/LoginTab';
import NavBar from '../components/NavBar';


import '../styles/login.css';

export const Login = () => {
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
    // <div
    //   className="modal show"
    //   style={{ display: 'block', position: 'initial' }}
    // >
    //   <Modal.Dialog>
    //     <Modal.Header closeButton>
    //       <Modal.Title>Modal title</Modal.Title>
    //     </Modal.Header>

    //     <Modal.Body>
    //       <p>Modal body text goes here.</p>
    //     </Modal.Body>

    //     <Modal.Footer>
    //       <Button variant="secondary">Close</Button>
    //       <Button variant="primary">Save changes</Button>
    //     </Modal.Footer>
    //   </Modal.Dialog>
    // </div>
    <div className="login-container">
      <NavBar loginPage />
      <div className="login-sub-container">
        <div className="login-card-container">
          <LoginTab login />
          <div className="login-card">
            {/* <div className="title">
            <img id="login-logo" src={logo} alt="site-logo" />
          </div> */}
            <div className="input-box">
              <input type="text" onChange={handleOnChangeUser} placeholder="Username" />
              <br />
              <br />
              <input type="text" onChange={handleOnChangePass} placeholder="Password" />
            </div>
            <br />
            <br />
            <div className="login-btn-container">
              <div id="login-btn">
                Log In
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
        </div>
      </div>
    </div>
  )
}