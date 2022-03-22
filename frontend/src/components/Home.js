import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Container, Nav } from "react-bootstrap";
import { connect } from "react-redux";
import { logout } from "./login/LoginActions";

class Home extends Component {
  onLogout = () => {
    this.props.logout();
  };

  render() {
    return (
      <Container>
        <h1>Home</h1>
        <p>
          <Link to="/login/">Login</Link>
        </p>
        <Nav.Link onClick={this.onLogout}>Logout</Nav.Link>
        {(this.props.isAuthenticated) ? `Вы вошли под аккаунтом - ${this.props.user.telegram_id}` : null}
      </Container>
    );
  }
}

function mapStateToProps(state){
  return{
    isAuthenticated: state.auth.isAuthenticated,
    user: state.auth.user
  };
}

export default connect(mapStateToProps , {
  logout
})(Home);
