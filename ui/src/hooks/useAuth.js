import React, { useContext, createContext } from "react";
import { useHistory } from "react-router-dom";
import useLocalStorage from "./useLocalStorage";

const authContext = createContext();

function ProvideAuth({ children }) {
  const history = useHistory();
  const [username, setUsername] = useLocalStorage("username", null);

  function logIn(username) {
    setUsername(username);
  }

  const logOut = () => {
    setUsername(null);
  };

  const auth = {
    username,
    logIn,
    logOut,
  };

  return <authContext.Provider value={auth}>{children}</authContext.Provider>;
}

function useAuth() {
  return useContext(authContext);
}

export { useAuth, ProvideAuth };
