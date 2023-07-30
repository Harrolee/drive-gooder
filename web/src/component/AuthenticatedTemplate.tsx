import { useCallback, useState } from "react";
import SetupPage from "./SetupPage";
import { PlaybackPage } from "./PlaybackPage";
import { getSplit } from "../api";

export interface AuthenticatedTemplateProps {
}

export function AuthenticatedTemplate(props: AuthenticatedTemplateProps) {
    const [articleText, setArticleText] = useState("");
    const [articleSubmitted, setArticleSubmitted] = useState(false);

    const handleArticleSubmit = useCallback(async () => {
        const response = await getSplit(articleText);
        console.log(response);

        setArticleSubmitted(true);
    }, [articleText]);

    if (!articleSubmitted) {
        return <SetupPage
            articleText={articleText}
            setArticleText={setArticleText}
            submitCallback={handleArticleSubmit} />
    }

    return <PlaybackPage
            articleText={articleText} />
}