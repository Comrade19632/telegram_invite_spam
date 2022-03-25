import React from 'react'
import PropTypes from 'prop-types'
import Button from '@mui/material/Button'

const CustomButton = ({
  variant, disabled, onClick, name,
}) => (
    <Button
      sc={{ color: '#fff'}}
      variant={variant}
      disabled={disabled}
      onClick={onClick}
      >
      {name}
    </Button>
)

CustomButton.propTypes = {
  onClick: PropTypes.func.isRequired,
  name: PropTypes.string.isRequired,
  disabled: PropTypes.bool,
  type: PropTypes.string,
}

CustomButton.defaultProps = {
  disabled: false,
  type: 'button',
  variant: 'outlined'
}

export default CustomButton
