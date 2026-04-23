import { FormEvent, useEffect, useState } from 'react'
import api from '../api'

interface Customer {
  id: number
  name: string
  phone: string
  email?: string
  birthday?: string
  tags?: string
}

function CustomerManager() {
  const [customers, setCustomers] = useState<Customer[]>([])
  const [formState, setFormState] = useState({ name: '', phone: '', email: '', birthday: '', tags: '' })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchCustomers = () => {
    setLoading(true)
    api
      .get<Customer[]>('/customers')
      .then((response) => setCustomers(response.data))
      .catch(() => setError('Unable to load customers.'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchCustomers()
  }, [])

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)
    api
      .post<Customer>('/customers', {
        ...formState,
        birthday: formState.birthday || null,
      })
      .then(() => {
        setFormState({ name: '', phone: '', email: '', birthday: '', tags: '' })
        fetchCustomers()
      })
      .catch((err) => {
        setError(err.response?.data?.detail || 'Unable to save customer.')
      })
  }

  return (
    <section className="space-y-5">
      <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-xl font-semibold text-white">Customer Management</h2>
            <p className="mt-2 text-sm text-slate-300">Add, search, and manage customer records.</p>
          </div>
        </div>
      </div>

      <div className="grid gap-4 xl:grid-cols-[1.2fr,0.8fr]">
        <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
          <h3 className="text-lg font-semibold text-white">Add Customer</h3>
          <form className="mt-5 space-y-4" onSubmit={handleSubmit}>
            <div className="grid gap-4 sm:grid-cols-2">
              <label className="space-y-2 text-sm text-slate-300">
                Name
                <input
                  value={formState.name}
                  onChange={(e) => setFormState({ ...formState, name: e.target.value })}
                  required
                  className="w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </label>
              <label className="space-y-2 text-sm text-slate-300">
                Phone
                <input
                  value={formState.phone}
                  onChange={(e) => setFormState({ ...formState, phone: e.target.value })}
                  required
                  className="w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </label>
              <label className="space-y-2 text-sm text-slate-300">
                Email
                <input
                  value={formState.email}
                  onChange={(e) => setFormState({ ...formState, email: e.target.value })}
                  className="w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </label>
              <label className="space-y-2 text-sm text-slate-300">
                Birthday
                <input
                  type="date"
                  value={formState.birthday}
                  onChange={(e) => setFormState({ ...formState, birthday: e.target.value })}
                  className="w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </label>
            </div>
            <label className="space-y-2 text-sm text-slate-300">
              Tags / Categories
              <input
                value={formState.tags}
                onChange={(e) => setFormState({ ...formState, tags: e.target.value })}
                className="w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                placeholder="vip, loyal, new"
              />
            </label>
            {error && <p className="text-sm text-rose-500">{error}</p>}
            <button className="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 px-5 py-3 text-sm font-semibold text-white transition hover:from-blue-700 hover:to-purple-700">
              Save Customer
            </button>
          </form>
        </div>

        <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
          <h3 className="text-lg font-semibold text-white">Customer List</h3>
          {loading ? (
            <p className="mt-4 text-sm text-slate-400">Loading...</p>
          ) : (
            <div className="mt-4 space-y-3">
              {customers.length === 0 ? (
                <p className="text-sm text-slate-400">No customers yet.</p>
              ) : (
                customers.map((customer) => (
                  <div key={customer.id} className="rounded-3xl border border-slate-700 bg-slate-900/80 p-4">
                    <p className="font-semibold text-white">{customer.name}</p>
                    <p className="text-sm text-slate-400">{customer.phone}</p>
                    <p className="text-sm text-slate-400">{customer.email || 'No email'}</p>
                    <p className="text-sm text-slate-400">{customer.birthday || 'No birthday'}</p>
                    <p className="text-sm text-slate-400">{customer.tags || 'No tags'}</p>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </section>
  )
}

export default CustomerManager
