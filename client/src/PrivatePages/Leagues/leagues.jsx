import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import NavBar from '../components/navBar.jsx'
import styles from './leagues.module.css'

function Leagues() {
  const [username, setUsername] = useState('')
  const [leagues, setLeagues] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showJoinModal, setShowJoinModal] = useState(false)
  const [leagueName, setLeagueName] = useState('')
  const [startDate, setStartDate] = useState('')
  const [joinLeagueId, setJoinLeagueId] = useState('')
  const navigate = useNavigate()

  // Fetch user leagues
  const fetchLeagues = async () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      navigate('/Login')
      return
    }

    try {
      const response = await fetch('http://localhost:8000/api/leagues/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const data = await response.json()
        setLeagues(data)
      } else if (response.status === 404) {
        // Endpoint might not exist yet, set empty array
        setLeagues([])
      } else {
        setError('Failed to load leagues')
      }
    } catch (err) {
      console.error('Error fetching leagues:', err)
      setLeagues([]) // Set empty array on error
    } finally {
      setLoading(false)
    }
  }

  // Get username from localStorage
  useEffect(() => {
    const storedUsername = localStorage.getItem('username')
    if (storedUsername) {
      setUsername(storedUsername)
    }
    fetchLeagues()
  }, [])

  // Handle create league
  const handleCreateLeague = async (e) => {
    e.preventDefault()
    const token = localStorage.getItem('access_token')
    
    if (!leagueName.trim()) {
      setError('League name is required')
      return
    }

    if (!startDate) {
      setError('Start date is required')
      return
    }

    try {
      const response = await fetch('http://localhost:8000/api/leagues/create/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: leagueName,
          start_date: startDate,
        }),
      })

      if (response.ok) {
        setShowCreateModal(false)
        setLeagueName('')
        setStartDate('')
        setError('')
        fetchLeagues() // Refresh leagues list
      } else {
        const errorData = await response.json()
        setError(errorData.detail || 'Failed to create league')
      }
    } catch (err) {
      setError('Network error. Please try again.')
    }
  }

  // Handle join league
  const handleJoinLeague = async (e) => {
    e.preventDefault()
    const token = localStorage.getItem('access_token')
    
    if (!joinLeagueId.trim()) {
      setError('League ID is required')
      return
    }

    try {
      const response = await fetch('http://localhost:8000/api/leagues/join/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          league_id: joinLeagueId,
        }),
      })

      if (response.ok) {
        setShowJoinModal(false)
        setJoinLeagueId('')
        setError('')
        fetchLeagues() // Refresh leagues list
      } else {
        const errorData = await response.json()
        setError(errorData.detail || 'Failed to join league')
      }
    } catch (err) {
      setError('Network error. Please try again.')
    }
  }

  // Handle league click - navigate to home with selected league
  const handleLeagueClick = (leagueId) => {
    localStorage.setItem('selected_league_id', leagueId)
    navigate('/Private/Home')
  }

  return (
    <>
      <NavBar />
      <div className={styles.leaguesContainer}>
        <div className={styles.leaguesContent}>
          <div className={styles.header}>
            <h1 className={styles.welcomeText}>
              Welcome, <span className={styles.username}>{username || 'User'}</span>!
            </h1>
            <p className={styles.subtitle}>Manage your fantasy stock leagues</p>
          </div>

          {error && <div className={styles.errorMessage}>{error}</div>}

          <div className={styles.actions}>
            <button
              className={styles.createButton}
              onClick={() => {
                setShowCreateModal(true)
                setError('')
              }}
            >
              Create League
            </button>
            <button
              className={styles.joinButton}
              onClick={() => {
                setShowJoinModal(true)
                setError('')
              }}
            >
              Join League
            </button>
          </div>

          <div className={styles.leaguesSection}>
            <h2 className={styles.sectionTitle}>Your Leagues</h2>
            {loading ? (
              <div className={styles.loading}>Loading leagues...</div>
            ) : leagues.length === 0 ? (
              <div className={styles.emptyState}>
                <p>You're not in any leagues yet.</p>
                <p>Create a new league or join an existing one to get started!</p>
              </div>
            ) : (
              <div className={styles.leaguesGrid}>
                {leagues.map((league) => (
                  <div
                    key={league.league_id}
                    className={styles.leagueCard}
                    onClick={() => handleLeagueClick(league.league_id)}
                  >
                    <h3 className={styles.leagueName}>{league.name}</h3>
                    <div className={styles.leagueInfo}>
                      <p className={styles.leagueDetail}>
                        <span className={styles.label}>Start Date:</span> {new Date(league.start_date).toLocaleDateString()}
                      </p>
                      <p className={styles.leagueDetail}>
                        <span className={styles.label}>End Date:</span> {new Date(league.end_date).toLocaleDateString()}
                      </p>
                      <p className={styles.leagueDetail}>
                        <span className={styles.label}>Status:</span>{' '}
                        <span className={league.is_active ? styles.active : styles.inactive}>
                          {league.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Create League Modal */}
      {showCreateModal && (
        <div className={styles.modalOverlay} onClick={() => setShowCreateModal(false)}>
          <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
            <h2>Create New League</h2>
            <form onSubmit={handleCreateLeague}>
              <div className={styles.formGroup}>
                <label htmlFor="leagueName">League Name</label>
                <input
                  type="text"
                  id="leagueName"
                  value={leagueName}
                  onChange={(e) => setLeagueName(e.target.value)}
                  placeholder="Enter league name"
                  required
                />
              </div>
              <div className={styles.formGroup}>
                <label htmlFor="startDate">Start Date</label>
                <input
                  type="date"
                  id="startDate"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  required
                />
              </div>
              <div className={styles.modalActions}>
                <button type="button" className={styles.cancelButton} onClick={() => setShowCreateModal(false)}>
                  Cancel
                </button>
                <button type="submit" className={styles.submitButton}>
                  Create League
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Join League Modal */}
      {showJoinModal && (
        <div className={styles.modalOverlay} onClick={() => setShowJoinModal(false)}>
          <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
            <h2>Join League</h2>
            <form onSubmit={handleJoinLeague}>
              <div className={styles.formGroup}>
                <label htmlFor="leagueId">League ID</label>
                <input
                  type="text"
                  id="leagueId"
                  value={joinLeagueId}
                  onChange={(e) => setJoinLeagueId(e.target.value)}
                  placeholder="Enter league ID"
                  required
                />
              </div>
              <div className={styles.modalActions}>
                <button type="button" className={styles.cancelButton} onClick={() => setShowJoinModal(false)}>
                  Cancel
                </button>
                <button type="submit" className={styles.submitButton}>
                  Join League
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  )
}

export default Leagues

