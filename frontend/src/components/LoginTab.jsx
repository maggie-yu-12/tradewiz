
export const LoginTab = ({ login, setLogin }) => {
  return (
    <div className="tab-container">
      <button onClick={() => setLogin(true)}>
        <div id={login ? "login-tab-light" : "login-tab-dark"}>
          Log In
        </div>
      </button>
      <button onClick={() => setLogin(false)}>
        <div id={!login ? "login-tab-light" : "login-tab-dark"}>
          Sign Up
        </div>
      </button>
    </div>
  )
}