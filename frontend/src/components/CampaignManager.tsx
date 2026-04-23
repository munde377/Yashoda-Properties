import { FormEvent, useEffect, useState } from 'react'
import api from '../api'

interface Template {
  id: number
  name: string
  type: string
}

interface Customer {
  id: number
  name: string
}

function CampaignManager() {
  const [templates, setTemplates] = useState<Template[]>([])
  const [customers, setCustomers] = useState<Customer[]>([])
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [formState, setFormState] = useState({
    name: '',
    template_id: 0,
    send_all: false,
    recipient_ids: [] as number[],
    scheduled_at: '',
  })

  useEffect(() => {
    api.get<Template[]>('/templates').then((response) => setTemplates(response.data)).catch(console.error)
    api
      .get<Customer[]>('/customers')
      .then((response) => setCustomers(response.data))
      .catch(console.error)
  }, [])

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)
    setSuccess(null)
    api
      .post('/campaigns', {
        name: formState.name,
        template_id: formState.template_id,
        send_all: formState.send_all,
        recipient_ids: formState.send_all ? [] : formState.recipient_ids,
        scheduled_at: formState.scheduled_at || null,
      })
      .then(() => {
        setSuccess('Campaign created successfully.')
        setFormState({ name: '', template_id: 0, send_all: false, recipient_ids: [], scheduled_at: '' })
      })
      .catch((err) => {
        setError(err.response?.data?.detail || 'Unable to create campaign.')
      })
  }

  const toggleRecipient = (customerId: number) => {
    setFormState((current) => ({
      ...current,
      recipient_ids: current.recipient_ids.includes(customerId)
        ? current.recipient_ids.filter((id) => id !== customerId)
        : [...current.recipient_ids, customerId],
    }))
  }

  return (
    <section className="space-y-5">
      <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
        <h2 className="text-xl font-semibold text-white">Campaign Manager</h2>
        <p className="mt-2 text-sm text-slate-300">Create and schedule campaigns using templates.</p>
      </div>

      <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
        <form className="space-y-5" onSubmit={handleSubmit}>
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="space-y-2 text-sm text-slate-300">
              Campaign Name
              <input
                value={formState.name}
                onChange={(e) => setFormState({ ...formState, name: e.target.value })}
                required
                className="w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              />
            </label>
            <label className="space-y-2 text-sm text-slate-300">
              Template
              <select
                value={formState.template_id}
                onChange={(e) => setFormState({ ...formState, template_id: Number(e.target.value) })}
                required
                className="w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              >
                <option value={0} className="bg-slate-900 text-white">Select template</option>
                {templates.map((template) => (
                  <option key={template.id} value={template.id} className="bg-slate-900 text-white">
                    {template.name} ({template.type})
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className="flex items-center gap-3">
            <label className="inline-flex items-center gap-2 text-sm text-slate-300">
              <input
                type="checkbox"
                checked={formState.send_all}
                onChange={(e) => setFormState({ ...formState, send_all: e.target.checked })}
                className="rounded border-slate-600 bg-slate-900 text-blue-500 focus:ring-blue-500"
              />
              Send to all customers
            </label>
          </div>

          {!formState.send_all && (
            <div className="rounded-3xl border border-slate-700 bg-slate-900/80 p-4">
              <p className="mb-3 text-sm font-semibold text-white">Select recipients</p>
              <div className="grid gap-2">
                {customers.map((customer) => (
                  <label key={customer.id} className="inline-flex items-center gap-3 rounded-2xl border border-slate-700 bg-slate-800/80 px-4 py-3 text-sm text-slate-200">
                    <input
                      type="checkbox"
                      checked={formState.recipient_ids.includes(customer.id)}
                      onChange={() => toggleRecipient(customer.id)}
                      className="rounded border-slate-600 bg-slate-900 text-blue-500 focus:ring-blue-500"
                    />
                    <span>{customer.name}</span>
                  </label>
                ))}
              </div>
            </div>
          )}

          <label className="space-y-2 text-sm text-slate-300">
            Schedule Date & Time
            <input
              type="datetime-local"
              value={formState.scheduled_at}
              onChange={(e) => setFormState({ ...formState, scheduled_at: e.target.value })}
              className="w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </label>

          {error && <p className="text-sm text-rose-500">{error}</p>}
          {success && <p className="text-sm text-emerald-400">{success}</p>}

          <button className="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 px-5 py-3 text-sm font-semibold text-white transition hover:from-blue-700 hover:to-purple-700">
            Create Campaign
          </button>
        </form>
      </div>
    </section>
  )
}

export default CampaignManager
