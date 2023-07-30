import { useCallback, useState } from "react";
import SetupPage from "./SetupPage";
import { PlaybackPage } from "./playbackPage";
import { getSplit } from "../api";
import React from "react";

export interface AuthenticatedTemplateProps {
}

export function AuthenticatedTemplate(props: AuthenticatedTemplateProps) {
    const [articleText, setArticleText] = useState("");
    const [splitArticleText, setSplitArticleText] = useState<string[]>([]);
    const [articleSubmitted, setArticleSubmitted] = useState(false);

    const handleArticleSubmit = useCallback(async () => {
        const response = await getSplit(articleText);
        setSplitArticleText(response);

        setArticleSubmitted(true);
    }, [articleText]);

    if (!articleSubmitted) {
        return <SetupPage
            articleText={articleText}
            setArticleText={setArticleText}
            submitCallback={handleArticleSubmit}
             />
    }

    return <PlaybackPage
            articleText={articleText}
            splitArticleText={splitArticleText} />
}