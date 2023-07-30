import { MenuItem, Select, Slider } from "@mui/material";
import AudioPlayer from 'react-h5-audio-player';
import { useState } from "react";

export interface PlaybackPageProps {
    articleText: string;
    splitArticleText: string[];
}

export function PlaybackPage(props: PlaybackPageProps) {
    const [onPlayBack, setOnPlayBack] = useState(false);
    const [sliderValue, setSliderValue] = useState(1);
    const [emotionValue, setEmotion] = useState("Neutral");

    const handleSliderChange = (event: any) => {
        setSliderValue(event.target.value);
    };

    const handleEmotionChange = (event: any) => {
        setEmotion(event.target.value);
    };

    return <div>
        <AudioPlayer
            autoPlay
            src="./audio/buzzbuzzbuzz.mp3"
            onPlay={e => console.log("onPlay")}
        // other props here
        />
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