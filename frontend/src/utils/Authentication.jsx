import React, { useCallback, useEffect } from 'react'
import { useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { useNavigate } from 'react-router-dom'

const  Authenticate = () => {
    
    const {isAuthenticated, token} = useSelector({
        isAuthenticated: state.auth.isAuthenticated,
        token: state.auth.token,
    })

    const checkAuth = useCallback(() => {
        if (isAuthenticated) {
            const location = useLocation()
            const redirectAfterLogin = location.pathname;
            useNavigate(`/login?next=${redirectAfterLogin}`)
        }
    })
    
    useEffect(checkAuth())

    return (
      <div>
          {isAuthenticated === true ? (
              <div {...props} />
            ) : null}
        </div>
    );
}

Authenticate.propTypes = {
    isAuthenticated: PropTypes.bool.isRequired,
    location: PropTypes.shape({
        pathname: PropTypes.string.isRequired,
    }).isRequired,
    dispatch: PropTypes.func.isRequired,
}

export default Authenticate
