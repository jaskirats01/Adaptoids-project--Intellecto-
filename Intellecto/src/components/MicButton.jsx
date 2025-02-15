import { useState, useRef } from "react";

function MicButton() {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const [audioUrl, setAudioUrl] = useState(null);

  const handleMicClick = async () => {
    if (!isRecording) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        const audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
          const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
          const url = URL.createObjectURL(audioBlob);
          setAudioUrl(url);
        };

        mediaRecorderRef.current = mediaRecorder;
        mediaRecorder.start();
        setIsRecording(true);
      } catch (error) {
        console.error("Mic access error:", error);
      }
    } else {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      <button 
        onClick={handleMicClick}
        style={{
          backgroundColor: isRecording ? "red" : "green",
          color: "white",
          padding: "10px 20px",
          borderRadius: "50px",
          border: "none",
          cursor: "pointer",
          fontSize: "16px",
        }}
      >
        {isRecording ? "Stop Recording" : "Start Recording"}
      </button>

      {audioUrl && (
        <div style={{ marginTop: "20px" }}>
          <h3>Recorded Audio:</h3>
          <audio controls>
            <source src={audioUrl} type="audio/wav" />
          </audio>
        </div>
      )}
    </div>
  );
}

export default MicButton;
