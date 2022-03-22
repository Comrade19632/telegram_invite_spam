import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { Container, Button, Row, Col, Form } from "react-bootstrap";
import TelegramLoginButton from './components/TelegramLoginButton'

import { login } from "./LoginActions.js";

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      telegram_id: "",
    };
  }
  onChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  onLoginClick = () => {
    const userData = {
      id: this.state.telegram_id,
    };
    this.props.login(userData, "/");
  };

  handleTelegramResponse = (userData) => {
    this.props.login(userData, "/");
  }

  render() {
    return (
      <Container>
      {(process.env.NODE_ENV == "production") ? <TelegramLoginButton dataOnauth={this.handleTelegramResponse} /> :
        <Row>
          <Col md="4">
            <h1>Login</h1>
            <Form>
              <Form.Group controlId="telegram_idId">
                <Form.Label>Your telegram_id</Form.Label>
                <Form.Control
                  type="text"
                  name="telegram_id"
                  placeholder="Enter telegram_id"
                  value={this.state.telegram_id}
                  onChange={this.onChange}
                />
              </Form.Group>
            </Form>
            <Button color="primary" onClick={this.onLoginClick}>
              Login
            </Button>
          </Col>
        </Row>}
      </Container>
    );
  }
}

//export default Login;
Login.propTypes = {
  login: PropTypes.func.isRequired,
  auth: PropTypes.object.isRequired
};

const mapStateToProps = state => ({
  auth: state.auth
});

export default connect(mapStateToProps, {
  login
})(withRouter(Login));
