import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import styles from './navBar.module.css';

function navBar() {
  const navigate = useNavigate()

  const handleLogout = () => {
    const confirmed = window.confirm('Are you sure you want to logout?')
    if (confirmed) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('selected_league_id')
      navigate('/Login')
    }
  }

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
            <Link to="/Private/Matchup">Matchup</Link>
          </p>
          <p className={styles.navbarItem}>
            <Link to="/Private/ExploreStocks">Explore Stocks</Link>
          </p>
          <p className={styles.navbarItem}>
            <button className={styles.navbarButton} onClick={handleLogout}>
              Logout
            </button>
          </p>
        </div>
      </nav>
    </>
  )
}

export default navBar