import { Application } from "@/types/application"
import Link from "next/link"

export default function Home() {
  const jobs: Application[] = []

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">Job Application Tracker</h1>
            <Link
              href="/applications/new"
              className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
            >
              + Add Application
            </Link>
          </div>
        </div>
      </header>

      {/* Stats */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm">Total Applications</div>
            <div className="text-3xl font-bold text-gray-900">{jobs.length}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm">Applied</div>
            <div className="text-3xl font-bold text-primary-600">{jobs.filter(j => j.status === 'applied').length}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm">Interviews</div>
            <div className="text-3xl font-bold text-green-600">{jobs.filter(j => j.status === 'interview').length}</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-gray-500 text-sm">Pending</div>
            <div className="text-3xl font-bold text-yellow-600">{jobs.filter(j => j.status === 'pending').length}</div>
          </div>
        </div>

        {/* Pipeline View */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Application Pipeline</h2>
          
          {jobs.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 mb-4">No applications yet</p>
              <Link
                href="/applications/new"
                className="text-primary-600 hover:text-primary-700 font-medium"
              >
                Add your first application →
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {['pending', 'applied', 'interview', 'offer'].map((status) => (
                <div key={status} className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-700 mb-2 capitalize">{status}</h3>
                  {jobs.filter(j => j.status === status).map(job => (
                    <Link
                      key={job.id}
                      href={`/applications/${job.id}`}
                      className="block bg-white p-3 rounded border hover:border-primary-500 mb-2"
                    >
                      <div className="font-medium text-gray-900">{job.position}</div>
                      <div className="text-sm text-gray-500">{job.company}</div>
                    </Link>
                  ))}
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
