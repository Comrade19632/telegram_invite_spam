import React, { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';

import style from './HomePage.module.sass';
import { logout } from '../../redux/actions/authAC';
import Button from '../../components/common/Button';

const HomePage = () => {
  
  const navigate = useNavigate()
  
  const {isAuthenticated, user } = useSelector(state => ({
    isAuthenticated: state.auth.isAuthenticated,
    user: state.auth.user
  }))

  const dispatch = useDispatch()

  const onLogout = useCallback((e) => {
    dispatch(logout())
  })

  return (
      <div className={style.container}>
        <h1>Home</h1>
         {(isAuthenticated) ? 
            <>
                <Button 
                    name='Logout'
                    onClick={onLogout}  />
                    <span>
                        Вы вошли под аккаунтом - {user.telegramID}
                    </span>
            </> : 
          <Button 
            name='Login'
            onClick={() => navigate("/login")}
            />
        }
      </div>
    )
}

export default HomePage
