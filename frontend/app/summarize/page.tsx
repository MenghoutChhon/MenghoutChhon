'use client'

import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function SummarizePage() {
  const [text, setText] = useState('')
  const [maxLength, setMaxLength] = useState(150)
  const [loading, setLoading] = useState(false)
  const [summary, setSummary] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSummarize = async () => {
    if (!text.trim()) {
      setError('Please enter some text')
      return
    }

    setLoading(true)
    setError(null)
    setSummary(null)

    try {
      const response = await axios.post(`${API_URL}/api/llm/summarize`, {
        text,
        max_length: maxLength,
        min_length: Math.floor(maxLength / 3)
      })

      setSummary(response.data.output)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to summarize text')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">📝 Text Summarization</h1>
        
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">
              Khmer Text
            </label>
            <textarea
              className="w-full p-3 border rounded-lg dark:bg-gray-700 dark:border-gray-600"
              rows={8}
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter Khmer text to summarize..."
            />
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">
              Maximum Summary Length: {maxLength} tokens
            </label>
            <input
              type="range"
              min="50"
              max="300"
              step="10"
              value={maxLength}
              onChange={(e) => setMaxLength(parseInt(e.target.value))}
              className="w-full"
            />
          </div>

          <button
            onClick={handleSummarize}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Summarizing...' : 'Summarize Text'}
          </button>

          {error && (
            <div className="mt-4 p-4 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-100 rounded-lg">
              {error}
            </div>
          )}

          {summary && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold mb-3">Summary</h3>
              <div className="p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
                <p className="whitespace-pre-wrap">{summary}</p>
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
