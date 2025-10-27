import { useState } from 'react'
import NavBar from "../components/navBar.jsx"
import SearchBar from "./components/SearchBar.jsx"
import PopularStocks from "./components/PopularStocks.jsx"
import AllStocksList from "./components/AllStocksList.jsx"
import styles from "./exploreStocks.module.css"

function ExploreStocks() {
  const [searchTerm, setSearchTerm] = useState('')
  const [filteredStocks, setFilteredStocks] = useState([])

  const allStocks = [
    { ticker: 'AAPL', name: 'Apple Inc.', price: 155.50, change: 2.5, changePercent: 1.63 },
    { ticker: 'GOOGL', name: 'Alphabet Inc.', price: 2750.00, change: -15.25, changePercent: -0.55 },
    { ticker: 'MSFT', name: 'Microsoft Corp.', price: 315.25, change: 8.75, changePercent: 2.85 },
    { ticker: 'TSLA', name: 'Tesla Inc.', price: 195.75, change: -12.50, changePercent: -6.0 },
    { ticker: 'AMZN', name: 'Amazon.com Inc.', price: 3250.00, change: 45.80, changePercent: 1.43 },
    { ticker: 'META', name: 'Meta Platforms Inc.', price: 365.80, change: 12.30, changePercent: 3.48 },
    { ticker: 'NVDA', name: 'NVIDIA Corp.', price: 475.25, change: 25.50, changePercent: 5.67 },
    { ticker: 'NFLX', name: 'Netflix Inc.', price: 410.50, change: -8.25, changePercent: -1.97 },
    { ticker: 'DIS', name: 'Walt Disney Co.', price: 98.75, change: 3.25, changePercent: 3.41 },
    { ticker: 'UBER', name: 'Uber Technologies Inc.', price: 47.30, change: 1.80, changePercent: 3.96 },
    { ticker: 'SPOT', name: 'Spotify Technology S.A.', price: 175.40, change: -2.60, changePercent: -1.46 },
    { ticker: 'SQ', name: 'Block Inc.', price: 68.90, change: 4.20, changePercent: 6.49 },
    { ticker: 'PYPL', name: 'PayPal Holdings Inc.', price: 82.15, change: -1.85, changePercent: -2.20 },
    { ticker: 'ADBE', name: 'Adobe Inc.', price: 535.60, change: 15.40, changePercent: 2.96 },
    { ticker: 'CRM', name: 'Salesforce Inc.', price: 225.80, change: 5.60, changePercent: 2.54 }
  ]

  const popularStocks = allStocks.slice(0, 8) 

  const handleSearch = (term) => {
    setSearchTerm(term)
    if (term.trim() === '') {
      setFilteredStocks([])
    } else {
      const filtered = allStocks.filter(stock => 
        stock.ticker.toLowerCase().includes(term.toLowerCase()) ||
        stock.name.toLowerCase().includes(term.toLowerCase())
      )
      setFilteredStocks(filtered)
    }
  }

  return (
    <>
        <NavBar></NavBar>
        <div className={styles.exploreStocksContainer}>
            <div className={styles.contentContainer}>
                <div className={styles.leftSide}>
                    <PopularStocks stocks={popularStocks} />
                </div>
                <div className={styles.rightSide}>
                    <AllStocksList 
                        stocks={searchTerm ? filteredStocks : allStocks}
                        searchTerm={searchTerm}
                        onSearch={handleSearch}
                    />
                </div>
            </div>
        </div>
    </>
  )
}

export default ExploreStocks
