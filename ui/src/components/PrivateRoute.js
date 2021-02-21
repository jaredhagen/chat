import { Route, Redirect } from "react-router-dom";

import { useAuth } from "../hooks";

function PrivateRoute({ children, ...rest }) {
  const auth = useAuth();
  return (
    <Route
      {...rest}
      render={() =>
        auth.username ? children : <Redirect to={{ pathname: "/signup" }} />
      }
    />
  );
}

export default PrivateRoute;
