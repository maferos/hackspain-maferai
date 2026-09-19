/**
 * Live image sources for the viewport: an HTML video, an MJPEG stream or
 * JPEG/PNG frames over a WebSocket. Each fills the panel with letterboxing.
 */

import { useEffect, useRef } from 'react'
import type { ViewportSource } from '../../config'

const RECONNECT_MS = 3000

function FrameSocket({ url }: { url: string }) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    let socket: WebSocket | null = null
    let timer: number | null = null
    let closed = false

    const draw = (bitmap: ImageBitmap | HTMLImageElement, w: number, h: number) => {
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w
        canvas.height = h
      }
      ctx.drawImage(bitmap, 0, 0)
    }

    const connect = () => {
      socket = new WebSocket(url)
      socket.binaryType = 'blob'
      socket.onmessage = async (e) => {
        if (e.data instanceof Blob) {
          const bmp = await createImageBitmap(e.data)
          draw(bmp, bmp.width, bmp.height)
          bmp.close()
          return
        }
        try {
          const msg = JSON.parse(String(e.data)) as { type?: string; data?: string; mime?: string }
          if (msg.type === 'frame' && msg.data) {
            const img = new Image()
            img.onload = () => draw(img, img.naturalWidth, img.naturalHeight)
            img.src = `data:${msg.mime ?? 'image/jpeg'};base64,${msg.data}`
          }
        } catch {
          /* not a frame message */
        }
      }
      socket.onclose = () => {
        if (!closed) timer = window.setTimeout(connect, RECONNECT_MS)
      }
    }
    connect()
    return () => {
      closed = true
      if (timer !== null) window.clearTimeout(timer)
      socket?.close()
    }
  }, [url])

  return <canvas ref={canvasRef} className="h-full w-full object-contain" />
}

export function StreamView({ source }: { source: Exclude<ViewportSource, { kind: 'schematic' }> }) {
  switch (source.kind) {
    case 'video':
      return <video src={source.src} autoPlay muted loop playsInline className="h-full w-full object-contain" />
    case 'mjpeg':
      return <img src={source.src} alt="Simulator stream" className="h-full w-full object-contain" />
    case 'websocket':
      return <FrameSocket url={source.url} />
  }
}
