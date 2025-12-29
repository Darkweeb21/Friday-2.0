import { Send } from 'lucide-react';
import { useState, KeyboardEvent, useEffect } from 'react';

interface MessageInputProps {
  onSend: (message: string) => void;
  onTypingChange?: (isTyping: boolean) => void;
  disabled?: boolean;
}

export function MessageInput({ onSend, onTypingChange, disabled }: MessageInputProps) {
  const [message, setMessage] = useState('');

  // Notify parent when typing state changes
  useEffect(() => {
    if (onTypingChange) {
      onTypingChange(message.length > 0);
    }
  }, [message, onTypingChange]);

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex items-center gap-3">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type a command…"
        disabled={disabled}
        className="flex-1 bg-zinc-900 border border-zinc-800 text-zinc-200 placeholder:text-zinc-600 rounded-lg px-4 py-2.5 outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20 transition-all"
      />
      <button
        onClick={handleSend}
        disabled={!message.trim() || disabled}
        className={`p-2.5 rounded-lg transition-all ${
          message.trim() && !disabled
            ? 'bg-blue-500 hover:bg-blue-600 text-white shadow-lg shadow-blue-500/30'
            : 'bg-zinc-900 border border-zinc-800 text-zinc-600 cursor-not-allowed'
        }`}
      >
        <Send className="w-4 h-4" />
      </button>
    </div>
  );
}