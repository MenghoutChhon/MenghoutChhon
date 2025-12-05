'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function VideoPage() {
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [duration, setDuration] = useState(5)
  const [resolution, setResolution] = useState('720p')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('http://localhost:8000/api/video/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          prompt, 
          duration,
          resolution,
          fps: 30
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to generate video')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError('Failed to generate video. Please make sure the backend server is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="container mx-auto px-4">
        <Link href="/" className="text-blue-600 hover:text-blue-800 mb-4 inline-block">
          ← Back to Home
        </Link>

        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8">
          <div className="text-center mb-8">
            <div className="text-6xl mb-4">🎬</div>
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              Video Generation
            </h1>
            <p className="text-gray-600">
              Generate videos from text descriptions
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-2">
                Video Description
              </label>
              <textarea
                id="prompt"
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Describe the video you want to generate..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="duration" className="block text-sm font-medium text-gray-700 mb-2">
                  Duration: {duration}s
                </label>
                <input
                  type="range"
                  id="duration"
                  min="3"
                  max="30"
                  value={duration}
                  onChange={(e) => setDuration(parseInt(e.target.value))}
                  className="w-full"
                />
              </div>

              <div>
                <label htmlFor="resolution" className="block text-sm font-medium text-gray-700 mb-2">
                  Resolution
                </label>
                <select
                  id="resolution"
                  value={resolution}
                  onChange={(e) => setResolution(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="480p">480p</option>
                  <option value="720p">720p</option>
                  <option value="1080p">1080p</option>
                </select>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Generating Video...' : 'Generate Video'}
            </button>
          </form>

          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {result && (
            <div className="mt-6 p-6 bg-yellow-50 border border-yellow-200 rounded-lg">
              <h3 className="font-semibold text-yellow-800 mb-4">Status: {result.status}</h3>
              <p className="text-yellow-700 mb-4">{result.message}</p>
              {result.note && (
                <p className="text-sm text-yellow-600 mb-4 italic">{result.note}</p>
              )}
              {result.recommended_models && (
                <div className="mt-4">
                  <h4 className="font-semibold text-yellow-800 mb-2">Recommended Models:</h4>
                  <ul className="list-disc list-inside space-y-1">
                    {result.recommended_models.map((model: string, idx: number) => (
                      <li key={idx} className="text-sm text-yellow-700">{model}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          <div className="mt-8 p-6 bg-gray-50 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-4">Available Models</h3>
            <div className="space-y-3">
              <div className="border-l-4 border-blue-500 pl-4">
                <p className="font-semibold text-gray-800">Mochi 1</p>
                <p className="text-sm text-gray-600">10B+ parameters, MIT license, Easy deployment</p>
              </div>
              <div className="border-l-4 border-green-500 pl-4">
                <p className="font-semibold text-gray-800">Wan2.2-T2V-A14B</p>
                <p className="text-sm text-gray-600">14B parameters, 5s @ 720p, Cinematic quality</p>
              </div>
              <div className="border-l-4 border-purple-500 pl-4">
                <p className="font-semibold text-gray-800">HunyuanVideo</p>
                <p className="text-sm text-gray-600">13B+ parameters, Temporal consistency, Apache 2.0</p>
              </div>
            </div>
            <p className="text-sm text-gray-500 mt-4">
              ⚠️ Note: Video generation requires GPU infrastructure (A100/H100 recommended)
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
