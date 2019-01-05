import React, { Component } from 'react';
import LoginPage from "./Features/LoginPage";
import Polls from "./Features/Polls"
import {Switch, Route, Router} from "react-router-dom";
import history from "./General/History";

class App extends Component {
    render() {
        return (
            <Router history={history}>
              <Switch >
                <Route path="/login" component={LoginPage}/>
                <Route path="/polls" component={Polls}/>
              </Switch>
            </Router>
        )
    }
}

export default App;

