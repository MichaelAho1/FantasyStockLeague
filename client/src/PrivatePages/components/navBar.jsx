import { useState } from 'react'
import { Link } from 'react-router-dom';
import styles from './navBar.module.css';

function navBar() {
  return (
    <>
      <nav className={styles.navbar}>
        <div className={styles.navbarLeft}>
          <h1>Fantasy Stock League</h1>
        </div>
        <div className={styles.navbarRight}>
          <p className={styles.navbarItem}>
            <Link to="/Private/Home">Home</Link>
          </p>
          <p className={styles.navbarItem}>
            <Link to="/Private/ExploreStocks">Explore Stocks</Link>
          </p>
          <p className={styles.navbarItem}>
            <Link to="/Private/Matchup">Matchup</Link>
          </p>
          <p className={styles.navbarItem}>
            <Link to="/Private/MyStocks">My Stocks</Link>
          </p>
        </div>
      </nav>
    </>
  )
}

export default navBar