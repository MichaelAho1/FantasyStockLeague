import styles from './LeagueLeaderboard.module.css'

function LeagueLeaderboard() {
  return (
    <div className={styles.leagueSection}>
      <h2>League Leaderboard (Power Rankings)</h2>
      <div className={styles.leaderboard}>
        <ol>
          <li>Team #6 | +$12,000</li>
          <li className={styles.userTeam}>Team #5 | +$11,500</li>
          <li>Team #8 | +$9,400</li>
          <li>Team #1 | +$6,500</li>
          <li>Team #3 | +$6,300</li>
          <li>Team #2 | +$1,200</li>
          <li>Team #4 | -$150</li>
          <li>Team #7 | -$1,300</li>
        </ol>
      </div>
    </div>
  )
}

export default LeagueLeaderboard
