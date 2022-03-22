import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Container } from "react-bootstrap";

class Home extends Component {
  render() {
    return (
      <Container>
        <h1>Home</h1>
        <p>
          <Link to="/login/">Login</Link>
        </p>
      </Container>
    );
  }
}

export default Home;
