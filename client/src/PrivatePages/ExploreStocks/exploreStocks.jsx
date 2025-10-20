import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import NavBar from "../components/navBar.jsx"
import styles from "./exploreStocks.module.css"

function ExploreStocks() {
  return (
    <>
        <NavBar></NavBar>
        <div className={styles.exploreStocksContainer}>
            <h1>Explore Stocks</h1>
        </div>
    </>
  )
}

export default ExploreStocks
