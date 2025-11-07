import { BrowserRouter, Routes, Route } from "react-router-dom"
import Signup from "./PublicPages/Signup/signup.jsx"
import Login from "./PublicPages/Login/login.jsx"
import Home from "./PrivatePages/Home/home.jsx"
import ProtectedRoute from "./components/protectedRoute.jsx"
import MatchUp from "./PrivatePages/MatchUp/matchUp.jsx"
import ExploreStocks from "./PrivatePages/ExploreStocks/exploreStocks.jsx"
import Leagues from "./PrivatePages/Leagues/leagues.jsx"

function App() {
  return (
      <BrowserRouter>
        <Routes>
        <Route path="/Signup" element={<Signup></Signup>}></Route>
        <Route path="/Login" element={<Login></Login>}></Route>

        <Route path="/Private/Leagues" element={<ProtectedRoute><Leagues></Leagues></ProtectedRoute>}></Route>
        <Route path="/Private/Home" element={<ProtectedRoute><Home></Home></ProtectedRoute>}></Route>
        <Route path="/Private/MatchUp" element={<ProtectedRoute><MatchUp></MatchUp></ProtectedRoute>}></Route>
        <Route path="/Private/ExploreStocks" element={<ProtectedRoute><ExploreStocks></ExploreStocks></ProtectedRoute>}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
