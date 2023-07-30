import { useCallback, useRef } from "react";
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';
import PauseCircleOutlineIcon from '@mui/icons-material/PauseCircleOutline';
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
        <PlayCircleOutlineIcon onClick={handlePlay}/>
        <PauseCircleOutlineIcon onClick={handlePause}/>
    </div>;
}
export default AudioPlayerControls