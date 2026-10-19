import { TacticalMap } from './TacticalMap';
import { ShieldAlert, Radio } from 'lucide-react';

function App() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw' }}>
      <header style={{
        height: '60px',
        backgroundColor: '#0f172a',
        borderBottom: '1px solid #1e293b',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 24px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <ShieldAlert color="#38bdf8" size={24} />
          <h1 style={{ fontSize: '18px', letterSpacing: '1px' }}>C2 TACTICAL COP</h1>
          <span style={{ fontSize: '11px', background: '#0284c7', padding: '2px 8px', borderRadius: '4px' }}>
            NATO / NCIA PROTOTYPE
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', fontSize: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Radio size={16} color="#22c55e" />
            <span>LIVE INGESTION ACTIVE</span>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <span style={{ color: '#60a5fa' }}>● FRIENDLY</span>
            <span style={{ color: '#f87171' }}>● HOSTILE</span>
            <span style={{ color: '#fbbf24' }}>● UNKNOWN</span>
          </div>
        </div>
      </header>

      <main style={{ flex: 1, position: 'relative' }}>
        <TacticalMap />
      </main>
    </div>
  );
}

export default App;