'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function VideoPage() {
  const [prompt, setPrompt] = useState('')
  const [duration, setDuration] = useState(5)
  const [loading, setLoading] = useState(false)
  const [jobId, setJobId] = useState<string | null>(null)
  const [status, setStatus] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a video prompt')
      return
    }

    setLoading(true)
    setError(null)
    setJobId(null)
    setStatus(null)

    try {
      const response = await axios.post(`${API_URL}/api/video/generate`, {
        prompt,
        duration,
        resolution: '720p',
        fps: 30
      })

      setJobId(response.data.job_id)
      setLoading(false)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start video generation')
      setLoading(false)
    }
  }

  useEffect(() => {
    if (jobId) {
      const interval = setInterval(async () => {
        try {
          const response = await axios.get(`${API_URL}/api/video/status/${jobId}`)
          setStatus(response.data)

          if (response.data.status === 'completed' || response.data.status === 'failed') {
            clearInterval(interval)
          }
        } catch (err) {
          console.error('Failed to fetch status')
        }
      }, 2000)

      return () => clearInterval(interval)
    }
  }, [jobId])

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">🎬 Video Generation</h1>
        
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">
              Video Prompt
            </label>
            <textarea
              className="w-full p-3 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
              rows={4}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the video you want to generate..."
            />
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">
              Duration: {duration} seconds
            </label>
            <input
              type="range"
              min="3"
              max="10"
              step="1"
              value={duration}
              onChange={(e) => setDuration(parseInt(e.target.value))}
              className="w-full"
            />
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Starting...' : 'Generate Video'}
          </button>

          {error && (
            <div className="mt-4 p-4 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-100 rounded-lg">
              {error}
            </div>
          )}

          {status && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold mb-3">Generation Status</h3>
              <div className="p-4 bg-gray-100 dark:bg-gray-700 rounded-lg">
                <p className="mb-2">Status: <span className="font-semibold">{status.status}</span></p>
                {status.progress !== null && (
                  <div className="mb-2">
                    <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2.5">
                      <div
                        className="bg-blue-600 h-2.5 rounded-full"
                        style={{ width: `${status.progress}%` }}
                      ></div>
                    </div>
                    <p className="text-sm mt-1">{status.progress}%</p>
                  </div>
                )}
                {status.error && (
                  <p className="text-red-600 dark:text-red-400">Error: {status.error}</p>
                )}
                {status.status === 'completed' && (
                  <div className="mt-4">
                    <p className="text-green-600 dark:text-green-400 font-semibold">
                      Video generation completed!
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                      Note: This is a placeholder implementation. In production, the video would be available for download.
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="mt-6 text-center">
          <a href="/" className="text-blue-600 hover:underline">← Back to Home</a>
        </div>
      </div>
    </div>
  )
}
