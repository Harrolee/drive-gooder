"use client";
import { useState } from "react";
import Button from "@mui/material/Button";
import { ReactMic, ReactMicStopEvent } from "react-mic";
import { getSpeech } from "./api";
export default function RecordForSpeech() {
    const [isRecording, setIsRecording] = useState(false);
    const [audioUrl, setAudioUrl] = useState<string>("");

    const handleStop = async (recordedData: ReactMicStopEvent) => {
        const audioData = await getSpeech(recordedData);
        if (audioData != undefined) {
            setAudioUrl(
                URL.createObjectURL(new Blob([audioData], { type: "audio/wav" }))
            );
        } else {
            console.log("no response");
        }
    };

    const toggleIsRecording = () => {
        if (isRecording) {
            setIsRecording(false);
        } else {
            setIsRecording(true);
        }
    };

    return (
        <div className="w-2/3">
            <h2>Hear a response</h2>
            <Button onClick={toggleIsRecording} variant="contained">
                {isRecording ? "Send" : "Ask"}
            </Button>
            <ReactMic
                record={isRecording}
                className="sound-wave"
                onStop={handleStop}
                strokeColor="#0d6efd"
                backgroundColor="#000000"
            />

            {audioUrl != "" && (
                <audio controls src={audioUrl}>
                    <a href={audioUrl}>Download speech</a>
                </audio>
            )}
        </div>
    );
}
