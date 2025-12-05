'use client'

import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function TTSPage() {
  const [text, setText] = useState('')
  const [speed, setSpeed] = useState(1.0)
  const [loading, setLoading] = useState(false)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSynthesize = async () => {
    if (!text.trim()) {
      setError('Please enter some text')
      return
    }

    setLoading(true)
    setError(null)
    setAudioUrl(null)

    try {
      const response = await axios.post(`${API_URL}/api/tts/synthesize`, {
        text,
        speed
      })

      // Convert base64 to audio URL
      const audioBlob = base64ToBlob(response.data.audio_base64, 'audio/wav')
      const url = URL.createObjectURL(audioBlob)
      setAudioUrl(url)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to synthesize speech')
    } finally {
      setLoading(false)
    }
  }

  const base64ToBlob = (base64: string, type: string) => {
    const byteCharacters = atob(base64)
    const byteNumbers = new Array(byteCharacters.length)
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i)
    }
    const byteArray = new Uint8Array(byteNumbers)
    return new Blob([byteArray], { type })
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">🔊 Text-to-Speech</h1>
        
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">
              Khmer Text
            </label>
            <textarea
              className="w-full p-3 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
              rows={6}
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter Khmer text here..."
            />
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">
              Speed: {speed.toFixed(1)}x
            </label>
            <input
              type="range"
              min="0.5"
              max="2.0"
              step="0.1"
              value={speed}
              onChange={(e) => setSpeed(parseFloat(e.target.value))}
              className="w-full"
            />
          </div>

          <button
            onClick={handleSynthesize}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Synthesizing...' : 'Generate Speech'}
          </button>

          {error && (
            <div className="mt-4 p-4 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-100 rounded-lg">
              {error}
            </div>
          )}

          {audioUrl && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold mb-3">Generated Audio</h3>
              <audio controls src={audioUrl} className="w-full" />
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
