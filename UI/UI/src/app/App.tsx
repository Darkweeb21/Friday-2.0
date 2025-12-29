import { useState, useEffect } from 'react';
import { VoiceControl } from './components/VoiceControl';
import { ConversationDisplay } from './components/ConversationDisplay';
import { MessageInput } from './components/MessageInput';
import { DebugPanel } from './components/DebugPanel';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

interface DebugData {
  intent: string;
  confidence: number;
  entities: Record<string, string>;
}

export default function App() {
  const [micEnabled, setMicEnabled] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [debugData, setDebugData] = useState<DebugData>({
    intent: '',
    confidence: 0,
    entities: {},
  });
  const [orbState, setOrbState] = useState<'idle' | 'listening' | 'speaking' | 'typing' | 'pulse'>('idle');
  const [isTyping, setIsTyping] = useState(false);
  const [isResponding, setIsResponding] = useState(false);

  // Update orb state based on conditions
  useEffect(() => {
    // Priority order: typing > responding > mic > voice > idle
    if (isTyping) {
      setOrbState('typing');
    } else if (isResponding) {
      setOrbState('speaking');
    } else if (micEnabled) {
      setOrbState('listening');
    } else if (voiceEnabled) {
      setOrbState('speaking');
    } else {
      setOrbState('idle');
    }
  }, [isTyping, isResponding, micEnabled, voiceEnabled]);

  // Handle typing state change from input
  const handleTypingChange = (typing: boolean) => {
    setIsTyping(typing);
  };

  // Simulate processing a user message and extracting debug data
  const processMessage = (text: string) => {
    // Mock intent extraction
    const lowerText = text.toLowerCase();
    let intent = 'general.query';
    let confidence = 0.75;
    const entities: Record<string, string> = {};

    if (lowerText.includes('weather')) {
      intent = 'weather.query';
      confidence = 0.92;
      entities.location = 'current';
    } else if (lowerText.includes('time') || lowerText.includes('clock')) {
      intent = 'time.query';
      confidence = 0.88;
    } else if (lowerText.includes('reminder') || lowerText.includes('remind')) {
      intent = 'reminder.create';
      confidence = 0.85;
      entities.action = 'create';
    } else if (lowerText.includes('hello') || lowerText.includes('hi')) {
      intent = 'greeting';
      confidence = 0.95;
    }

    setDebugData({ intent, confidence, entities });
  };

  const handleSendMessage = (text: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, newMessage]);

    // Process message for debug data
    processMessage(text);

    // Trigger pulse animation on message send
    setOrbState('pulse');
    
    // After pulse, set to responding state
    setTimeout(() => {
      setIsResponding(true);
      
      // Simulate FRIDAY response
      setTimeout(() => {
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: 'Command received. This is a demo response from FRIDAY 2.0.',
          sender: 'assistant',
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
        
        // Stop responding after message is complete
        setTimeout(() => {
          setIsResponding(false);
        }, 2000);
      }, 800);
    }, 1200); // Duration of pulse animation
  };

  const isActive = micEnabled || voiceEnabled;

  return (
    <div className="min-h-screen w-full bg-black flex justify-center">



    <div className="w-full min-h-screen flex flex-col bg-zinc-950 overflow-hidden">




        {/* Header */}
        <div className="px-6 py-4 border-b border-zinc-900 bg-zinc-950/95 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <div
                  className={`w-2 h-2 rounded-full transition-all duration-300 ${
                    isActive ? 'bg-blue-500 shadow-lg shadow-blue-500/50 animate-pulse' : 'bg-zinc-700'
                  }`}
                />
                <h1 className="text-zinc-100 tracking-wide">FRIDAY 2.0</h1>
              </div>
            </div>
            <div className="flex items-center gap-4 text-xs text-zinc-600">
              <span className="font-mono">v2.0.1</span>
              <span>|</span>
              <span className={isActive ? 'text-blue-400' : ''}>
                {isActive ? 'ACTIVE' : 'STANDBY'}
              </span>
            </div>
          </div>
        </div>

        {/* Main Conversation Area with AI Core Orb */}
        <ConversationDisplay messages={messages} orbState={orbState} />

        {/* Bottom Section: Controls + Input */}
        <div className="border-t border-zinc-900 bg-zinc-950">
          <div className="px-6 py-4 flex items-center gap-6">
            {/* Control Panel */}
            <VoiceControl
              micEnabled={micEnabled}
              voiceEnabled={voiceEnabled}
              onMicToggle={() => setMicEnabled(!micEnabled)}
              onVoiceToggle={() => setVoiceEnabled(!voiceEnabled)}
            />

            {/* Divider */}
            <div className="h-8 w-px bg-zinc-800" />

            {/* Input Section */}
            <div className="flex-1">
              <MessageInput 
                onSend={handleSendMessage}
                onTypingChange={handleTypingChange}
              />
            </div>
          </div>
        </div>

        {/* Debug Panel */}
        <DebugPanel data={debugData} />
      </div>
    </div>
  );
}