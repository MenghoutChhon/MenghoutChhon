'use client'

import { useState } from 'react'
import Link from 'next/link'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function OCRPage() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [preview, setPreview] = useState<string | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
      // Create preview
      const reader = new FileReader()
      reader.onload = (e) => {
        setPreview(e.target?.result as string)
      }
      reader.readAsDataURL(selectedFile)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${API_URL}/api/ocr/extract`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to extract text')
      }

      const data = await response.json()
      setResult(data.text)
    } catch (err) {
      setError('Failed to extract text. Please make sure the backend server is running.')
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
            <div className="text-6xl mb-4">📸</div>
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              OCR - Text Extraction
            </h1>
            <p className="text-gray-600">
              Extract Khmer text from images
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="file" className="block text-sm font-medium text-gray-700 mb-2">
                Upload Image
              </label>
              <input
                type="file"
                id="file"
                accept="image/*"
                onChange={handleFileChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            {preview && (
              <div className="border border-gray-300 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-2">Preview:</p>
                <img src={preview} alt="Preview" className="max-w-full h-auto rounded" />
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !file}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Extracting Text...' : 'Extract Text'}
            </button>
          </form>

          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {result && (
            <div className="mt-6 p-6 bg-green-50 border border-green-200 rounded-lg">
              <h3 className="font-semibold text-green-800 mb-4">Extracted Text:</h3>
              <div className="bg-white p-4 rounded border border-green-300">
                <p className="text-gray-800 whitespace-pre-wrap">{result}</p>
              </div>
            </div>
          )}

          <div className="mt-8 p-6 bg-gray-50 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2">Model Information</h3>
            <p className="text-sm text-gray-600 mb-2">
              <strong>Model:</strong> songhieng/khmer-trocr-ocr-v1.0
            </p>
            <p className="text-sm text-gray-600 mb-2">
              <strong>Type:</strong> TrOCR (Vision Transformer + RoBERTa)
            </p>
            <p className="text-sm text-gray-600">
              <strong>Use Case:</strong> ID cards, documents, printed Khmer text
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
