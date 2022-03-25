import React from 'react';
import css from './Button.module.sass';

const Button =  ({ disabled, onClick, name }) => {
  return (
    <button
      disabled={disabled || null} 
      onClick={onClick} 
      className={css.button} 
    >
      {name} 
    </button>
  )
}

export default Button;