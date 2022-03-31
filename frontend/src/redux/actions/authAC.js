import * as axios from 'axios'
import { toast } from 'react-toastify'
import { useNavigate } from 'react-router-dom'

import {
  SET_TOKEN,
  SET_CURRENT_USER,
  UNSET_CURRENT_USER,
} from './authTypes'
import {
  setAxiosAuthToken,
  toastOnError,
} from '../../utils/Utils'

export const setCurrentUser = (user) => (dispatch) => {
  localStorage.setItem('user', JSON.stringify(user))
  dispatch({
    type: SET_CURRENT_USER,
    payload: user,
  })
}

export const setToken = (token) => (dispatch) => {
  setAxiosAuthToken(token)
  localStorage.setItem('token', token)
  dispatch({
    type: SET_TOKEN,
    payload: token,
  })
}

export const unsetCurrentUser = (dispatch) => {
  setAxiosAuthToken('')
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  dispatch({
    type: UNSET_CURRENT_USER,
  })
}

export const logout = () => (dispatch) => {
  dispatch(unsetCurrentUser())
  useNavigate('/')
  toast.success('Logout successful.')
}

export const login = (userData, redirectTo) => (dispatch) => {
  axios
    .post('/api/token/', userData)
    .then((response) => {
      const { access, user } = response.data
      setAxiosAuthToken(access)
      dispatch(setToken(access))
      dispatch(setCurrentUser(user))
      if (redirectTo !== '') {
        useNavigate(redirectTo)
      }
      toast.success('Login successful.')
    })
    .catch((error) => {
      dispatch(unsetCurrentUser())
      toastOnError(error)
    })
}
