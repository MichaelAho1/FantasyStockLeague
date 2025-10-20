import SearchBar from './SearchBar.jsx'
import styles from './AllStocksList.module.css'

function AllStocksList({ stocks, searchTerm, onSearch }) {
  return (
    <div className={styles.allStocksSection}>
      <div className={styles.sectionHeader}>
        <h2>{searchTerm ? `Search Results (${stocks.length})` : 'All Stocks'}</h2>
        <SearchBar onSearch={onSearch} />
      </div>
      
      <div className={styles.stocksTable}>
        <div className={styles.tableHeader}>
          <div>Ticker</div>
          <div>Company Name</div>
          <div>Price</div>
          <div>Change</div>
          <div>Change %</div>
        </div>
        <div className={styles.stocksTableBody}>
          {stocks.length === 0 ? (
            <div className={styles.noResults}>
              {searchTerm ? `No stocks found for "${searchTerm}"` : 'No stocks available'}
            </div>
          ) : (
            stocks.map((stock, index) => (
              <div key={index} className={styles.stockRow}>
                <div className={styles.ticker}>{stock.ticker}</div>
                <div className={styles.stockName}>{stock.name}</div>
                <div className={styles.price}>${stock.price.toFixed(2)}</div>
                <div className={`${styles.change} ${stock.change >= 0 ? styles.positive : styles.negative}`}>
                  {stock.change >= 0 ? '+' : ''}${stock.change.toFixed(2)}
                </div>
                <div className={`${styles.changePercent} ${stock.changePercent >= 0 ? styles.positive : styles.negative}`}>
                  {stock.changePercent >= 0 ? '+' : ''}{stock.changePercent.toFixed(2)}%
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default AllStocksList
