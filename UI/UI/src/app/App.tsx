import { useState, useEffect } from "react";
import { VoiceControl } from "./components/VoiceControl";
import { ConversationDisplay } from "./components/ConversationDisplay";
import { MessageInput } from "./components/MessageInput";
import { DebugPanel } from "./components/DebugPanel";

import {
  sendCommand,
  getState,
  toggleMic,
  toggleSpeech,
} from "../api/friday";

interface Message {
  id: string;
  text: string;
  sender: "user" | "assistant";
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
    intent: "",
    confidence: 0,
    entities: {},
  });

  const [orbState, setOrbState] = useState<
    "idle" | "listening" | "speaking" | "typing" | "pulse"
  >("idle");

  const [isTyping, setIsTyping] = useState(false);
  const [isResponding, setIsResponding] = useState(false);

  // ----------------------------------------
  // 🔁 Sync backend voice state on load
  // ----------------------------------------
  useEffect(() => {
    getState().then((state) => {
      setMicEnabled(state.mic_enabled);
      setVoiceEnabled(state.speech_enabled);
    });
  }, []);

  // ----------------------------------------
  // 🧠 Orb state logic (priority-based)
  // ----------------------------------------
  useEffect(() => {
    if (isTyping) {
      setOrbState("typing");
    } else if (isResponding) {
      setOrbState("speaking");
    } else if (micEnabled) {
      setOrbState("listening");
    } else if (voiceEnabled) {
      setOrbState("speaking");
    } else {
      setOrbState("idle");
    }
  }, [isTyping, isResponding, micEnabled, voiceEnabled]);

  // ----------------------------------------
  // 🎙️ Remote Mic Toggle (API)
  // ----------------------------------------
  const handleMicToggle = async () => {
    const res = await toggleMic();
    setMicEnabled(res.mic_enabled);
  };

  // ----------------------------------------
  // 🔊 Remote Speech Toggle (API)
  // ----------------------------------------
  const handleVoiceToggle = async () => {
    const res = await toggleSpeech();
    setVoiceEnabled(res.speech_enabled);
  };

  // ----------------------------------------
  // ⌨️ Typing state from input
  // ----------------------------------------
  const handleTypingChange = (typing: boolean) => {
    setIsTyping(typing);
  };

  // ----------------------------------------
  // 📤 Send message → backend
  // ----------------------------------------
  const handleSendMessage = async (text: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsResponding(true);

    try {
      const res = await sendCommand(text);

      // Debug panel (REAL backend data)
      setDebugData({
        intent: res.intent,
        confidence: res.confidence,
        entities: res.entities || {},
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: res.reply,
        sender: "assistant",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          text: "Backend error. Please check server.",
          sender: "assistant",
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsResponding(false);
    }
  };

  const isActive = micEnabled || voiceEnabled;

  // ----------------------------------------
  // 🖥️ UI
  // ----------------------------------------
  return (
    <div className="min-h-screen w-full bg-black flex justify-center">
      <div className="w-full h-screen flex flex-col bg-zinc-950 overflow-hidden">


        {/* Header */}
        <div className="px-6 py-4 border-b border-zinc-900 bg-zinc-950/95 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <div
                  className={`w-2 h-2 rounded-full transition-all duration-300 ${
                    isActive
                      ? "bg-blue-500 shadow-lg shadow-blue-500/50 animate-pulse"
                      : "bg-zinc-700"
                  }`}
                />
                <h1 className="text-zinc-100 tracking-wide">FRIDAY 2.0</h1>
              </div>
            </div>
            <div className="flex items-center gap-4 text-xs text-zinc-600">
              <span className="font-mono">v2.0.1</span>
              <span>|</span>
              <span className={isActive ? "text-blue-400" : ""}>
                {isActive ? "ACTIVE" : "STANDBY"}
              </span>
            </div>
          </div>
        </div>

        {/* Conversation + Orb */}
        <ConversationDisplay messages={messages} orbState={orbState} />

        {/* Controls + Input */}
        <div className="border-t border-zinc-900 bg-zinc-950">
          <div className="px-6 py-4 flex items-center gap-6">
            <VoiceControl
              micEnabled={micEnabled}
              voiceEnabled={voiceEnabled}
              onMicToggle={handleMicToggle}
              onVoiceToggle={handleVoiceToggle}
            />

            <div className="h-8 w-px bg-zinc-800" />

            <div className="flex-1">
              <MessageInput
                onSend={handleSendMessage}
                onTypingChange={handleTypingChange}
              />
            </div>
          </div>
        </div>

        {/* Debug */}
        <DebugPanel data={debugData} />
      </div>
    </div>
  );
}
