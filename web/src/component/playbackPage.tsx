import { MenuItem, Select, Slider } from "@mui/material";
import AudioPlayer from 'react-h5-audio-player';
import "../styling/styles.css";
import { useCallback, useEffect, useMemo, useState } from "react";
import { readText } from "../api";

export interface PlaybackPageProps {
    articleText: string;
    splitArticleText: string[];
}

function useObjectUrl(blob: Blob) {
    const url = useMemo(() => URL.createObjectURL(blob), [blob]);
    useEffect(() => URL.revokeObjectURL(url), [blob, url]);
    return url;
}

interface AudioElementProps {
    blob: Blob;
}

function AudioElement(props: AudioElementProps) {
    const src = useObjectUrl(props.blob);
    return <audio
        src={src}
    />;
}

export function PlaybackPage(props: PlaybackPageProps) {
    const [chunkNumber, setChunkNumber] = useState(0);
    const [onPlayBack, setOnPlayBack] = useState(false);
    const [sliderValue, setSliderValue] = useState(1);
    const [emotionValue, setEmotion] = useState("Neutral");
    const [audioBlob, setAudioBlob] = useState<Blob>();

    const handleSliderChange = (event: any) => {
        setSliderValue(event.target.value);
    };

    const handleEmotionChange = (event: any) => {
        setEmotion(event.target.value);
    };

    const getCurrentAudioChuck = useCallback(async () => {
        const currentChunk = props.splitArticleText[chunkNumber];
        const audioChunk = await readText(currentChunk, emotionValue, sliderValue);

        const blob = new Blob([audioChunk], {
            type: 'audio/wav'
        });

        setAudioBlob(blob);
    }, [chunkNumber, emotionValue, props.splitArticleText, sliderValue]);

    useEffect(() => {
        getCurrentAudioChuck();
    }, [getCurrentAudioChuck]);

    if (!audioBlob) {
        return <div>Loading...</div>;
    }

    return <div>
        <AudioPlayer
            autoPlay
            onPlay={e => console.log("onPlay")}
        // other props here
        >
            <AudioElement blob={audioBlob} />
        </AudioPlayer>
        <Select
            value={emotionValue}
            onChange={handleEmotionChange}
            label="Emotion"
        >
            <MenuItem value={"Neutral"}>Neutral</MenuItem>
            <MenuItem value={"Happy"}>Happy</MenuItem>
            <MenuItem value={"Angry"}>Angry</MenuItem>
            <MenuItem value={"Sad"}>Sad</MenuItem>
            <MenuItem value={"Surprise"}>Surprise</MenuItem>
            <MenuItem value={"Dull"}>Dull</MenuItem>
        </Select>
        <Slider
            value={sliderValue}
            onChange={handleSliderChange}
            defaultValue={1.0}
            min={0}
            max={2}
            marks
            step={0.1}
            valueLabelDisplay="auto"
        />
    </div>
}