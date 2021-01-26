import "./App.css";
import NavBar from "./components/NavBar";
import { Container } from "reactstrap";
import Footer from "./components/Footer";
import Main from "./components/Main";
import Guide from "./components/Guide";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import Profile from "./components/Profile";
import Pricing from "./components/Pricing";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import React from "react";
import $ from "jquery";
import config from "./config/config";
import PaymentForm from "./components/checkout/Payment"
import Review from "./components/checkout/Review"

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
      isLogin: false,
      user: null,
    };
    this.signInHandle = this.signInHandle.bind(this);
    this.signInOnchange = this.signInOnchange.bind(this);
    this.signUpOnchange = this.signUpOnchange.bind(this);
    this.signUpHandle = this.signUpHandle.bind(this);
    this.logout = this.logout.bind(this);
    this.updateVipAccount = this.updateVipAccount.bind(this)
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
    const formData = new FormData();
    formData.append("username", this.state.signIn.username);
    formData.append("password", this.state.signIn.password);
    // console.log(formData)
    // const data = this.state.signIn;
    let result = await fetch(config.url + config.api + "token", {
      method: "POST",
      mode: "cors",
      credentials: "include",
      // headers: {
      //   "Content-Type": "application/json",
      // },
      // body: JSON.stringify(data),
      body: formData,
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
      this.setState({
        isLogin: true,
      });
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
    let result = await fetch(config.url + config.api + "create-user", {
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
    } else if (status === 422){
      this.setState({
        error: "Service unable"
      })
    } 
    else {
      this.setState({
        error: result["detail"],
      });
    }
  }

  componentDidMount() {
    const token = localStorage.getItem("token");
    if (token == null) {
      this.setState({
        isLogin: false,
      });
      return false;
    }
    $.ajax({
      method: "GET",
      url: config.url + config.api + "users/me",
      credentials: true,
      mode: "cors",
      headers: {
        Authorization: "Bearer " + token,
      },
    })
      .done((res) => {
        this.setState({
          isLogin: true,
          user: { ...res },
        });
      })
      .fail((err) => {
        this.setState({
          isLogin: false,
          user: null,
        });
      });
  }

  logout() {
    localStorage.removeItem("token");
    this.setState({
      isLogin: false,
      user: null,
    });
    window.location.href = "/";
  }

  updateVipAccount(){
    const token = localStorage.getItem("token");
    if (token == null) {
      this.setState({
        isLogin: false,
      });
      window.location.href="/sign-in"
    }
    $.ajax({
      method: "GET",
      url: config.url + config.api + "update-vip-member",
      credentials: true,
      mode: "cors",
      headers: {
        Authorization: "Bearer " + token,
      },
    })
      .done((res) => {
        this.setState({
          isLogin: true,
          user: { ...res },
        });
        alert("Update account successful")
        window.location.href="/user/me"
      })
      .fail((err) => {
        this.setState({
          isLogin: false,
          user: null,
        });
      });
  }

  render() {
    return (
      <Router>
        <div className="main">
          <Container>
            <div className="main-2">
              <NavBar isLogin={this.state.isLogin} logout={this.logout} />
              <Switch>
                <Route path="/buy/">
                  <Pricing />
                </Route>
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
                <Route path="/user/me">
                  <Profile info={this.state.user} isLog={this.isLogin} updateAccount={this.updateVipAccount}/>
                </Route>
                <Route path="/payment/step1">
                  <PaymentForm />
                </Route>
                <Route path="/payment/step2">
                  <Review />
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
