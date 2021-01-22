import "./App.css";
import NavBar from "./components/NavBar";
import { Container } from "reactstrap";
import Footer from "./components/Footer";
import Main from "./components/Main";
import Guide from "./components/Guide";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import React from "react";

class App extends React.Component {
  constructor() {
    super();
    this.state = {
      signIn: {
        username: "",
        password: "",
      },
      signUp: {
        username: "",
        password: "",
        email: "",
        first_name: "",
        last_name: "",
      },
      error: "",
      redirect: null,
    };
    this.signInHandle = this.signInHandle.bind(this);
    this.signInOnchange = this.signInOnchange.bind(this);
    this.signUpOnchange = this.signUpOnchange.bind(this);
    this.signUpHandle = this.signUpHandle.bind(this);
  }

  signUpOnchange(e) {
    const target = e.target;
    const name = target.name;
    const value = target.value;
    const old_info = this.state.signUp;
    switch (name) {
      case "username":
        old_info.username = value;
        break;
      case "password":
        old_info.password = value;
        break;
      case "email":
        old_info.email = value;
        break;
      case "firstName":
        old_info.first_name = value;
        break;
      default:
        old_info.last_name = value;
        break;
    }

    this.setState({
      SignUp: {
        ...old_info,
      },
    });
  }

  signInOnchange(e) {
    const target = e.target;
    const name = target.name;
    const value = target.value;
    const old_info = this.state.signIn;
    if (name === "username") {
      old_info.username = value;
    } else {
      old_info.password = value;
    }
    this.setState({
      SignIn: {
        ...old_info,
      },
    });
  }

  async signInHandle(e) {
    e.preventDefault();
    const info = this.state.signIn;
    if (info.username.length === 0 || info.password.length === 0) {
      alert("Please complete input before submit");
      return false;
    }
    let status = "";
    const formData = new FormData()
    formData.append("username", this.state.signIn.username)
    formData.append("password", this.state.signIn.password)
    // console.log(formData)
    // const data = this.state.signIn;
    let result = await fetch("http://localhost:8000/api/token", {
      method: "POST",
      mode: "cors",
      credentials: "include",
      // headers: {
      //   "Content-Type": "application/json",
      // },
      // body: JSON.stringify(data),
      body: formData
    })
      .then((res) => {
        status = res.status;
        return res.json();
      })
      .catch((err) => {
        status = err.status;
        return err.json();
      });
    if (status === 200) {
      alert("Login success");
      localStorage.setItem("token", result["access_token"]);
      window.location.href = "/";
    } else {
      console.log(result);
      this.setState({
        error: result["detail"],
      });
    }
  }

  async signUpHandle(e) {
    console.log(this.state.signUp);
    e.preventDefault();
    const info = this.state.signUp;
    if (
      info.username.length === 0 ||
      info.password.length === 0 ||
      info.email.length === 0 ||
      info.first_name.length === 0 ||
      info.last_name.length === 0
    ) {
      alert("Please complete input before submit");
      return false;
    }
    let status = "";
    const data = this.state.signUp;
    let result = await fetch("http://localhost:8000/api/create-user", {
      method: "POST",
      mode: "cors",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((res) => {
        status = res.status;
        return res.json();
      })
      .catch((err) => {
        status = err.status;
        return err.json();
      });
    if (status === 201) {
      alert(result["detail"]);
      window.location.href = "/sign-in";
    } else {
      console.log(result);
      this.setState({
        error: result["detail"],
      });
    }
  }

  render() {
    return (
      <Router>
        <div className="main">
          <Container>
            <div className="main-2">
              <NavBar />
              <Switch>
                <Route path="/sign-in">
                  <SignIn
                    signInClick={this.signInHandle}
                    onchange={this.signInOnchange}
                    error={this.state.error}
                  />
                </Route>
                <Route path="/guide/">
                  <Guide />
                </Route>
                <Route path="/sign-up">
                  <SignUp
                    signUpClick={this.signUpHandle}
                    onchange={this.signUpOnchange}
                    error={this.state.error}
                  />
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
