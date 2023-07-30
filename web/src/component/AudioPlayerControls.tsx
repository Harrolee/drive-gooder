interface AudioPlayerControlsProps {
  src: string;
}

export function AudioPlayerControls(props: AudioPlayerControlsProps) {
  return <audio
    src={props.src}
    controls />;
}