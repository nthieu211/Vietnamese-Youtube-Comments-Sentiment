import { useState } from "react";
import { NavLink } from "react-router-dom";
import { Navbar, Nav, Container, NavDropdown, Form } from "react-bootstrap";
import ytSentLogo from "/yt-sent.svg";

const Header = () => {
  const [language, setLanguage] = useState("en"); // "en" | "vi"

  return (
    <Navbar expand="md" className="bg-body-tertiary">
      <Container>
        <NavLink to="/" className="navbar-brand">
          <img src={ytSentLogo} height="24" /> VYCS
        </NavLink>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <NavLink to="/" className="nav-link">
              Home
            </NavLink>
            <NavLink to="/model" className="nav-link">
              About Model
            </NavLink>
          </Nav>
          <Nav>
            <NavDropdown
              title={language === "en" ? "English" : "Tiếng Việt"}
              id="basic-nav-dropdown"
            >
              <NavDropdown.Item
                onClick={() => {
                  setLanguage("en");
                }}
              >
                English
              </NavDropdown.Item>
              <NavDropdown.Item
                onClick={() => {
                  setLanguage("vi");
                }}
              >
                Tiếng Việt
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;
