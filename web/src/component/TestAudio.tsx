import { useState } from "react";
import { AudioRecorder } from "react-audio-voice-recorder";
// const {
//   startRecording,
//   stopRecording,
//   togglePauseResume,
//   recordingBlob,
//   isRecording,
//   isPaused,
//   recordingTime,
//   mediaRecorder,
// } = useAudioRecorder();

export default function RecordAudio() {
  const addAudioElement = (blob: Blob) => {
    const url = URL.createObjectURL(blob);
    const audio = document.createElement("audio");
    audio.src = url;
    audio.controls = true;
    document.body.appendChild(audio);
  };

  return (
    <AudioRecorder
      onRecordingComplete={addAudioElement}
      audioTrackConstraints={{
        noiseSuppression: true,
        echoCancellation: true,
      }}
      downloadOnSavePress={true}
      downloadFileExtension="webm"
    />
  );
}
