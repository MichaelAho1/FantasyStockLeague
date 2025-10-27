import { useState } from 'react'
import Pagination from '../../../components/Pagination.jsx'
import styles from './MyStocks.module.css'

function MyStocks() {
  const [stocks] = useState([
    { ticker: 'AAPL', name: 'Apple Inc.', startPrice: 150.00, currentPrice: 155.50, shares: 10 },
    { ticker: 'GOOGL', name: 'Alphabet Inc.', startPrice: 2800.00, currentPrice: 2750.00, shares: 2 },
    { ticker: 'MSFT', name: 'Microsoft Corp.', startPrice: 300.00, currentPrice: 315.25, shares: 5 },
    { ticker: 'TSLA', name: 'Tesla Inc.', startPrice: 200.00, currentPrice: 195.75, shares: 8 },
    { ticker: 'AMZN', name: 'Amazon.com Inc.', startPrice: 3200.00, currentPrice: 3250.00, shares: 1 },
    { ticker: 'META', name: 'Meta Platforms Inc.', startPrice: 350.00, currentPrice: 365.80, shares: 3 },
    { ticker: 'NVDA', name: 'NVIDIA Corp.', startPrice: 450.00, currentPrice: 475.25, shares: 4 },
    { ticker: 'NFLX', name: 'Netflix Inc.', startPrice: 425.00, currentPrice: 410.50, shares: 6 },
    { ticker: 'DIS', name: 'Walt Disney Co.', startPrice: 95.00, currentPrice: 98.75, shares: 12 },
    { ticker: 'UBER', name: 'Uber Technologies Inc.', startPrice: 45.00, currentPrice: 47.30, shares: 20 },
    { ticker: 'SPOT', name: 'Spotify Technology S.A.', startPrice: 180.00, currentPrice: 175.40, shares: 8 },
    { ticker: 'SQ', name: 'Block Inc.', startPrice: 65.00, currentPrice: 68.90, shares: 15 },
    { ticker: 'PYPL', name: 'PayPal Holdings Inc.', startPrice: 85.00, currentPrice: 82.15, shares: 10 },
    { ticker: 'ADBE', name: 'Adobe Inc.', startPrice: 520.00, currentPrice: 535.60, shares: 2 },
    { ticker: 'CRM', name: 'Salesforce Inc.', startPrice: 220.00, currentPrice: 225.80, shares: 5 }
  ])

  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 9

  // Calculate totals
  const totalValue = stocks.reduce((sum, stock) => sum + (stock.currentPrice * stock.shares), 0)
  const totalStartValue = stocks.reduce((sum, stock) => sum + (stock.startPrice * stock.shares), 0)
  const totalProfit = totalValue - totalStartValue

  // Calculate pagination
  const totalPages = Math.ceil(stocks.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const currentStocks = stocks.slice(startIndex, endIndex)

  const handlePageChange = (page) => {
    setCurrentPage(page)
  }

  return (
    <div className={styles.myStocksSection}>
      <h2>My Stocks</h2>
      
      <div className={styles.stockTable}>
        <div className={styles.tableHeader}>
          <div>Ticker</div>
          <div>Stock Name</div>
          <div>Start Price</div>
          <div>Current Price</div>
          <div>Profit</div>
          <div>Shares</div>
        </div>
        <div className={styles.stockTableBody}>
          {currentStocks.map((stock, index) => {
            const profit = (stock.currentPrice - stock.startPrice) * stock.shares
            const profitPercent = ((stock.currentPrice - stock.startPrice) / stock.startPrice) * 100
            
            return (
              <div key={index} className={styles.stockRow}>
                <div className={styles.ticker}>{stock.ticker}</div>
                <div className={styles.stockName}>{stock.name}</div>
                <div className={styles.startPrice}>${stock.startPrice.toFixed(2)}</div>
                <div className={styles.currentPrice}>${stock.currentPrice.toFixed(2)}</div>
                <div className={`${styles.profit} ${profit >= 0 ? styles.profitPositive : styles.profitNegative}`}>
                  ${profit.toFixed(2)} ({profitPercent.toFixed(1)}%)
                </div>
                <div className={styles.shares}>{stock.shares}</div>
              </div>
            )
          })}
        </div>
      </div>
      <Pagination 
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={handlePageChange}
      />
      <div className={styles.stockSummary}>
        <div className={styles.summaryItem}>
          <span className={styles.summaryLabel}>Total Stocks Value:</span>
          <span className={styles.summaryValue}>${totalValue.toFixed(2)}</span>
        </div>
        <div className={styles.summaryItem}>
          <span className={styles.summaryLabel}>Total Weekly Profit:</span>
          <span className={`${styles.summaryValue} ${totalProfit >= 0 ? styles.profitPositive : styles.profitNegative}`}>
            {totalProfit >= 0 ? '+' : ''}${totalProfit.toFixed(2)}
          </span>
        </div>
      </div>
    </div>
  )
}

export default MyStocks
