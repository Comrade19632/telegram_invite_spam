import React from 'react'
import { useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { Outlet } from 'react-router-dom'

const  Authenticate = () => {
        
    const {isAuthenticated } = useSelector(state => ({
        isAuthenticated: state.auth.isAuthenticated,
    }))

    return (
        <div>
            {isAuthenticated === true ? (
              <Outlet />
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
