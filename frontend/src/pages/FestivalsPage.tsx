import { FormEvent, useEffect, useState } from 'react'
import api from '../api'

interface Festival {
  id: number
  name: string
  date: string
  template_id?: number
}

interface Template {
  id: number
  name: string
  type: string
}

const FestivalsPage = () => {
  const [festivals, setFestivals] = useState<Festival[]>([])
  const [templates, setTemplates] = useState<Template[]>([])
  const [formState, setFormState] = useState({ name: '', date: '', template_id: '' })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([
      api.get<Festival[]>('/festivals'),
      api.get<Template[]>('/templates')
    ])
      .then(([festivalsResponse, templatesResponse]) => {
        setFestivals(festivalsResponse.data)
        setTemplates(templatesResponse.data)
      })
      .catch(() => setError('Unable to load data.'))
      .finally(() => setLoading(false))
  }, [])

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)
    const data: any = {
      name: formState.name,
      date: formState.date,
    }
    if (formState.template_id) {
      data.template_id = parseInt(formState.template_id)
    }
    api
      .post<Festival>('/festivals', data)
      .then((response) => {
        setFestivals((current) => [response.data, ...current])
        setFormState({ name: '', date: '', template_id: '' })
      })
      .catch((err) => {
        setError(err.response?.data?.detail || 'Unable to save festival.')
      })
  }

  return (
    <section className="space-y-5">
      <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
        <h2 className="text-xl font-semibold text-white">Festival Management</h2>
        <p className="mt-2 text-sm text-slate-300">Manage festival campaigns and greetings.</p>
      </div>

      <div className="grid gap-4 xl:grid-cols-[1.2fr,0.8fr]">
        <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
          <h3 className="text-lg font-semibold text-white">Add Festival</h3>
          <form className="mt-5 space-y-4" onSubmit={handleSubmit}>
            <div className="grid gap-4 sm:grid-cols-2">
              <label className="space-y-2 text-sm text-slate-300">
                Festival Name
                <input
                  value={formState.name}
                  onChange={(e) => setFormState({ ...formState, name: e.target.value })}
                  required
                  className="w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </label>
              <label className="space-y-2 text-sm text-slate-300">
                Date
                <input
                  type="date"
                  value={formState.date}
                  onChange={(e) => setFormState({ ...formState, date: e.target.value })}
                  required
                  className="w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
              </label>
            </div>
            <label className="space-y-2 text-sm text-slate-300">
              Template (Optional)
              <select
                value={formState.template_id}
                onChange={(e) => setFormState({ ...formState, template_id: e.target.value })}
                className="w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              >
                <option value="">No template</option>
                {templates.filter(t => t.type === 'festival').map((template) => (
                  <option key={template.id} value={template.id}>
                    {template.name}
                  </option>
                ))}
              </select>
            </label>
            {error && <p className="text-sm text-rose-500">{error}</p>}
            <button className="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 px-5 py-3 text-sm font-semibold text-white transition hover:from-blue-700 hover:to-purple-700">
              Save Festival
            </button>
          </form>
        </div>

        <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
          <h3 className="text-lg font-semibold text-white">Festival List</h3>
          {loading ? (
            <p className="mt-4 text-sm text-slate-400">Loading...</p>
          ) : (
            <div className="mt-4 space-y-3">
              {festivals.length === 0 ? (
                <p className="text-sm text-slate-400">No festivals yet.</p>
              ) : (
                festivals.map((festival) => (
                  <div key={festival.id} className="rounded-3xl border border-slate-700 bg-slate-900/80 p-4">
                    <p className="font-semibold text-white">{festival.name}</p>
                    <p className="text-sm text-slate-400">
                      {new Date(festival.date).toLocaleDateString()}
                    </p>
                    {festival.template_id && (
                      <p className="text-sm text-slate-400">
                        Template: {templates.find(t => t.id === festival.template_id)?.name}
                      </p>
                    )}
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

export default FestivalsPage