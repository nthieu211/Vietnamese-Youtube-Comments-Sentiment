import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";
import { Navbar, Nav, Container, NavDropdown, Form } from "react-bootstrap";
import { useTranslation } from "react-i18next";
import ytSentLogo from "/images/yt-sent.svg";

const Header = () => {
  const { t, i18n } = useTranslation();
  const [language, setLanguage] = useState("en"); // "en" | "vi"
  useEffect(() => {
    i18n.changeLanguage(language);
  }, [language]);

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
              {t("header.home")}
            </NavLink>
            <NavLink to="/model" className="nav-link">
              {t("header.model")}
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
