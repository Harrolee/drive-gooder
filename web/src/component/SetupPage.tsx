import { useCallback } from "react";
import { FormLabel, TextField, Button, FormControl, Box } from "@mui/material"

export interface SetupPageProps {
    articleText: string;
    setArticleText: React.Dispatch<React.SetStateAction<string>>;
    submitCallback: VoidFunction;
}

export default function SetupPage(props: SetupPageProps) {

    const handleArticleTextChange = useCallback((event: any) => {
        props.setArticleText(event.target.value);
    }, [props]);

    return <Box display="flex" justifyContent="center" alignItems="center" >
        <FormControl>
            <FormLabel>Input an article</FormLabel>
            <TextField multiline value={props.articleText} onInput={handleArticleTextChange} inputProps={{
                style: {
                    height: "400px",
                    width: "400px",
                },
            }} />
            <Button onClick={props.submitCallback}>Submit</Button>
        </FormControl>
    </Box>;
}