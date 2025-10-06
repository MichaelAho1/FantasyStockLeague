import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Signup from "./PublicPages/Signup/signup.jsx"
import Login from "./PublicPages/Login/login.jsx"
import Home from "./PrivatePages/Home/home.jsx"
import ExploreStocks from "./PrivatePages/LeaguePages/ExploreStocks"
import LeagueHomePage from "./PrivatePages/LeaguePages/LeagueHomePage"
import MatchUp from "./PrivatePages/LeaguePages/MatchUp"
import MyStocks from "./PrivatePages/LeaguePages/MyStocks"

function App() {
  return (
    <BrowserRouter>
      {/* These will be Public Pages*/}
      <Route path="/Signup" element={<Signup></Signup>}></Route>
      <Route path="/Login" element={<Login></Login>}></Route>
      {/* These will be Private Pages*/}
      <Route path="/Private/Home" element={<Home></Home>}></Route>
      <Route path="/Private/ExploreStocks" element={<ExploreStocks></ExploreStocks>}></Route>
      <Route path="/Private/LeagueHomePage" element={<LeagueHomePage></LeagueHomePage>}></Route>
      <Route path="/Private/MatchUp" element={<MatchUp></MatchUp>}></Route>
      <Route path="/Private/MyStocks" element={<MyStocks></MyStocks>}></Route>
    </BrowserRouter>
  )
}

export default App
