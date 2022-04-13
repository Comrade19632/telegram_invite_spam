import React from 'react'
import PropTypes from 'prop-types'

import css from './Button.module.sass'

const Button = ({
  type, disabled, onClick, name,
}) => (
  <button
    /* eslint-disable-next-line react/button-has-type */
    type={type}
    disabled={disabled && null}
    onClick={onClick}
    className={css.button}
  >
    {name}
  </button>
)

Button.propTypes = {
  onClick: PropTypes.func.isRequired,
  name: PropTypes.string.isRequired,
  disabled: PropTypes.bool,
  type: PropTypes.string,
}

Button.defaultProps = {
  disabled: null,
  type: 'button',
}

export default Button
