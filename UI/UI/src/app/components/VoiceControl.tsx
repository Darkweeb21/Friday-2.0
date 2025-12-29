import { Mic, MicOff, Volume2, VolumeX } from 'lucide-react';

interface VoiceControlProps {
  micEnabled: boolean;
  voiceEnabled: boolean;
  onMicToggle: () => void;
  onVoiceToggle: () => void;
}

export function VoiceControl({ micEnabled, voiceEnabled, onMicToggle, onVoiceToggle }: VoiceControlProps) {
  return (
    <div className="flex gap-3">
      {/* Microphone Toggle */}
      <button
        onClick={onMicToggle}
        className={`flex items-center gap-2 px-4 py-2.5 rounded-lg border transition-all duration-200 ${
          micEnabled
            ? 'bg-blue-500/10 border-blue-500 text-blue-400 shadow-lg shadow-blue-500/20'
            : 'bg-zinc-900 border-zinc-800 text-zinc-500 hover:border-zinc-700'
        }`}
      >
        {micEnabled ? (
          <Mic className="w-4 h-4" />
        ) : (
          <MicOff className="w-4 h-4" />
        )}
        <span className="text-sm">Microphone</span>
        <div className={`w-1.5 h-1.5 rounded-full ${micEnabled ? 'bg-blue-400' : 'bg-zinc-600'}`} />
      </button>

      {/* Speech Output Toggle */}
      <button
        onClick={onVoiceToggle}
        className={`flex items-center gap-2 px-4 py-2.5 rounded-lg border transition-all duration-200 ${
          voiceEnabled
            ? 'bg-teal-500/10 border-teal-500 text-teal-400 shadow-lg shadow-teal-500/20'
            : 'bg-zinc-900 border-zinc-800 text-zinc-500 hover:border-zinc-700'
        }`}
      >
        {voiceEnabled ? (
          <Volume2 className="w-4 h-4" />
        ) : (
          <VolumeX className="w-4 h-4" />
        )}
        <span className="text-sm">Speech Output</span>
        <div className={`w-1.5 h-1.5 rounded-full ${voiceEnabled ? 'bg-teal-400' : 'bg-zinc-600'}`} />
      </button>
    </div>
  );
}