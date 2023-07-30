import { MenuItem, Select, Slider } from "@mui/material";
import "../styling/styles.css";
import { useCallback, useState } from "react";
import { ask, readText, summarize } from "../api";
import { AudioPlayerControls } from "./AudioPlayerControls"
import RecordAudio from "./AudioRecorder";
import { Button } from "@mui/material";

export interface PlaybackPageProps {
    articleText: string;
    splitArticleText: string[];
}

export function PlaybackPage(props: PlaybackPageProps) {
    const [currentChunkNumber, setCurrentChunkNumber] = useState(0);
    // const [onPlayBack, setOnPlayBack] = useState(false);
    const [sliderValue, setSliderValue] = useState(1);
    const [emotionValue, setEmotion] = useState("Neutral");
    const [audioUrl, setAudioUrl] = useState<string>();
    const [currentlyAsking, setCurrentlyAsking] = useState(false);

    const handleAsk = async (blob: Blob) =>{
        setCurrentlyAsking(false);
        const response = await ask(blob, props.articleText, emotionValue, sliderValue);
        const url = URL.createObjectURL(response);
        setAudioUrl(url);
    };

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

    const getCurrentAudioChuck = useCallback(async () => {
        const currentChunk = props.splitArticleText[currentChunkNumber];
        const audioChunk = await readText(currentChunk, emotionValue, sliderValue);

        const blob = new Blob([audioChunk], {
            type: 'audio/wav'
        });

        setAudioUrl(URL.createObjectURL(blob));
    }, [emotionValue, props.splitArticleText, sliderValue, currentChunkNumber]);

    const handleSummarize = useCallback(async () => {
        setAudioUrl(undefined);
        await getSummary();
    }, [getSummary]);

    const handleRead = useCallback(async () => {
        setAudioUrl(undefined);
        setCurrentChunkNumber(0);
        await getCurrentAudioChuck();
    }, [getCurrentAudioChuck]);

    const handleStartAsking = useCallback(() => {
        setAudioUrl(undefined);
        setCurrentlyAsking(true);
    }, []);

    return <div>
        <div>
            <Button onClick={handleRead}>Read</Button>
            <Button onClick={handleSummarize}>Summarize</Button>
            <Button onClick={handleStartAsking}>Ask</Button>
        </div>
        {audioUrl && <AudioPlayerControls src={audioUrl} />}
        {currentlyAsking && <RecordAudio onRecordAudio={handleAsk} />}
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