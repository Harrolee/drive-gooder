import { useCallback } from "react";

export interface SetupPageProps {
    articleText: string;
    setArticleText: React.Dispatch<React.SetStateAction<string>>;
    submitCallback: VoidFunction;
}

export default function SetupPage(props: SetupPageProps) {

    const handleArticleTextChange = useCallback((event: any) => {
        props.setArticleText(event.target.value);
    }, [props]);

    return <div>
        <h2>Input a Article</h2>
        <textarea name="articleTextarea" value={props.articleText} onInput={handleArticleTextChange} />
        <button onClick={props.submitCallback}>Submit</button>
    </div>
}