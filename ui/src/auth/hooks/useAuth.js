import React, { useContext, createContext } from "react";
import { useHistory } from "react-router-dom";
import useLocalStorage from "./useLocalStorage";

const authContext = createContext();

function ProvideAuth({ children }) {
  const history = useHistory();
  const [user, setUser] = useLocalStorage("user", null);

  function logIn(user) {
    setUser(user);
  }

  const logOut = () => {
    setUser(null);
  };

  const auth = {
    user,
    logIn,
    logOut,
  };

  return <authContext.Provider value={auth}>{children}</authContext.Provider>;
}

function useAuth() {
  return useContext(authContext);
}

export { useAuth, ProvideAuth };
