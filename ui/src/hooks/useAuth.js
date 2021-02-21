import { useContext, createContext } from "react";
import useLocalStorage from "./useLocalStorage";

const authContext = createContext();

function ProvideAuth({ children }) {
  const [username, setUsername] = useLocalStorage("username", null);

  function logIn(usrname) {
    setUsername(usrname);
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
