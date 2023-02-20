import { useRef, useState } from 'react';
import { Modal } from 'react-bootstrap';

import { LoginTab } from '../components/LoginTab';

import '../styles/login.css';
import { RegisterCard } from './Register';

export const Login = ({ showModal, setShowModal }) => {
  const [login, setLogin] = useState(true);
  return (
    <Modal className='modal fade' centered animation show={showModal} onHide={() => setShowModal(false)} style={{ opacity: 1 }}>

      <Modal.Body>
        <LoginTab login={login} setLogin={setLogin} />
        {login && <LoginCard />}
        {!login && <RegisterCard />}
      </Modal.Body>
    </Modal >);
}

const LoginCard = () => {
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
    // <div className="login-container">
    //   <NavBar loginPage />
    //   <div className="login-sub-container">

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
    //   </div>
    // </div>
  )
}