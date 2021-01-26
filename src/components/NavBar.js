import React, { useState } from "react";
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
} from "reactstrap";
import { Link } from "react-router-dom";

const NavBar = (props) => {
  const [collapsed, setCollapsed] = useState(true);
  const isLogin = props.isLogin;
  const logout  = props.logout
  const toggleNavbar = () => setCollapsed(!collapsed);
  return (
    <div>
      {/* <Router> */}
      <Navbar color="faded" light>
        <NavbarBrand
          className="mr-auto text-primary"
          style={{ border: "2px solid gray" }}
        >
          <NavLink href="/">🆂🆄🅱🅻🅸🆂🆃3🆁</NavLink>
        </NavbarBrand>
        <NavbarToggler onClick={toggleNavbar} className="mr-2" />
        <Collapse isOpen={!collapsed} navbar>
          <Nav navbar>
            <NavItem>
              {isLogin === true && (
                <NavLink>
                  <Link to="/" onClick = {logout}>Logout</Link>
                </NavLink>
              )}
              {isLogin === true && (
                <NavLink>
                  <Link to="/user/me">Profile</Link>
                </NavLink>
              )}
              {isLogin === false && (
                <NavLink>
                  <Link to="/sign-in/">Sign In</Link>
                </NavLink>
              )}
              {isLogin === false && (
                <NavLink>
                  <Link to="/sign-up/">Sign Up</Link>
                </NavLink>
              )}
              {isLogin === false && (
                <NavLink>
                  <Link to="/buy/">Buy Now</Link>
                </NavLink>
              )}
              <NavLink>
                <Link to="/guide/">Guide</Link>
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="https://github.com/aboul3la/Sublist3r">
                GitHub
              </NavLink>
            </NavItem>
          </Nav>
        </Collapse>
      </Navbar>
      {/* </Router> */}
      <hr></hr>
    </div>
  );
};

export default NavBar;
