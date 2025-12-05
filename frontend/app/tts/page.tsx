'use client'

import { useState } from 'react'
import Link from 'next/link'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function TTSPage() {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setAudioUrl(null)

    try {
      const response = await fetch(`${API_URL}/api/tts/synthesize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, language: 'khmer' }),
      })

      if (!response.ok) {
        throw new Error('Failed to generate speech')
      }

      const data = await response.json()
      // In a real implementation, you would get the audio file URL from the response
      setAudioUrl(data.audio_file)
    } catch (err) {
      setError('Failed to generate speech. Please make sure the backend server is running.')
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
            <div className="text-6xl mb-4">🔊</div>
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              Text-to-Speech
            </h1>
            <p className="text-gray-600">
              Convert Khmer text to natural-sounding speech
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="text" className="block text-sm font-medium text-gray-700 mb-2">
                Enter Khmer Text
              </label>
              <textarea
                id="text"
                rows={6}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="សូមបញ្ចូលអត្ថបទភាសាខ្មែរនៅទីនេះ..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Generating Speech...' : 'Generate Speech'}
            </button>
          </form>

          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {audioUrl && (
            <div className="mt-6 p-6 bg-green-50 border border-green-200 rounded-lg">
              <h3 className="font-semibold text-green-800 mb-4">Speech Generated!</h3>
              <audio controls className="w-full">
                <source src={audioUrl} type="audio/wav" />
                Your browser does not support the audio element.
              </audio>
            </div>
          )}

          <div className="mt-8 p-6 bg-gray-50 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2">Model Information</h3>
            <p className="text-sm text-gray-600 mb-2">
              <strong>Model:</strong> facebook/mms-tts-khm (Meta MMS)
            </p>
            <p className="text-sm text-gray-600 mb-2">
              <strong>Type:</strong> VITS (Variational Inference with adversarial learning)
            </p>
            <p className="text-sm text-gray-600">
              <strong>Features:</strong> High-quality Khmer speech synthesis
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
