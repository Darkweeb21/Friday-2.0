import { ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';

interface DebugData {
  intent: string;
  confidence: number;
  entities: Record<string, string>;
}

interface DebugPanelProps {
  data: DebugData;
}

export function DebugPanel({ data }: DebugPanelProps) {
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <div className="border-t border-zinc-800 bg-zinc-950">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between px-6 py-3 hover:bg-zinc-900/50 transition-colors"
      >
        <span className="text-xs text-zinc-500 font-mono uppercase tracking-wider">Developer Mode</span>
        {isExpanded ? (
          <ChevronDown className="w-4 h-4 text-zinc-600" />
        ) : (
          <ChevronUp className="w-4 h-4 text-zinc-600" />
        )}
      </button>

      {isExpanded && (
        <div className="px-6 pb-4 space-y-3 font-mono text-xs">
          {/* Intent */}
          <div className="flex items-baseline gap-3">
            <span className="text-zinc-600 min-w-[100px]">Intent:</span>
            <span className="text-blue-400">{data.intent || 'null'}</span>
          </div>

          {/* Confidence */}
          <div className="flex items-baseline gap-3">
            <span className="text-zinc-600 min-w-[100px]">Confidence:</span>
            <div className="flex items-center gap-2">
              <span className="text-teal-400">
                {data.confidence ? (data.confidence * 100).toFixed(1) + '%' : '0.0%'}
              </span>
              <div className="flex-1 h-1.5 bg-zinc-900 rounded-full overflow-hidden w-32">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-teal-500 transition-all duration-300"
                  style={{ width: `${(data.confidence || 0) * 100}%` }}
                />
              </div>
            </div>
          </div>

          {/* Entities */}
          <div className="flex items-start gap-3">
            <span className="text-zinc-600 min-w-[100px]">Entities:</span>
            <div className="flex-1">
              {Object.keys(data.entities).length === 0 ? (
                <span className="text-zinc-700">{'{ }'}</span>
              ) : (
                <div className="space-y-1">
                  <span className="text-zinc-700">{'{'}</span>
                  {Object.entries(data.entities).map(([key, value], index) => (
                    <div key={key} className="pl-4">
                      <span className="text-purple-400">{key}</span>
                      <span className="text-zinc-600">: </span>
                      <span className="text-green-400">&quot;{value}&quot;</span>
                      {index < Object.keys(data.entities).length - 1 && (
                        <span className="text-zinc-600">,</span>
                      )}
                    </div>
                  ))}
                  <span className="text-zinc-700">{'}'}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
