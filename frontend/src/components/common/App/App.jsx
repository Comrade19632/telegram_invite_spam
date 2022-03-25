import React from 'react';
import { Route, Routes } from 'react-router';
import * as axios from 'axios';

import Login from '../../layouts/Auth/Login/Login';
import HomePage from '../../../containers/HomePage/HomePage';
import { PageNotFound } from '../../../containers/PageNotFound/PageNotFound';
import { Layout } from '../../layouts/Layout/Layout';
import './App.module.sass';

if (window.location.origin === 'http://localhost:3000') {
  axios.defaults.baseURL = 'http://localhost/';
} else {
  axios.defaults.baseURL = window.location.origin;
}

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="*" element={<PageNotFound />} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;
