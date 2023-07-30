import { AudioRecorder } from "react-audio-voice-recorder";

export interface RecordAudioProps {
  onRecordAudio: (blob: Blob) => void
}

export default function RecordAudio(props: RecordAudioProps) {
  
  return (
    <div>
      <h2>Ask a Question!</h2>
      <AudioRecorder
      onRecordingComplete={props.onRecordAudio}
      audioTrackConstraints={{
        noiseSuppression: true,
        echoCancellation: true,
      }}
    />
    </div>
  );
}
