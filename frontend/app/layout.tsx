import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Khmer AI/ML Platform',
  description: 'AI/ML services for Khmer language including TTS, OCR, Summarization, and Video Generation',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
