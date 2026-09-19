/**
 * React binding of the state source.
 *
 * `LabStateProvider` owns one `LabStateSource` (demo or live), re-renders on
 * every published snapshot and exposes the state, the connection status and
 * the demo playback controls through `useLabState()`.
 */

import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import type { LabState } from './types'
import type { ConnectionStatus, DemoControls, LabStateSource, SourceKind } from './sources/LabStateSource'
import { DemoSource } from './sources/DemoSource'
import { LiveSource } from './sources/LiveSource'
import { emptyState } from './emptyState'

export interface LabContextValue {
  state: LabState
  source: SourceKind
  connection: ConnectionStatus
  liveUrl: string
  /** Playback controls, present only for the demo source. */
  demo: DemoControls | null
  setSource(kind: SourceKind): void
}

const LabContext = createContext<LabContextValue | null>(null)

export interface LabStateProviderProps {
  initialSource: SourceKind
  liveUrl: string
  demoSpeed?: number
  demoStart?: number
  demoPaused?: boolean
  loop?: boolean
  children: ReactNode
}

export function LabStateProvider({ initialSource, liveUrl, demoSpeed = 1, demoStart = 0, demoPaused = false, loop = false, children }: LabStateProviderProps) {
  const [sourceKind, setSourceKind] = useState<SourceKind>(initialSource)
  const [state, setState] = useState<LabState>(() => emptyState())
  const [connection, setConnection] = useState<ConnectionStatus>('idle')

  const source: LabStateSource = useMemo(() => {
    if (sourceKind === 'live') return new LiveSource(liveUrl, emptyState())
    return new DemoSource({ speed: demoSpeed, loopAfterSeconds: loop ? 6 : null, startAt: demoStart, paused: demoPaused })
  }, [sourceKind, liveUrl, demoSpeed, demoStart, demoPaused, loop])

  useEffect(() => {
    const offState = source.subscribe(setState)
    const offConn = source.subscribeConnection(setConnection)
    source.start()
    return () => {
      offState()
      offConn()
      source.stop()
    }
  }, [source])

  const value = useMemo<LabContextValue>(
    () => ({
      state,
      source: sourceKind,
      connection,
      liveUrl,
      demo: source.kind === 'demo' ? (source as DemoSource) : null,
      setSource: setSourceKind,
    }),
    [state, sourceKind, connection, liveUrl, source],
  )

  return <LabContext.Provider value={value}>{children}</LabContext.Provider>
}

export function useLabState(): LabContextValue {
  const ctx = useContext(LabContext)
  if (!ctx) throw new Error('useLabState must be used inside LabStateProvider')
  return ctx
}
