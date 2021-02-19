import { QueryClient, QueryClientProvider } from "react-query";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import { PrivateRoute } from "./components";
import { ProvideAuth } from "./hooks";
import { ChatPage, LoginPage, SignUpPage } from "./pages";

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
            <Route path="/signup">
              <SignUpPage />
            </Route>
            <PrivateRoute path="/">
              <ChatPage />
            </PrivateRoute>
          </Switch>
        </Router>
      </ProvideAuth>
    </QueryClientProvider>
  );
}

export default App;
