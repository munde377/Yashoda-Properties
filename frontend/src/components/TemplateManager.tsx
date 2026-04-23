import { FormEvent, useEffect, useState } from 'react'
import api from '../api'

interface Template {
  id: number
  name: string
  type: string
  body: string
}

const templateTypes = ['birthday', 'festival', 'campaign', 'custom']

function TemplateManager() {
  const [templates, setTemplates] = useState<Template[]>([])
  const [formState, setFormState] = useState({ name: '', type: 'birthday', body: '' })
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api
      .get<Template[]>('/templates')
      .then((response) => setTemplates(response.data))
      .catch(() => setError('Unable to load templates.'))
  }, [])

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)
    api
      .post<Template>('/templates', formState)
      .then((response) => {
        setTemplates((current) => [response.data, ...current])
        setFormState({ name: '', type: 'birthday', body: '' })
      })
      .catch((err) => {
        setError(err.response?.data?.detail || 'Unable to save template.')
      })
  }

  return (
    <section className="space-y-5">
      <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
        <h2 className="text-xl font-semibold text-white">Template Management</h2>
        <p className="mt-2 text-sm text-slate-300">Create birthday, festival, campaign, and custom WhatsApp templates.</p>
      </div>

      <div className="grid gap-4 xl:grid-cols-[1.3fr,0.7fr]">
        <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
          <h3 className="text-lg font-semibold text-white">New Template</h3>
          <form className="mt-5 space-y-4" onSubmit={handleSubmit}>
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
              Type
              <select
                value={formState.type}
                onChange={(e) => setFormState({ ...formState, type: e.target.value })}
                className="w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              >
                {templateTypes.map((typeOption) => (
                  <option key={typeOption} value={typeOption} className="bg-slate-900 text-white">
                    {typeOption}
                  </option>
                ))}
              </select>
            </label>
            <label className="space-y-2 text-sm text-slate-300">
              Body
              <textarea
                rows={5}
                value={formState.body}
                onChange={(e) => setFormState({ ...formState, body: e.target.value })}
                required
                className="w-full rounded-2xl border border-slate-700 bg-slate-900/80 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                placeholder="Hello {{name}}, we have a special offer for you..."
              />
            </label>
            {error && <p className="text-sm text-rose-500">{error}</p>}
            <button className="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 px-5 py-3 text-sm font-semibold text-white transition hover:from-blue-700 hover:to-purple-700">
              Save Template
            </button>
          </form>
        </div>

        <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
          <h3 className="text-lg font-semibold text-white">Saved Templates</h3>
          <div className="mt-4 space-y-3">
            {templates.length === 0 ? (
              <p className="text-sm text-slate-400">No templates created yet.</p>
            ) : (
              templates.map((template) => (
                <div key={template.id} className="rounded-3xl border border-slate-700 bg-slate-900/80 p-4">
                  <p className="font-semibold text-white">{template.name}</p>
                  <p className="text-sm text-slate-400">Type: {template.type}</p>
                  <p className="mt-2 whitespace-pre-wrap text-sm text-slate-300">{template.body}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </section>
  )
}

export default TemplateManager
