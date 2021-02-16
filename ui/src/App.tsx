import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

import { Chat, Login, SignUp } from "./pages"

import './App.css';


function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Chat</Link>
            </li>
            <li>
              <Link to="/login">About</Link>
            </li>
            <li>
              <Link to="/signup">Users</Link>
            </li>
          </ul>
        </nav>
        <Switch>
          <Route path="/signup">
            <SignUp />
          </Route>
          <Route path="/login">
            <Login />
          </Route>
          <Route path="/">
            <Chat />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
