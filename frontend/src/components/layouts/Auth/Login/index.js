import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import Button from 'components/common/Button'
import { login } from 'redux/actions/authAC'
import TelegramLoginButton from '../TelegramLoginButton/TelegramLoginButton/TelegramLoginButton'
import style from './Login.module.sass'

const Login = () => {
  const [telegramID, setTelegramID] = useState(useSelector((state) => state.telegramID))

  const dispatch = useDispatch()

  const onChange = (e) => {
    setTelegramID(e.target.value)
  }

  const onLoginClick = () => {
    const userData = {
      id: telegramID,
    }

    dispatch(login(userData, '/'))
  }

  const handleTelegramResponse = (userData) => {
    login(userData, '/')
  }

  return (
    <div>
      {(process.env.NODE_ENV === 'production') ? <TelegramLoginButton dataOnauth={handleTelegramResponse} /> : (
        <div className={style.container}>
          <h1>Login</h1>
          <form className={style.form}>
            <label>Your telegram_id</label>
            <input
              type="text"
              name="telegramID"
              placeholder="Enter telegram_id"
              value={telegramID}
              onChange={onChange}
            />
            <Button name="Login" onClick={onLoginClick} />
          </form>
        </div>
      )}
    </div>
  )
}

export default Login
