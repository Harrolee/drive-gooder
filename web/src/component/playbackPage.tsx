import { MenuItem, Select, Slider } from "@mui/material";
import "../styling/styles.css";
import { useCallback, useEffect, useState } from "react";
import { readText, summarize } from "../api";
import { AudioPlayerControls } from "./AudioPlayerControls"

export interface PlaybackPageProps {
    articleText: string;
    splitArticleText: string[];
}

export function PlaybackPage(props: PlaybackPageProps) {
    // const [currentChunkNumber, setCurrentChunkNumber] = useState(0);
    // const [onPlayBack, setOnPlayBack] = useState(false);
    const [sliderValue, setSliderValue] = useState(1);
    const [emotionValue, setEmotion] = useState("Neutral");
    const [audioUrl, setAudioUrl] = useState<string>();

    const handleSliderChange = (event: any) => {
        setSliderValue(event.target.value);
    };

    const handleEmotionChange = (event: any) => {
        setEmotion(event.target.value);
    };

    const getSummary = useCallback(async () => {
        const audio = await summarize(props.articleText, emotionValue, sliderValue);
        setAudioUrl(URL.createObjectURL(audio));
    }, [emotionValue, props.articleText, sliderValue]);

    // const getCurrentAudioChuck = useCallback(async (chunkNumber: number) => {
    //     const currentChunk = props.splitArticleText[chunkNumber];
    //     const audioChunk = await readText(currentChunk, emotionValue, sliderValue);

    //     const blob = new Blob([audioChunk], {
    //         type: 'audio/wav'
    //     });

    //     setAudioUrl(URL.createObjectURL(blob));
    // }, [emotionValue, props.splitArticleText, sliderValue]);

    useEffect(() => {
        getSummary();
    }, [getSummary]);

    if (!audioUrl) {
        return <div>Loading...</div>;
    }

    return <div>
        <AudioPlayerControls src={audioUrl} />
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