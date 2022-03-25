import React from 'react'
import { Footer } from '../Footer/Footer'
import { Header } from '../Header/Header'
import { Outlet } from 'react-router'

export const Layout = () => {
  return (
    <div>
        <Header />
            <Outlet />
        <Footer />
    </div>
  )
}
