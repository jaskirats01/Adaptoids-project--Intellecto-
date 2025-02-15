import React, { useState } from "react";
import axios from "axios";

const AudioRecorder = () => {
    const [recording, setRecording] = useState(false);
    const [audioBlob, setAudioBlob] = useState(null);
    const [transcript, setTranscript] = useState("");
    const [sentiment, setSentiment] = useState("");

    const startRecording = () => {
        setRecording(true);
        // Use MediaRecorder API to record audio
    };

    const stopRecording = (blob) => {
        setRecording(false);
        setAudioBlob(blob);
    };

    const sendAudioToBackend = async () => {
        const formData = new FormData();
        formData.append("audio", audioBlob);

        const response = await axios.post("http://127.0.0.1:8000/api/process_speech/", formData);
        setTranscript(response.data.transcript);
        setSentiment(response.data.sentiment);
    };

    return (
        <div>
            <button onClick={startRecording} disabled={recording}>Start Recording</button>
            <button onClick={stopRecording} disabled={!recording}>Stop Recording</button>
            <button onClick={sendAudioToBackend} disabled={!audioBlob}>Analyze Speech</button>
            
            {transcript && <p>Transcript: {transcript}</p>}
            {sentiment && <p>Sentiment: {sentiment}</p>}
        </div>
    );
};

export default AudioRecorder;