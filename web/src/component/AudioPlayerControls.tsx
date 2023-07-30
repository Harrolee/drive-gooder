import { useCallback, useRef } from "react";

interface AudioPlayerControlsProps {
    src: string;
}

export function AudioPlayerControls(props: AudioPlayerControlsProps) {
    const audioRef = useRef<HTMLAudioElement>(null);

    const handlePlay = useCallback(() => {
        console.log("Staring to play");
        audioRef.current?.play();
    }, []);

    return <div>
        <audio
            src={props.src}
            ref={audioRef} />
        <button onClick={handlePlay}>Play</button>
    </div>;
}