const API = "http://127.0.0.1:8000";



export async function sendCommand(text: string) {
  const res = await fetch(`${API}/api/command`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!res.ok) throw new Error("Command failed");
  return res.json();
}

export async function getState() {
  const res = await fetch(`${API}/api/state`);
  if (!res.ok) throw new Error("State fetch failed");
  return res.json();
}

export async function toggleMic() {
  const res = await fetch(`${API}/api/mic/toggle`, { method: "POST" });
  if (!res.ok) throw new Error("Mic toggle failed");
  return res.json();
}

export async function toggleSpeech() {
  const res = await fetch(`${API}/api/speech/toggle`, { method: "POST" });
  if (!res.ok) throw new Error("Speech toggle failed");
  return res.json();
}
