import modal

app = modal.App(
    "find_keyword"
) 

def download_model_to_image(model_dir, model_name):
    import os
    from huggingface_hub import snapshot_download
    from transformers.utils import move_cache

    os.makedirs(model_dir, exist_ok=True)
    
    snapshot_download(
        model_name,
        local_dir=model_dir
    )
    move_cache()

TOKEN_CLASSIFIER = "ml6team/keyphrase-extraction-distilbert-inspec"
MODEL_DIR = "/token_classifier"
transformers_image = (
    modal.Image.debian_slim()
    .pip_install(
        "torch==2.2.2",
        "transformers==4.40.0",
        "hf-transfer==0.1.6",
        "huggingface_hub==0.22.2",
    )
    .run_function(download_model_to_image,
        timeout=60 * 4,
        kwargs={
            "model_dir": MODEL_DIR,
            "model_name": TOKEN_CLASSIFIER,
        }
    )
)

@app.function(image=transformers_image, gpu="a10g")
def find_keywords(text) -> str:
    """
    If keywords are found, find_keywords returns a string containing the top three keywords from the text.
    If no keywords are found, find_keywords returns a string containing the word "no-tokens-found".
    """
    from transformers import pipeline
    pipe = pipeline("token-classification", model=MODEL_DIR)
    keywords = pipe(text)

    if len(keywords) == 0:
        return "no-tokens-found"
    if len(keywords) > 3:
        keywords = keywords[:3]
    print(keywords)
    keywords = [k.get("word") for k in keywords]
    keywords = " ".join(keywords)
    return keywords