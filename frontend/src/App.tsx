import { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Login from './components/Login'
import DashboardPage from './pages/DashboardPage'
import CustomersPage from './pages/CustomersPage'
import TemplatesPage from './pages/TemplatesPage'
import CampaignsPage from './pages/CampaignsPage'
import FestivalsPage from './pages/FestivalsPage'
import CustomerDetailPage from './pages/CustomerDetailPage'
import MessagesPage from './pages/MessagesPage'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    setIsAuthenticated(Boolean(localStorage.getItem('access_token')))
    setIsLoading(false)
  }, [])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 flex items-center justify-center text-white">
        <div className="text-center space-y-3 p-6 rounded-3xl bg-slate-900/80 border border-slate-700 shadow-2xl">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent mx-auto" />
          <h3 className="text-base font-semibold">Loading...</h3>
          <p className="text-sm text-slate-300">Initializing the dashboard experience</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 flex items-center justify-center px-4 py-10">
        <Login onLogin={() => setIsAuthenticated(true)} />
      </div>
    )
  }

  return (
    <BrowserRouter>
      <Layout onLogout={() => setIsAuthenticated(false)}>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/customers" element={<CustomersPage />} />
          <Route path="/customers/:id" element={<CustomerDetailPage />} />
          <Route path="/templates" element={<TemplatesPage />} />
          <Route path="/campaigns" element={<CampaignsPage />} />
          <Route path="/festivals" element={<FestivalsPage />} />
          <Route path="/messages" element={<MessagesPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
