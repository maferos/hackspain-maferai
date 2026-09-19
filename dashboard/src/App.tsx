import { useMemo } from 'react'
import { readConfig, type ViewportSources } from './config'
import type { CameraId } from './state/types'
import { LabStateProvider } from './state/LabStateProvider'
import { HeaderStatus } from './components/HeaderStatus'
import { SimulationViewport } from './components/viewport/SimulationViewport'
import { ExecutionPanel } from './components/execution/ExecutionPanel'
import { BalancePanel } from './components/balance/BalancePanel'
import { RobotTelemetry } from './components/RobotTelemetry'
import { PerceptionPanel } from './components/PerceptionPanel'
import { AutonomyPipeline } from './components/pipeline/AutonomyPipeline'
import { EventLog } from './components/EventLog'

function Dashboard({ sources, camera }: { sources: ViewportSources; camera: CameraId | null }) {
  return (
    <div className="flex h-full flex-col gap-2 p-2">
      <HeaderStatus />
      <main className="dashboard-grid min-h-0 flex-1">
        <div className="min-h-0 min-w-0" style={{ gridArea: 'sim' }}>
          <SimulationViewport sources={sources} initialCamera={camera} />
        </div>
        <div className="grid min-h-0 min-w-0 grid-cols-[1.25fr_1fr] gap-2" style={{ gridArea: 'telemetry' }}>
          <RobotTelemetry />
          <EventLog />
        </div>
        <div className="min-h-0 min-w-0" style={{ gridArea: 'exec' }}>
          <ExecutionPanel />
        </div>
        <div className="min-h-0 min-w-0" style={{ gridArea: 'balance' }}>
          <BalancePanel />
        </div>
        <div className="min-h-0 min-w-0" style={{ gridArea: 'perception' }}>
          <PerceptionPanel />
        </div>
        <div className="min-h-0 min-w-0" style={{ gridArea: 'pipeline' }}>
          <AutonomyPipeline />
        </div>
      </main>
    </div>
  )
}

export default function App() {
  const config = useMemo(readConfig, [])
  return (
    <LabStateProvider
      initialSource={config.source}
      liveUrl={config.liveUrl}
      demoSpeed={config.demoSpeed}
      demoStart={config.demoStart}
      demoPaused={config.demoPaused}
      loop={config.loop}
    >
      <Dashboard sources={config.viewport} camera={config.camera} />
    </LabStateProvider>
  )
}
