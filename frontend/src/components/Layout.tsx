import { ReactNode, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  BarChart3,
  Users,
  FileText,
  Megaphone,
  Calendar,
  MessageSquare,
  LogOut,
  Menu,
  X,
  Building,
  TrendingUp,
  User
} from 'lucide-react'

interface LayoutProps {
  children: ReactNode
  onLogout: () => void
}

const Layout = ({ children, onLogout }: LayoutProps) => {
  const location = useLocation()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  const navigation = [
    { name: 'Dashboard', href: '/', icon: BarChart3 },
    { name: 'Analytics', href: '/analytics', icon: TrendingUp },
    { name: 'Customers', href: '/customers', icon: Users },
    { name: 'Templates', href: '/templates', icon: FileText },
    { name: 'Campaigns', href: '/campaigns', icon: Megaphone },
    { name: 'Messages', href: '/messages', icon: MessageSquare },
    { name: 'Reports', href: '/reports', icon: BarChart3 },
    { name: 'Festivals', href: '/festivals', icon: Calendar },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 flex">
      {sidebarOpen && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm" onClick={() => setSidebarOpen(false)} />
        </div>
      )}

      <div className="flex-1 flex flex-col min-w-0">
        <div className="sticky top-0 z-10 bg-slate-800/95 backdrop-blur-sm border-b border-slate-700 shadow-lg">
          <div className="flex items-center justify-between h-16 px-4">
            <div className="flex items-center">
              <Building className="h-8 w-8 text-blue-400 mr-3" />
              <h1 className="text-lg font-bold text-white">Yashoda Properties</h1>
            </div>
            <div className="flex items-center space-x-2">
              <button
                className="hidden lg:flex text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-700 transition-colors"
                onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              >
                {sidebarCollapsed ? <Menu className="h-6 w-6" /> : <X className="h-6 w-6" />}
              </button>
              <button
                className="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-700 transition-colors lg:hidden"
                onClick={() => setSidebarOpen(!sidebarOpen)}
              >
                {sidebarOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </button>
            </div>
          </div>
        </div>

        <main className="flex-1 p-4 lg:p-6 bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 min-h-screen overflow-auto">
          <div className="max-w-7xl mx-auto">
            {sidebarCollapsed ? (
              <div className="space-y-6">
                <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 rounded-xl p-8 text-white shadow-2xl">
                  <div className="flex items-center justify-between gap-8 flex-wrap">
                    <div>
                      <h1 className="text-4xl font-bold mb-2">Yashoda Properties</h1>
                      <p className="text-xl text-blue-100">Customer Engagement Platform</p>
                      <p className="text-lg text-blue-200 mt-4">Manage your real estate communications with ease</p>
                    </div>
                    <Building className="h-24 w-24 text-blue-200 opacity-80" />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 text-white shadow-xl border border-slate-700">
                    <Users className="h-8 w-8 text-blue-400 mb-3" />
                    <h3 className="text-lg font-semibold mb-2">Customer Management</h3>
                    <p className="text-slate-300 text-sm">Manage your property clients and leads</p>
                  </div>

                  <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 text-white shadow-xl border border-slate-700">
                    <Megaphone className="h-8 w-8 text-emerald-400 mb-3" />
                    <h3 className="text-lg font-semibold mb-2">Campaign Management</h3>
                    <p className="text-slate-300 text-sm">Create and manage marketing campaigns</p>
                  </div>

                  <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 text-white shadow-xl border border-slate-700">
                    <MessageSquare className="h-8 w-8 text-purple-400 mb-3" />
                    <h3 className="text-lg font-semibold mb-2">WhatsApp Messaging</h3>
                    <p className="text-slate-300 text-sm">Send personalized messages to clients</p>
                  </div>

                  <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 text-white shadow-xl border border-slate-700">
                    <BarChart3 className="h-8 w-8 text-amber-400 mb-3" />
                    <h3 className="text-lg font-semibold mb-2">Analytics & Reports</h3>
                    <p className="text-slate-300 text-sm">Track performance and insights</p>
                  </div>
                </div>
              </div>
            ) : (
              children
            )}
          </div>
        </main>
      </div>

      <aside
        className={`hidden lg:flex flex-col bg-gradient-to-b from-slate-800 to-slate-900 shadow-2xl border-l border-slate-700 transition-all duration-300 ease-in-out ${
          sidebarCollapsed ? 'w-20' : 'w-64'
        }`}
      >
        <div className="flex flex-col h-full">
          <div className="flex items-center justify-center h-20 px-4 bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 border-b border-slate-700">
            <div className="flex items-center">
              <Building className="h-10 w-10 text-white mr-3" />
              {!sidebarCollapsed && (
                <div>
                  <h1 className="text-xl font-bold text-white leading-tight">Yashoda</h1>
                  <p className="text-xs text-blue-200 font-medium">Properties</p>
                </div>
              )}
            </div>
          </div>

          <nav className="flex-1 px-3 py-6 space-y-1 overflow-y-auto">
            <div className="mb-6">
              {!sidebarCollapsed && (
                <h3 className="px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Main Menu
                </h3>
              )}
              {navigation.map((item) => {
                const isActive = location.pathname === item.href
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`group flex items-center px-3 py-3 text-sm font-medium rounded-lg transition-all duration-200 ${
                      isActive
                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                        : 'text-slate-300 hover:bg-slate-700 hover:text-white'
                    } ${sidebarCollapsed ? 'justify-center' : ''}`}
                    title={sidebarCollapsed ? item.name : ''}
                  >
                    <item.icon
                      className={`h-5 w-5 transition-colors ${
                        isActive ? 'text-blue-100' : 'text-slate-400 group-hover:text-white'
                      } ${sidebarCollapsed ? '' : 'mr-3'}`}
                    />
                    {!sidebarCollapsed && item.name}
                    {isActive && !sidebarCollapsed && <div className="ml-auto w-2 h-2 bg-white rounded-full" />}
                  </Link>
                )
              })}
            </div>
          </nav>

          <div className="p-4 border-t border-slate-700 bg-slate-800/50">
            <div className={`flex items-center mb-3 ${sidebarCollapsed ? 'justify-center' : ''}`}>
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center shadow-lg">
                <User className="h-5 w-5 text-white" />
              </div>
              {!sidebarCollapsed && (
                <div className="ml-3">
                  <p className="text-sm font-semibold text-white">Admin User</p>
                  <p className="text-xs text-slate-400">Administrator</p>
                </div>
              )}
            </div>
            {!sidebarCollapsed ? (
              <button
                onClick={onLogout}
                className="w-full flex items-center justify-center px-4 py-2 text-sm font-medium text-slate-300 bg-slate-700 rounded-lg border border-slate-600 hover:bg-slate-600 hover:border-slate-500 transition-all duration-200"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </button>
            ) : (
              <button
                onClick={onLogout}
                className="w-full flex items-center justify-center p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg transition-all duration-200"
                title="Logout"
              >
                <LogOut className="h-5 w-5" />
              </button>
            )}
          </div>
        </div>
      </aside>

      <div
        className={`fixed inset-y-0 right-0 z-50 w-64 bg-gradient-to-b from-slate-800 to-slate-900 shadow-2xl border-l border-slate-700 transform transition-all duration-300 ease-in-out lg:hidden ${
          sidebarOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          <div className="flex items-center justify-center h-20 px-4 bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 border-b border-slate-700 relative">
            <div className="flex items-center">
              <Building className="h-10 w-10 text-white mr-3" />
              <div>
                <h1 className="text-xl font-bold text-white leading-tight">Yashoda</h1>
                <p className="text-xs text-blue-200 font-medium">Properties</p>
              </div>
            </div>
            <button
              className="absolute left-4 text-white hover:text-gray-200"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-6 w-6" />
            </button>
          </div>

          <nav className="flex-1 px-3 py-6 space-y-1 overflow-y-auto">
            <div className="mb-6">
              <h3 className="px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Main Menu
              </h3>
              {navigation.map((item) => {
                const isActive = location.pathname === item.href
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    onClick={() => setSidebarOpen(false)}
                    className={`group flex items-center px-3 py-3 text-sm font-medium rounded-lg transition-all duration-200 ${
                      isActive
                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                        : 'text-slate-300 hover:bg-slate-700 hover:text-white'
                    }`}
                  >
                    <item.icon className={`h-5 w-5 transition-colors mr-3 ${
                      isActive ? 'text-blue-100' : 'text-slate-400 group-hover:text-white'
                    }`} />
                    {item.name}
                    {isActive && <div className="ml-auto w-2 h-2 bg-white rounded-full" />}
                  </Link>
                )
              })}
            </div>
          </nav>

          <div className="p-4 border-t border-slate-700 bg-slate-800/50">
            <div className="flex items-center mb-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center shadow-lg">
                <User className="h-5 w-5 text-white" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-semibold text-white">Admin User</p>
                <p className="text-xs text-slate-400">Administrator</p>
              </div>
            </div>
            <button
              onClick={onLogout}
              className="w-full flex items-center justify-center px-4 py-2 text-sm font-medium text-slate-300 bg-slate-700 rounded-lg border border-slate-600 hover:bg-slate-600 hover:border-slate-500 transition-all duration-200"
            >
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Layout
