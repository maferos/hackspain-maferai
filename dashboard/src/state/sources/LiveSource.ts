/**
 * Live source: receives state from the real system.
 *
 * `ws://` and `wss://` URLs open a WebSocket; `http://` and `https://` URLs
 * open an EventSource (Server-Sent Events). Both deliver the JSON messages
 * described in `protocol.ts`. The connection reconnects on its own.
 */

import type { LabState } from '../types'
import type { ConnectionListener, ConnectionStatus, LabStateSource, StateListener } from './LabStateSource'
import { applyMessage, parseMessage } from './protocol'

const RECONNECT_MS = 3000

export class LiveSource implements LabStateSource {
  readonly kind = 'live' as const

  private listeners = new Set<StateListener>()
  private connListeners = new Set<ConnectionListener>()
  private socket: WebSocket | EventSource | null = null
  private reconnect: number | null = null
  private status: ConnectionStatus = 'idle'
  private state: LabState
  private running = false

  constructor(
    readonly url: string,
    initial: LabState,
  ) {
    this.state = initial
  }

  start(): void {
    if (this.running) return
    this.running = true
    this.connect()
  }

  stop(): void {
    this.running = false
    if (this.reconnect !== null) window.clearTimeout(this.reconnect)
    this.reconnect = null
    this.socket?.close()
    this.socket = null
    this.setStatus('closed')
  }

  subscribe(listener: StateListener): () => void {
    this.listeners.add(listener)
    listener(this.state)
    return () => this.listeners.delete(listener)
  }

  subscribeConnection(listener: ConnectionListener): () => void {
    this.connListeners.add(listener)
    listener(this.status)
    return () => this.connListeners.delete(listener)
  }

  current(): LabState {
    return this.state
  }

  private connect(): void {
    this.setStatus('connecting')
    try {
      if (/^wss?:\/\//.test(this.url)) {
        const ws = new WebSocket(this.url)
        ws.onopen = () => this.setStatus('open')
        ws.onmessage = (e) => this.handle(String(e.data))
        ws.onerror = () => this.setStatus('error')
        ws.onclose = () => this.scheduleReconnect()
        this.socket = ws
      } else {
        const es = new EventSource(this.url)
        es.onopen = () => this.setStatus('open')
        es.onmessage = (e) => this.handle(String(e.data))
        es.onerror = () => {
          this.setStatus('error')
          es.close()
          this.scheduleReconnect()
        }
        this.socket = es
      }
    } catch {
      this.setStatus('error')
      this.scheduleReconnect()
    }
  }

  private scheduleReconnect(): void {
    if (!this.running) return
    this.setStatus('closed')
    if (this.reconnect !== null) return
    this.reconnect = window.setTimeout(() => {
      this.reconnect = null
      if (this.running) this.connect()
    }, RECONNECT_MS)
  }

  private handle(raw: string): void {
    const msg = parseMessage(raw)
    if (!msg) return
    this.state = applyMessage(this.state, msg)
    this.listeners.forEach((l) => l(this.state))
  }

  private setStatus(status: ConnectionStatus): void {
    this.status = status
    this.connListeners.forEach((l) => l(status))
  }
}
