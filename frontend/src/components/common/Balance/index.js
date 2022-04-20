import * as React from 'react'
import Link from '@mui/material/Link'
import Typography from '@mui/material/Typography'
import PropTypes from 'prop-types'
import Title from '../Title'

const preventDefault = (event) => {
  event.preventDefault()
}

const Deposits = ({ balance }) => {
  const today = new Date().toLocaleDateString()
  return (
    <>
      <Title>Баланс</Title>
      <Typography component="p" variant="h4">
        {`${balance} RUB`}
      </Typography>
      <Typography
        color="text.secondary"
        sx={{flex: 1}}>
        {today}
      </Typography>
      <div>
        <Link 
          color="primary" 
          href="#" 
          onClick={preventDefault}>
          История зачислений
        </Link>
      </div>
    </>
  )
}

Deposits.propTypes = {
  balance: PropTypes.number
}

Deposits.defaultProps = {
  balance: 0,
}

export default Deposits
