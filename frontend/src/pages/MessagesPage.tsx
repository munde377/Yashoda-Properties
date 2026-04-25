import { useEffect, useState } from 'react'
import api from '../api'

interface Message {
  id: number
  customer_id: number
  campaign_id?: number
  content: string
  event_type: string
  event_name?: string
  status: string
  timestamp: string
}

const MessagesPage = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api
      .get<Message[]>('/messages')
      .then((response) => setMessages(response.data))
      .catch(() => setError('Unable to load messages.'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <section className="space-y-5">
      <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
        <h2 className="text-xl font-semibold text-white">Messages</h2>
        <p className="mt-2 text-sm text-slate-300">View and manage sent messages.</p>
      </div>

      <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
        {loading ? (
          <p className="text-sm text-slate-400">Loading messages...</p>
        ) : error ? (
          <p className="text-sm text-rose-500">{error}</p>
        ) : (
          <div className="space-y-3">
            {messages.length === 0 ? (
              <p className="text-sm text-slate-400">No messages yet.</p>
            ) : (
              messages.map((message) => (
                <div key={message.id} className="rounded-3xl border border-slate-700 bg-slate-900/80 p-4">
                  <div className="flex justify-between items-start mb-2">
                    <p className="font-semibold text-white">{message.event_type}</p>
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      message.status === 'sent' ? 'bg-green-600 text-white' :
                      message.status === 'delivered' ? 'bg-blue-600 text-white' :
                      'bg-red-600 text-white'
                    }`}>
                      {message.status}
                    </span>
                  </div>
                  <p className="text-sm text-slate-300 mb-2">{message.content}</p>
                  <p className="text-xs text-slate-400">
                    {new Date(message.timestamp).toLocaleString()}
                  </p>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </section>
  )
}

export default MessagesPage