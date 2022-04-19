import * as React from 'react';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Title from '../Title';

function preventDefault(event) {
  event.preventDefault();
}

const  Deposits = ({balance}) => {
  const today = new Date().toLocaleDateString()

  return (
    <React.Fragment>
      <Title>Баланс</Title>
      <Typography component="p" variant="h4">
        {`${balance} RUB`}
      </Typography>
      <Typography color="text.secondary" sx={{ 
flex: 1 }}>
        {today}
      </Typography>
      <div>
        <Link color="primary" href="#" 
onClick={preventDefault}>
          История зачислений
        </Link>
      </div>
    </React.Fragment>
  );
}

Deposits.defaultProps = {
  balance: '3 200 02'
}
export default Deposits
