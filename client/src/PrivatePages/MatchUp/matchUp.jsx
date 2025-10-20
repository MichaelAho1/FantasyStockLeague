import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import NavBar from "../components/navBar.jsx"
import styles from "./matchUp.module.css"

function MatchUp() {
  return (
    <>
        <NavBar></NavBar>
        <div className={styles.matchUpContainer}>
            <h1>Match Up</h1>
        </div>
    </>
  )
}

export default MatchUp
