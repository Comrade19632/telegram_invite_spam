import Button from 'components/common/Button'
import TelegramLoginButton from '../TelegramLoginButton/TelegramLoginButton/TelegramLoginButton'
import style from './Login.module.sass'

const Login = ({ telegramID, handleAuthentication, updateTelegramID, handleTelegramResponse }) => {
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
              onChange={updateTelegramID}
            />
            <Button 
              type='button'
              name='login' 
              onClick={handleAuthentication} 
            />
          </form>
        </div>
      )}
    </div>
  )
}

export default Login
