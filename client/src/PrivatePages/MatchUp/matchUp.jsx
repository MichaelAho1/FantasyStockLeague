import { useState } from 'react'
import NavBar from "../components/navBar.jsx"
import TeamCard from "./components/TeamCard.jsx"
import styles from "./matchUp.module.css"

function MatchUp() {
  // Sample matchup data - in a real app this would come from props or API
  const [matchup] = useState({
    player1: {
      name: "Team #5",
      value: 125000,
      profit: 11500,
      record: "8-2",
      stocks: [
        { ticker: 'AAPL', profit: 5500 },
        { ticker: 'GOOGL', profit: 3200 },
        { ticker: 'MSFT', profit: 2800 },
        { ticker: 'TSLA', profit: 4200 },
        { ticker: 'NVDA', profit: 3800 },
        { ticker: 'META', profit: 2900 },
        { ticker: 'AMZN', profit: 2100 },
        { ticker: 'NFLX', profit: 1800 },
        { ticker: 'DIS', profit: 1200 },
        { ticker: 'UBER', profit: 800 },
        { ticker: 'SPOT', profit: 650 },
        { ticker: 'SQ', profit: 420 },
        { ticker: 'PYPL', profit: 380 },
        { ticker: 'ADBE', profit: 290 },
        { ticker: 'CRM', profit: 150 }
      ]
    },
    player2: {
      name: "Team #6", 
      value: 132000,
      profit: 12000,
      record: "9-1",
      stocks: [
        { ticker: 'TSLA', profit: 4500 },
        { ticker: 'NVDA', profit: 3800 },
        { ticker: 'META', profit: 3700 },
        { ticker: 'AAPL', profit: 3200 },
        { ticker: 'GOOGL', profit: 2800 },
        { ticker: 'MSFT', profit: 2500 },
        { ticker: 'AMZN', profit: 2200 },
        { ticker: 'NFLX', profit: 1900 },
        { ticker: 'DIS', profit: 1500 },
        { ticker: 'UBER', profit: 900 },
        { ticker: 'SPOT', profit: 750 },
        { ticker: 'SQ', profit: 580 },
        { ticker: 'PYPL', profit: 450 },
        { ticker: 'ADBE', profit: 320 },
        { ticker: 'CRM', profit: 200 }
      ]
    }
  })

  return (
    <>
        <NavBar></NavBar>
        <div className={styles.matchUpContainer}>
            <div className={styles.matchupHeader}>
                <h1>Week 2</h1>
            </div>
            
            <div className={styles.teamsContainer}>
                <TeamCard 
                    team={matchup.player1} 
                    isPlayer1={true}
                />
                <TeamCard 
                    team={matchup.player2} 
                    isPlayer1={false}
                />
            </div>
        </div>
    </>
  )
}

export default MatchUp
