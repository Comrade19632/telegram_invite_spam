import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { login } from 'redux/actions/authAC'
import Login from 'components/layouts/Auth/Login'

const LoginPage = () => {
  const [telegramID, setTelegramID] = useState('')
  const dispatch = useDispatch()

  const updateTelegramID = (e) => {
    setTelegramID(e.target.value)
  }
  const navigate = useNavigate()
  const handleAuthentication = () => {
    const userData = {
      id: telegramID,
    }
    dispatch(login(userData, '/', navigate))
  }

  const handleTelegramResponse = (userData) => {
    dispatch(
      login(userData, '/')
    )
  }

  return <Login 
            telegramID={telegramID}
            handleAuthentication={handleAuthentication}
            updateTelegramID={updateTelegramID}
            handleTelegramResponse={handleTelegramResponse}
        />
   
}

export default LoginPage
