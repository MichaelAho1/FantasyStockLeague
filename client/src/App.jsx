import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Signup from "./PublicPages/Signup/signup.jsx"
import Login from "./PublicPages/Login/login.jsx"
import Home from "./PrivatePages/Home/home.jsx"

import MatchUp from "./PrivatePages/MatchUp/matchUp.jsx"
import ExploreStocks from "./PrivatePages/ExploreStocks/exploreStocks.jsx"

function App() {
  return (
      <BrowserRouter>
        <Routes>
        <Route path="/Signup" element={<Signup></Signup>}></Route>
        <Route path="/Login" element={<Login></Login>}></Route>

        <Route path="/Private/Home" element={<Home></Home>}></Route>
        <Route path="/Private/MatchUp" element={<MatchUp></MatchUp>}></Route>
        <Route path="/Private/ExploreStocks" element={<ExploreStocks></ExploreStocks>}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
