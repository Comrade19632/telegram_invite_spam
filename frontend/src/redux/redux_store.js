import { applyMiddleware, combineReducers, createStore } from 'redux'
import thunkMiddleWare from 'redux-thunk'
import authReducer from './reducers/authReducer'

/// /
// all reducers are combined here
// then passed to the store
/// /

const reducers = combineReducers({
  auth: authReducer,
})

const store = createStore(reducers, applyMiddleware(thunkMiddleWare))

export default store

/// /
// thunkMiddleWare is a function,
// that can act asynchronosly and dispatch actions
/// /

/// /
// window.store = store
// allows store.getState() in the browser console
// for easier debugging process
/// /
