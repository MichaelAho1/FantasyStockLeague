import { useState, useEffect } from 'react'
import Pagination from '../../../components/Pagination.jsx'
import styles from './MyStocks.module.css'

function MyStocks() {
  const [stocks, setStocks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 9

  useEffect(() => {
    fetchOwnedStocks()
  }, [])

  const fetchOwnedStocks = async () => {
    const leagueId = localStorage.getItem('selected_league_id')
    if (!leagueId) {
      setError('Please select a league first')
      setLoading(false)
      return
    }

    const token = localStorage.getItem('access_token')
    if (!token) {
      setError('Please log in')
      setLoading(false)
      return
    }

    try {
      const response = await fetch(`http://localhost:8000/api/owned-stocks/${leagueId}/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        // Transform data to match component format
        const transformedStocks = data.map(stock => ({
          ticker: stock.ticker,
          name: stock.name,
          startPrice: parseFloat(stock.start_price) || 0,
          currentPrice: parseFloat(stock.current_price) || 0,
          shares: parseFloat(stock.shares) || 0
        }))
        setStocks(transformedStocks)
        setError('')
      } else {
        setError('Failed to load stocks')
        setStocks([])
      }
    } catch (err) {
      console.error('Error fetching owned stocks:', err)
      setError('Network error. Please try again.')
      setStocks([])
    } finally {
      setLoading(false)
    }
  }

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
      
      {loading ? (
        <div className={styles.loading}>Loading stocks...</div>
      ) : error ? (
        <div className={styles.errorMessage}>{error}</div>
      ) : stocks.length === 0 ? (
        <div className={styles.emptyState}>
          <p>You don't own any stocks yet.</p>
          <p>Go to Explore Stocks to start buying!</p>
        </div>
      ) : (
        <>
          <div className={styles.stockTable}>
            <div className={styles.tableHeader}>
              <div>Ticker</div>
              <div>Stock Name</div>
              <div>Day Start Price</div>
              <div>Current Price</div>
              <div>Daily Price Change</div>
              <div>Shares</div>
            </div>
            <div className={styles.stockTableBody}>
              {currentStocks.map((stock, index) => {
                const profit = (stock.currentPrice - stock.startPrice) * stock.shares
                const profitPercent = stock.startPrice !== 0 ? ((stock.currentPrice - stock.startPrice) / stock.startPrice) * 100 : 0
                
                return (
                  <div key={index} className={styles.stockRow}>
                    <div className={styles.ticker}>{stock.ticker}</div>
                    <div className={styles.stockName}>{stock.name}</div>
                    <div className={styles.startPrice}>${stock.startPrice.toFixed(2)}</div>
                    <div className={styles.currentPrice}>${stock.currentPrice.toFixed(2)}</div>
                    <div className={`${styles.profit} ${profit >= 0 ? styles.profitPositive : styles.profitNegative}`}>
                      ${profit.toFixed(2)} ({profitPercent.toFixed(1)}%)
                    </div>
                    <div className={styles.shares}>{stock.shares.toFixed(2)}</div>
                  </div>
                )
              })}
            </div>
          </div>
          {totalPages > 1 && (
            <Pagination 
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={handlePageChange}
            />
          )}
          <div className={styles.stockSummary}>
            <div className={styles.summaryItem}>
              <span className={styles.summaryLabel}>Net Worth:</span>
              <span className={styles.summaryValue}>${totalValue.toFixed(2)}</span>
            </div>
            <div className={styles.summaryItem}>
              <span className={styles.summaryLabel}>Total Weekly Profit:</span>
              <span className={`${styles.summaryValue} ${totalProfit >= 0 ? styles.profitPositive : styles.profitNegative}`}>
                {totalProfit >= 0 ? '+' : ''}${totalProfit.toFixed(2)}
              </span>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default MyStocks
