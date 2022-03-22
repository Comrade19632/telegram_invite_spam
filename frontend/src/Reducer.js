import { combineReducers } from "redux";
import { connectRouter } from "connected-react-router";

import { loginReducer } from "./components/login/LoginReducer";

const createRootReducer = history =>
  combineReducers({
    router: connectRouter(history),
    auth: loginReducer,
  });

export default createRootReducer;
