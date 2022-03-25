import React from 'react'
import { Outlet } from 'react-router-dom'

import Footer from 'components/layouts/Footer'
import Header from 'components/layouts/Header'

const Layout = () => (
  <div>
    <Header />
    <Outlet />
    <Footer />
  </div>
)

export default Layout
