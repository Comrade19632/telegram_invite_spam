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
         {(this.props.isAuthenticated) ?
          <><Nav.Link onClick={this.onLogout}>Logout</Nav.Link> Вы вошли под аккаунтом - {this.props.user.telegram_id}</>
          : <Link to="/login/">Login</Link>} 
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
