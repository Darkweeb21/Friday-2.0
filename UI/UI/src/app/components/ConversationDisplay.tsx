import { useEffect, useRef } from 'react';
import { AICoreOrb } from './AICoreOrb';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

interface ConversationDisplayProps {
  messages: Message[];
  orbState: 'idle' | 'listening' | 'speaking' | 'typing' | 'pulse';
}

export function ConversationDisplay({ messages, orbState }: ConversationDisplayProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: 'smooth',
    });
  }, [messages]);

  return (
    <div className="flex-1 relative min-h-0">
      {/* AI Core Orb */}
      <AICoreOrb state={orbState} />

      {/* Scrollable chat area */}
      <div
        ref={scrollRef}
        className="relative z-10 h-full overflow-y-auto px-8 py-6 space-y-4"
        style={{
          scrollbarWidth: 'thin',
          scrollbarColor: '#27272a transparent',
        }}
      >
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center">
            <p className="text-zinc-600 text-sm">
              No messages yet. Start by typing a command below.
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className="flex flex-col gap-1 max-w-[75%]">
                <div
                  className={`rounded-xl px-4 py-3 ${
                    message.sender === 'user'
                      ? 'bg-blue-500/10 border border-blue-500/30 text-blue-100'
                      : 'bg-zinc-900 border border-zinc-800 text-zinc-200'
                  }`}
                >
                  <p className="whitespace-pre-wrap break-words leading-relaxed">
                    {message.text}
                  </p>
                </div>
                <span
                  className={`text-xs text-zinc-600 px-2 ${
                    message.sender === 'user' ? 'text-right' : 'text-left'
                  }`}
                >
                  {message.timestamp.toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
