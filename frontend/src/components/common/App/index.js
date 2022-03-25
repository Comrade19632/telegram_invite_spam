import React from 'react'
import { Route, Routes } from 'react-router-dom'
import * as axios from 'axios'

import Login from 'components/layouts/Auth/Login'
import HomePage from 'containers/HomePage'
import PageNotFound from 'containers/PageNotFound'
import Layout from 'components/layouts/Layout'
import './App.module.sass'

if (window.location.origin === 'http://localhost:3000') {
  axios.defaults.baseURL = 'http://localhost/'
} else {
  axios.defaults.baseURL = window.location.origin
}

const App = () => (
  <div className="App">
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<PageNotFound />} />
      </Route>
    </Routes>
  </div>
)

export default App
