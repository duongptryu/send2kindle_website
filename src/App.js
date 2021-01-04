import "./App.css";
import NavBar from "./components/NavBar";
import { Container } from "reactstrap";
import Footer from "./components/Footer";
import Main from "./components/Main";
import Guide from "./components/Guide";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import React from "react";

class App extends React.Component {
  render() {
    return (
      <Router>
        <div className="main">
          <Container>
            <div className="main-2">
              <NavBar />
              <Switch>
                <Route path="/guide/">
                  <Guide />
                </Route>
                <Route path="/">
                  <Main />
                </Route>
              </Switch>
              <Footer />
            </div>
          </Container>
        </div>
      </Router>
    );
  }
}
export default App;
