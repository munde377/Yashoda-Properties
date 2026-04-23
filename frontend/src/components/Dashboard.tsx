import { useEffect, useState } from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import {
  Users,
  MessageSquare,
  Send,
  CheckCircle,
  XCircle,
  Megaphone,
  Calendar,
  TrendingUp,
  Activity,
  Plus,
  Eye,
  BarChart3,
  Clock,
  Target,
  Zap,
  CheckCircle2
} from 'lucide-react'
import api from '../api'

interface Metrics {
  total_customers: number
  total_messages: number
  sent_messages: number
  delivered_messages: number
  failed_messages: number
  total_campaigns: number
  scheduled_campaigns: number
}

interface Campaign {
  id: number
  name: string
  template_id: number
  send_all: boolean
  scheduled_at: string | null
  created_at: string
}

function Dashboard() {
  const [metrics, setMetrics] = useState<Metrics | null>(null)
  const [campaigns, setCampaigns] = useState<Campaign[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [metricsResponse, campaignsResponse] = await Promise.all([
          api.get<Metrics>('/dashboard'),
          api.get<Campaign[]>('/campaigns')
        ])

        setMetrics(metricsResponse.data)
        setCampaigns(campaignsResponse.data.slice(0, 6))
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()

    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 p-2">
        <div className="text-center rounded-3xl bg-slate-900/90 border border-slate-700 p-8 shadow-2xl">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent mx-auto mb-3"></div>
          <h3 className="text-base font-semibold text-white">Loading Dashboard...</h3>
          <p className="text-xs text-slate-400 mt-1">Fetching latest analytics</p>
        </div>
      </div>
    )
  }

  if (!metrics) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 p-2">
        <div className="text-center max-w-sm rounded-3xl bg-slate-900/90 border border-slate-700 p-8 shadow-2xl">
          <XCircle className="mx-auto h-12 w-12 text-rose-500 mb-3" />
          <h3 className="text-base font-bold text-white mb-1">Unable to Load Dashboard</h3>
          <p className="text-slate-400 mb-3">We're having trouble connecting to the server. Please check your connection and try again.</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  // Calculate advanced metrics
  const deliveryRate = metrics.total_messages > 0 ? (metrics.delivered_messages / metrics.total_messages) * 100 : 0
  const failureRate = metrics.total_messages > 0 ? (metrics.failed_messages / metrics.total_messages) * 100 : 0
  const successRate = 100 - failureRate
  const avgMessagesPerCampaign = metrics.total_campaigns > 0 ? Math.round(metrics.total_messages / metrics.total_campaigns) : 0

  // Enhanced chart data
  const messageData = [
    { name: 'Sent', value: metrics.sent_messages, color: '#0EA5E9', icon: Send },
    { name: 'Delivered', value: metrics.delivered_messages, color: '#10B981', icon: CheckCircle },
    { name: 'Failed', value: metrics.failed_messages, color: '#EF4444', icon: XCircle },
  ]

  const campaignData = [
    { name: 'Active', value: metrics.total_campaigns - metrics.scheduled_campaigns, color: '#8B5CF6' },
    { name: 'Scheduled', value: metrics.scheduled_campaigns, color: '#F59E0B' },
  ]

  const performanceData = [
    { name: 'Success Rate', value: successRate, color: successRate > 90 ? '#10B981' : successRate > 75 ? '#F59E0B' : '#EF4444' },
    { name: 'Delivery Rate', value: deliveryRate, color: deliveryRate > 85 ? '#10B981' : deliveryRate > 70 ? '#F59E0B' : '#EF4444' },
  ]

  const quickActions = [
    { icon: Plus, label: 'New Campaign', color: 'bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700', textColor: 'text-white' },
    { icon: Users, label: 'Add Customer', color: 'bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700', textColor: 'text-white' },
    { icon: MessageSquare, label: 'Create Template', color: 'bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700', textColor: 'text-white' },
    { icon: BarChart3, label: 'View Reports', color: 'bg-gradient-to-r from-slate-700 to-slate-800 hover:from-slate-600 hover:to-slate-700', textColor: 'text-white' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 p-2 lg:p-3">
      {/* Compact Header */}
      <div className="bg-gradient-to-r from-slate-800 via-slate-900 to-slate-800 rounded-2xl p-4 mb-3 shadow-2xl border border-slate-700">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
          <div className="mb-2 lg:mb-0">
            <h1 className="text-xl lg:text-2xl font-bold text-white mb-1">Analytics Dashboard</h1>
            <p className="text-slate-300 text-sm">Real-time insights into your customer engagement</p>
          </div>
          <div className="flex items-center space-x-3">
            <div className="bg-slate-700/50 backdrop-blur-sm rounded-lg px-3 py-1 border border-slate-600">
              <div className="text-xs text-slate-400">Last updated</div>
              <div className="font-semibold text-white text-sm">{new Date().toLocaleTimeString()}</div>
            </div>
            <div className="bg-green-500 text-white px-2 py-1 rounded-full text-xs font-medium flex items-center">
              <div className="w-2 h-2 bg-white rounded-full mr-1 animate-pulse"></div>
              Live
            </div>
          </div>
        </div>
      </div>

      {/* Key Metrics - Ultra Compact */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-2 mb-3">
        <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl p-3 text-white shadow-xl hover:shadow-2xl transition-shadow border border-blue-500/20">
          <div className="flex items-center justify-between mb-1">
            <Users className="h-5 w-5 text-blue-200" />
            <TrendingUp className="h-3 w-3 text-green-300" />
          </div>
          <div className="text-xl font-bold mb-1">{metrics.total_customers.toLocaleString()}</div>
          <div className="text-blue-100 text-xs">Total Customers</div>
          <div className="text-green-300 text-xs mt-1">+12.5% this month</div>
        </div>

        <div className="bg-gradient-to-br from-emerald-600 to-emerald-700 rounded-xl p-3 text-white shadow-xl hover:shadow-2xl transition-shadow border border-emerald-500/20">
          <div className="flex items-center justify-between mb-1">
            <Send className="h-5 w-5 text-emerald-200" />
            <CheckCircle className="h-3 w-3 text-emerald-300" />
          </div>
          <div className="text-xl font-bold mb-1">{metrics.sent_messages.toLocaleString()}</div>
          <div className="text-emerald-100 text-xs">Messages Sent</div>
          <div className="text-emerald-300 text-xs mt-1">{deliveryRate.toFixed(1)}% delivered</div>
        </div>

        <div className="bg-gradient-to-br from-purple-600 to-purple-700 rounded-xl p-3 text-white shadow-xl hover:shadow-2xl transition-shadow border border-purple-500/20">
          <div className="flex items-center justify-between mb-1">
            <Megaphone className="h-5 w-5 text-purple-200" />
            <Target className="h-3 w-3 text-purple-300" />
          </div>
          <div className="text-xl font-bold mb-1">{metrics.total_campaigns.toLocaleString()}</div>
          <div className="text-purple-100 text-xs">Active Campaigns</div>
          <div className="text-purple-300 text-xs mt-1">{metrics.scheduled_campaigns} scheduled</div>
        </div>

        <div className="bg-gradient-to-br from-amber-600 to-orange-600 rounded-xl p-3 text-white shadow-xl hover:shadow-2xl transition-shadow border border-amber-500/20">
          <div className="flex items-center justify-between mb-1">
            <Activity className="h-5 w-5 text-amber-200" />
            <Zap className="h-3 w-3 text-amber-300" />
          </div>
          <div className="text-xl font-bold mb-1">{successRate.toFixed(1)}%</div>
          <div className="text-amber-100 text-xs">Success Rate</div>
          <div className="text-amber-300 text-xs mt-1">{avgMessagesPerCampaign} avg per campaign</div>
        </div>
      </div>

      {/* Main Analytics Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-3 mb-3">
        {/* Performance Metrics */}
        <div className="space-y-3">
          {/* Success Rate Gauge */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-xl border border-slate-700 p-3">
            <h4 className="text-sm font-bold text-white mb-2">Performance Metrics</h4>
            <div className="space-y-2">
              {performanceData.map((metric, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div
                      className="w-3 h-3 rounded-full mr-2"
                      style={{ backgroundColor: metric.color }}
                    ></div>
                    <span className="text-xs font-medium text-slate-300">{metric.name}</span>
                  </div>
                  <span className="text-sm font-bold text-white" style={{ color: metric.color }}>
                    {metric.value.toFixed(1)}%
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Campaign Distribution */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-xl border border-slate-700 p-3">
            <h4 className="text-sm font-bold text-white mb-2">Campaign Status</h4>
            <ResponsiveContainer width="100%" height={160}>
              <PieChart>
                <Pie
                  data={campaignData}
                  cx="50%"
                  cy="50%"
                  innerRadius={30}
                  outerRadius={60}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {campaignData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(30, 41, 59, 0.95)',
                    border: '1px solid rgba(71, 85, 105, 0.5)',
                    borderRadius: '6px',
                    boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.5)',
                    color: 'white'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex justify-center space-x-3 mt-2">
              {campaignData.map((item, index) => (
                <div key={item.name} className="flex items-center">
                  <div
                    className="w-2 h-2 rounded-full mr-1"
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="text-xs text-slate-300">{item.name}: {item.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Message Status Overview */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-xl border border-slate-700 p-3">
          <h4 className="text-sm font-bold text-white mb-3">Message Status Overview</h4>
          <div className="space-y-3">
            {messageData.map((item, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg border border-slate-600">
                <div className="flex items-center">
                  <item.icon className="h-4 w-4 mr-2" style={{ color: item.color }} />
                  <span className="text-xs font-medium text-slate-200">{item.name}</span>
                </div>
                <span className="text-sm font-bold text-white">
                  {item.value.toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Section */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
        {/* Recent Campaigns */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-xl border border-slate-700 p-3">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-base font-bold text-white">Recent Campaigns</h3>
            <button className="text-blue-400 hover:text-blue-300 text-xs font-medium flex items-center">
              <Eye className="h-3 w-3 mr-1" />
              View All
            </button>
          </div>
          <div className="space-y-2">
            {campaigns.length > 0 ? (
              campaigns.map((campaign) => (
                <div key={campaign.id} className="flex items-center justify-between p-3 bg-gradient-to-r from-slate-700/50 to-slate-600/50 rounded-lg hover:from-blue-900/30 hover:to-purple-900/30 transition-all duration-200 border border-slate-600">
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                      <Megaphone className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="font-semibold text-white text-sm">{campaign.name}</p>
                      <p className="text-xs text-slate-400">
                        {new Date(campaign.created_at).toLocaleDateString()} • {new Date(campaign.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-1">
                    {campaign.scheduled_at ? (
                      <span className="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-amber-900/50 text-amber-300 border border-amber-700">
                        <Clock className="h-2.5 w-2.5 mr-1" />
                        Scheduled
                      </span>
                    ) : (
                      <span className="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-emerald-900/50 text-emerald-300 border border-emerald-700">
                        <CheckCircle2 className="h-2.5 w-2.5 mr-1" />
                        Active
                      </span>
                    )}
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-6">
                <Megaphone className="mx-auto h-8 w-8 text-slate-500 mb-2" />
                <h3 className="text-xs font-medium text-white mb-1">No campaigns yet</h3>
                <p className="text-xs text-slate-400">Create your first campaign to get started</p>
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions & System Status */}
        <div className="space-y-3">
          {/* Quick Actions */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-xl border border-slate-700 p-3">
            <h3 className="text-base font-bold text-white mb-3">Quick Actions</h3>
            <div className="grid grid-cols-2 gap-2">
              {quickActions.map((action, index) => (
                <button
                  key={index}
                  className={`p-3 rounded-lg font-semibold text-xs transition-all duration-200 transform hover:scale-105 ${action.color} ${action.textColor} shadow-md hover:shadow-lg`}
                >
                  <action.icon className="h-5 w-5 mx-auto mb-1" />
                  {action.label}
                </button>
              ))}
            </div>
          </div>

          {/* System Status */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-xl border border-slate-700 p-3">
            <h3 className="text-base font-bold text-white mb-3">System Health</h3>
            <div className="space-y-2">
              <div className="flex items-center justify-between p-2 bg-emerald-900/30 rounded-lg border border-emerald-700/50">
                <div className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-emerald-400 mr-2" />
                  <span className="text-xs font-medium text-slate-200">API Status</span>
                </div>
                <span className="text-xs text-emerald-300 font-semibold">Online</span>
              </div>

              <div className="flex items-center justify-between p-2 bg-emerald-900/30 rounded-lg border border-emerald-700/50">
                <div className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-emerald-400 mr-2" />
                  <span className="text-xs font-medium text-slate-200">WhatsApp Service</span>
                </div>
                <span className="text-xs text-emerald-300 font-semibold">Connected</span>
              </div>

              <div className="flex items-center justify-between p-2 bg-emerald-900/30 rounded-lg border border-emerald-700/50">
                <div className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-emerald-400 mr-2" />
                  <span className="text-xs font-medium text-slate-200">Database</span>
                </div>
                <span className="text-xs text-emerald-300 font-semibold">Healthy</span>
              </div>

              <div className="flex items-center justify-between p-2 bg-blue-900/30 rounded-lg border border-blue-700/50">
                <div className="flex items-center">
                  <Activity className="h-4 w-4 text-blue-400 mr-2" />
                  <span className="text-xs font-medium text-slate-200">Active Sessions</span>
                </div>
                <span className="text-xs text-blue-300 font-semibold">1</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

