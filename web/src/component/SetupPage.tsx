import { useCallback } from "react";
import { FormLabel, TextField, Button, FormControl } from "@mui/material"

export interface SetupPageProps {
    articleText: string;
    setArticleText: React.Dispatch<React.SetStateAction<string>>;
    submitCallback: VoidFunction;
}

export default function SetupPage(props: SetupPageProps) {

    const handleArticleTextChange = useCallback((event: any) => {
        props.setArticleText(event.target.value);
    }, [props]);

    return <FormControl>
        <FormLabel>Input an article</FormLabel>
        <TextField multiline value={props.articleText} onInput={handleArticleTextChange} />
        <Button onClick={props.submitCallback}>Submit</Button>
    </FormControl>;
}