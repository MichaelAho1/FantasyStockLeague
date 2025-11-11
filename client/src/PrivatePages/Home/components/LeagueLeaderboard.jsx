import styles from './LeagueLeaderboard.module.css'

function LeagueLeaderboard() {
  return (
    <div className={styles.leagueSection}>
      <h2>League Leaderboard (Power Rankings)</h2>
      <div className={styles.leaderboard}>
        <ol>
          <li>Team #6 | 10 - 1</li>
          <li className={styles.userTeam}>Team #5 | 10 - 1</li>
          <li>Team #8 | 9 - 2</li>
          <li>Team #1 | 6 - 5</li>
          <li>Team #3 | 5 - 6</li>
          <li>Team #2 | 2 - 9</li>
          <li>Team #4 | 1 - 10</li>
          <li>Team #7 | 1 - 10</li>
        </ol>
      </div>
    </div>
  )
}

export default LeagueLeaderboard
