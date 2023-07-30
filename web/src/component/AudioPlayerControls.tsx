import { useCallback, useRef } from "react";

interface AudioPlayerControlsProps {
    src: string;
}

export function AudioPlayerControls(this: any, props: AudioPlayerControlsProps) {
    const audioRef = useRef<HTMLAudioElement>(null);
    const handlePlay = useCallback(() => {
        console.log("Staring to play");
        audioRef.current?.play();
    }, []);
    const handlePause = useCallback(() => {
      audioRef.current?.pause();
  }, []);


    return <div>
        <audio
            id = "audio"
            src={props.src}
            ref={audioRef}/>
        <button onClick={handlePlay}>Play</button>
        <button onClick={handlePause}>Pause</button>
    </div>;
}
export default AudioPlayerControls