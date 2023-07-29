
export default function SetupPage({
    articleText, setArticleText }:
    { articleText: any, setArticleText: any }) {

    const handleArticleTextChange = (event: any) => {
        setArticleText(event.target.value);
    }

    return <div>
        <h2>Input a Article</h2>
        <textarea name="articleTextarea" value={articleText} onInput={handleArticleTextChange} />
    </div>
}