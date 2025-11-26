'use client'

import { useState, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'

interface VoiceInputProps {
  onTranscript: (transcript: string, audioData: string) => void
  disabled?: boolean
}

export function VoiceInput({ onTranscript, disabled }: VoiceInputProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [transcript, setTranscript] = useState('')
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      chunksRef.current = []

      mediaRecorder.ondataavailable = (e) => {
        chunksRef.current.push(e.data)
      }

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/wav' })
        const reader = new FileReader()

        reader.onloadend = () => {
          const base64Audio = reader.result?.toString().split(',')[1] || ''
          setTranscript('Processing...')
          onTranscript('Voice input received', base64Audio)
        }

        reader.readAsDataURL(audioBlob)

        // Stop all tracks
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      setIsRecording(true)
      setTranscript('')
    } catch (error) {
      console.error('Error starting recording:', error)
      alert('Could not access microphone. Please check permissions.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  return (
    <Card className="p-4">
      <div className="flex items-center gap-4">
        <Button
          onClick={isRecording ? stopRecording : startRecording}
          variant={isRecording ? 'destructive' : 'default'}
          disabled={disabled}
          className="flex-shrink-0"
        >
          {isRecording ? (
            <>
              <span className="mr-2">⏸</span> Stop Recording
            </>
          ) : (
            <>
              <span className="mr-2">🎤</span> Voice Input
            </>
          )}
        </Button>
        {isRecording && (
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-muted-foreground">Recording...</span>
          </div>
        )}
        {transcript && (
          <p className="text-sm text-muted-foreground">{transcript}</p>
        )}
      </div>
    </Card>
  )
}
