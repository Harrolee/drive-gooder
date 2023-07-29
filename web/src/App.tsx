import React, { useState } from "react";
import "./App.css";
import AudioPlayer from 'react-h5-audio-player';
import SetupPage from "./component/SetupPage";
import Slider from "@mui/material/Slider";
import Select from "@mui/material/Select";
import { Button, MenuItem } from "@mui/material";

function App() {
  const [onPlayBack, setOnPlayBack] = useState(false);
  const [sliderValue, setSliderValue] = useState(1);
  const [emotionValue, setEmotion] = useState("Neutral");
  const [articleText, setArticleText] = useState("");

  const handleSliderChange = (event: any) => {
    setSliderValue(event.target.value);
  };

  const handleEmotionChange = (event: any) => {
    setEmotion(event.target.value);
  };

  const submitArticle = () => {
    setOnPlayBack(true);
    console.log(`Article Text: ${articleText}`);
    console.log(`Slider Value: ${sliderValue}`);
    console.log(`Emotion: ${emotionValue}`);
    //TODO: Split text
  };
  const goToSetup = () => {
    setArticleText("");
    setEmotion("Neutral");
    setSliderValue(1);
    setOnPlayBack(false);
  };
  return (
    <div className="App">
      {onPlayBack ? null : SetupPage({ articleText, setArticleText })}
      <Button onClick={onPlayBack ? goToSetup : submitArticle}>Submit</Button>
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
  );
}

export default App;