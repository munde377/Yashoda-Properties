import { useParams } from 'react-router-dom'

const CustomerDetailPage = () => {
  const { id } = useParams<{ id: string }>()

  return (
    <div className="rounded-3xl bg-slate-800/80 border border-slate-700 p-6 shadow-2xl">
      <h2 className="text-xl font-semibold text-white">Customer Details</h2>
      <p className="mt-2 text-sm text-slate-300">Details for customer ID: {id}</p>
      <div className="mt-4 text-slate-300">
        <p>Customer detail view coming soon...</p>
      </div>
    </div>
  )
}

export default CustomerDetailPage