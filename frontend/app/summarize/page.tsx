'use client'

import { useState } from 'react'
import Link from 'next/link'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function SummarizePage() {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [summary, setSummary] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [maxLength, setMaxLength] = useState(150)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSummary(null)

    try {
      const response = await fetch(`${API_URL}/api/llm/summarize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text, 
          max_length: maxLength,
          min_length: 30 
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to summarize text')
      }

      const data = await response.json()
      setSummary(data.summary)
    } catch (err) {
      setError('Failed to summarize text. Please make sure the backend server is running.')
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
            <div className="text-6xl mb-4">📝</div>
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              Text Summarization
            </h1>
            <p className="text-gray-600">
              Summarize Khmer text using AI
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="text" className="block text-sm font-medium text-gray-700 mb-2">
                Enter Khmer Text to Summarize
              </label>
              <textarea
                id="text"
                rows={8}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="បញ្ចូលអត្ថបទវែងៗដើម្បីសង្ខេប..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                required
              />
            </div>

            <div>
              <label htmlFor="maxLength" className="block text-sm font-medium text-gray-700 mb-2">
                Maximum Summary Length: {maxLength}
              </label>
              <input
                type="range"
                id="maxLength"
                min="50"
                max="300"
                step="10"
                value={maxLength}
                onChange={(e) => setMaxLength(parseInt(e.target.value))}
                className="w-full"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Summarizing...' : 'Summarize Text'}
            </button>
          </form>

          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {summary && (
            <div className="mt-6 space-y-4">
              <div className="p-6 bg-green-50 border border-green-200 rounded-lg">
                <h3 className="font-semibold text-green-800 mb-4">Summary:</h3>
                <div className="bg-white p-4 rounded border border-green-300">
                  <p className="text-gray-800 whitespace-pre-wrap">{summary}</p>
                </div>
              </div>
              
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm text-blue-800">
                  Original length: {text.length} characters | Summary length: {summary.length} characters
                </p>
              </div>
            </div>
          )}

          <div className="mt-8 p-6 bg-gray-50 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2">Model Information</h3>
            <p className="text-sm text-gray-600 mb-2">
              <strong>Model:</strong> Seanghay/khmer-mt5-summarization
            </p>
            <p className="text-sm text-gray-600 mb-2">
              <strong>Type:</strong> mT5 (Multilingual Text-to-Text Transfer Transformer)
            </p>
            <p className="text-sm text-gray-600">
              <strong>Features:</strong> Fine-tuned for Khmer text summarization
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
