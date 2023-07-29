from fastllama import Model

# use this: https://github.com/PotatoSpudowski/fastLLaMa

# init the model (DL A MODEL, LEE)
MODEL_PATH = "./models/7B/ggml-model-q4_0.bin"

model = Model(
    path=MODEL_PATH,  # path to model
    num_threads=8,  # number of threads to use
    n_ctx=512,  # context size of model
    # size of last n tokens (used for repetition penalty) (Optional)
    last_n_size=64,
    seed=0,  # seed for random number generator (Optional)
    n_batch=128,  # batch size (Optional)
    use_mmap=False,  # use mmap to load model (Optional)
)


# ingesting prompts
prompt = """Transcript of a dialog, where the User interacts with an Assistant named Bob. Bob is helpful, kind, honest, good at writing, and never fails to answer the User's requests immediately and with precision.

User: Hello, Bob.
Bob: Hello. How may I help you today?
User: Please tell me the largest city in Europe.
Bob: Sure. The largest city in Europe is Moscow, the capital of Russia.
User: """

res = model.ingest(prompt, is_system_prompt=True)  # ingest model with prompt


# generate output

def stream_token(x: str) -> None:
    """
    This function is called by the library to stream tokens
    """
    print(x, end='', flush=True)


res = model.generate(
    num_tokens=100,
    top_p=0.95,  # top p sampling (Optional)
    temp=0.8,  # temperature (Optional)
    repeat_penalty=1.0,  # repetition penalty (Optional)
    streaming_fn=stream_token,  # streaming function
    # stop generation when this word is encountered (Optional)
    stop_words=["User:", "\n"]
)
