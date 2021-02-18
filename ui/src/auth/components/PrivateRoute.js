import { Route, Redirect } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

function PrivateRoute({ children, ...rest }) {
  let auth = useAuth();
  return (
    <Route
      {...rest}
      render={() =>
        auth.user ? children : <Redirect to={{ pathname: "/login" }} />
      }
    />
  );
}

export default PrivateRoute;
