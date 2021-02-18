import { QueryClient, QueryClientProvider } from "react-query";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import { LoginPage, PrivateRoute, ProvideAuth } from "./auth";
import { ChatPage } from "./chat";

import "./App.css";

function App() {
  return (
    <QueryClientProvider client={new QueryClient()}>
      <ProvideAuth>
        <Router>
          <Switch>
            <Route path="/login">
              <LoginPage />
            </Route>
            <PrivateRoute path={["/rooms/:roomId", "/"]}>
              <ChatPage />
            </PrivateRoute>
          </Switch>
        </Router>
      </ProvideAuth>
    </QueryClientProvider>
  );
}

export default App;
