import { useEffect } from "react";
import { AudioRecorder, useAudioRecorder } from "react-audio-voice-recorder";

export interface RecordAudioProps {
  onRecordAudio: (blob: Blob) => void
}

export default function RecordAudio(props: RecordAudioProps) {
  const recorderControls = useAudioRecorder({
    noiseSuppression: true,
    echoCancellation: true,
  });

  useEffect(() => {
    recorderControls.startRecording();
  }, [recorderControls]);
  return (
    <div>
      <AudioRecorder
        recorderControls={recorderControls}
        onRecordingComplete={props.onRecordAudio}
    />
    </div>
  );
}
