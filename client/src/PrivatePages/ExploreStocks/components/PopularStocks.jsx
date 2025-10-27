import styles from './PopularStocks.module.css'

function PopularStocks({ stocks }) {
  return (
    <div className={styles.popularSection}>
      <div className={styles.sectionHeader}>
        <h2>Popular Stocks</h2>
      </div>
      <div className={styles.stocksList}>
        {stocks.map((stock, index) => (
          <div key={index} className={styles.stockItem}>
            <div className={styles.stockInfo}>
              <div className={styles.ticker}>{stock.ticker}</div>
              <div className={styles.stockName}>{stock.name}</div>
            </div>
            <div className={styles.stockPrice}>
              <div className={styles.price}>${stock.price.toFixed(2)}</div>
              <div className={`${styles.change} ${stock.change >= 0 ? styles.positive : styles.negative}`}>
                {stock.change >= 0 ? '+' : ''}${stock.change.toFixed(2)} ({stock.changePercent >= 0 ? '+' : ''}{stock.changePercent.toFixed(2)}%)
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default PopularStocks
