import styles from './Schedule.module.css'

function Schedule() {
  return (
    <div className={styles.scheduleSection}>
      <h2>Schedule</h2>
      <div className={styles.schedule}>
        <div className={styles.scheduleList}>
          <div className={styles.gameItem}>Week 1: Team #1 vs Team #3</div>
          <div className={`${styles.gameItem} ${styles.currentWeek}`}>Week 2: Team #1 vs Team #7</div>
          <div className={styles.gameItem}>Week 3: Team #1 vs Team #5</div>
          <div className={styles.gameItem}>Week 4: Team #1 vs Team #6</div>
          <div className={styles.gameItem}>Week 5: Team #1 vs Team #8</div>
        </div>
      </div>
    </div>
  )
}

export default Schedule
