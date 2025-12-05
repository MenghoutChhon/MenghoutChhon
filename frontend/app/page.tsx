import Link from 'next/link'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            🇰🇭 Khmer AI/ML Platform
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Advanced AI services for Khmer language processing
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {/* TTS Card */}
          <Link href="/tts" className="block">
            <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer">
              <div className="text-4xl mb-4">🔊</div>
              <h2 className="text-2xl font-bold mb-2 text-gray-800">Text-to-Speech</h2>
              <p className="text-gray-600">
                Convert Khmer text to natural-sounding speech using Meta's MMS-TTS model
              </p>
              <div className="mt-4 text-blue-600 font-semibold">
                Try TTS →
              </div>
            </div>
          </Link>

          {/* OCR Card */}
          <Link href="/ocr" className="block">
            <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer">
              <div className="text-4xl mb-4">📸</div>
              <h2 className="text-2xl font-bold mb-2 text-gray-800">OCR</h2>
              <p className="text-gray-600">
                Extract Khmer text from images using TrOCR fine-tuned model
              </p>
              <div className="mt-4 text-blue-600 font-semibold">
                Try OCR →
              </div>
            </div>
          </Link>

          {/* Summarization Card */}
          <Link href="/summarize" className="block">
            <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer">
              <div className="text-4xl mb-4">📝</div>
              <h2 className="text-2xl font-bold mb-2 text-gray-800">Summarization</h2>
              <p className="text-gray-600">
                Summarize Khmer text using mT5 language model
              </p>
              <div className="mt-4 text-blue-600 font-semibold">
                Try Summarization →
              </div>
            </div>
          </Link>

          {/* Video Generation Card */}
          <Link href="/video" className="block">
            <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer">
              <div className="text-4xl mb-4">🎬</div>
              <h2 className="text-2xl font-bold mb-2 text-gray-800">Video Generation</h2>
              <p className="text-gray-600">
                Generate videos from text using state-of-the-art AI models
              </p>
              <div className="mt-4 text-blue-600 font-semibold">
                Try Video Gen →
              </div>
            </div>
          </Link>
        </div>

        {/* Features Section */}
        <div className="mt-16 max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
          <h3 className="text-3xl font-bold mb-6 text-gray-800 text-center">
            Platform Features
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-bold text-lg mb-2 text-gray-800">🚀 State-of-the-Art Models</h4>
              <p className="text-gray-600">
                Powered by latest AI models from Meta, Google, and research institutions
              </p>
            </div>
            <div>
              <h4 className="font-bold text-lg mb-2 text-gray-800">🇰🇭 Khmer Language Focus</h4>
              <p className="text-gray-600">
                Specialized models fine-tuned specifically for Khmer language processing
              </p>
            </div>
            <div>
              <h4 className="font-bold text-lg mb-2 text-gray-800">⚡ Fast API</h4>
              <p className="text-gray-600">
                High-performance FastAPI backend with async processing
              </p>
            </div>
            <div>
              <h4 className="font-bold text-lg mb-2 text-gray-800">🔒 Secure</h4>
              <p className="text-gray-600">
                Enterprise-grade security with JWT authentication and rate limiting
              </p>
            </div>
          </div>
        </div>

        {/* API Info */}
        <div className="mt-8 text-center">
          <a 
            href={`${API_URL}/docs`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            📚 View API Documentation
          </a>
        </div>
      </div>
    </main>
  )
}
