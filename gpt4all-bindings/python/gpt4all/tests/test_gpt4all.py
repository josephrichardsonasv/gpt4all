import sys
from io import StringIO

from gpt4all import GPT4All, Embed4All
import time
import pytest

def test_inference():
    model = GPT4All(model_name='orca-mini-3b.ggmlv3.q4_0.bin')
    output_1 = model.generate('hello', top_k=1)

    with model.chat_session():
        response = model.generate(prompt='hello', top_k=1)
        response = model.generate(prompt='write me a short poem', top_k=1)
        response = model.generate(prompt='thank you', top_k=1)
        print(model.current_chat_session)

    output_2 = model.generate('hello', top_k=1)

    assert output_1 == output_2

    tokens = []
    for token in model.generate('hello', streaming=True):
        tokens.append(token)

    assert len(tokens) > 0

    with model.chat_session():
        tokens = list(model.generate(prompt='hello', top_k=1, streaming=True))
        model.current_chat_session.append({'role': 'assistant', 'content': ''.join(tokens)})

        tokens = list(model.generate(prompt='write me a poem about dogs', top_k=1, streaming=True))
        model.current_chat_session.append({'role': 'assistant', 'content': ''.join(tokens)})

        print(model.current_chat_session)


def do_long_input(model):
    long_input = " ".join(["hello how are you"] * 40)

    with model.chat_session():
        # llmodel should limit us to 128 even if we ask for more
        model.generate(long_input, n_batch=512)
        print(model.current_chat_session)


def test_inference_long_orca_3b():
    model = GPT4All(model_name="orca-mini-3b.ggmlv3.q4_0.bin")
    do_long_input(model)


def test_inference_long_falcon():
    model = GPT4All(model_name='ggml-model-gpt4all-falcon-q4_0.bin')
    do_long_input(model)


def test_inference_long_llama_7b():
    model = GPT4All(model_name="orca-mini-7b.ggmlv3.q4_0.bin")
    do_long_input(model)


def test_inference_long_llama_13b():
    model = GPT4All(model_name='ggml-nous-hermes-13b.ggmlv3.q4_0.bin')
    do_long_input(model)


def test_inference_long_mpt():
    model = GPT4All(model_name='ggml-mpt-7b-chat.bin')
    do_long_input(model)


def test_inference_long_replit():
    model = GPT4All(model_name='ggml-replit-code-v1-3b.bin')
    do_long_input(model)


def test_inference_long_groovy():
    model = GPT4All(model_name='ggml-gpt4all-j-v1.3-groovy.bin')
    do_long_input(model)


def test_inference_hparams():
    model = GPT4All(model_name='orca-mini-3b.ggmlv3.q4_0.bin')

    output = model.generate("The capital of france is ", max_tokens=3)
    assert 'Paris' in output


def test_inference_falcon():
    model = GPT4All(model_name='ggml-model-gpt4all-falcon-q4_0.bin')
    prompt = 'hello'
    output = model.generate(prompt)
    assert isinstance(output, str)
    assert len(output) > 0


def test_inference_mpt():
    model = GPT4All(model_name='ggml-mpt-7b-chat.bin')
    prompt = 'hello'
    output = model.generate(prompt)
    assert isinstance(output, str)
    assert len(output) > 0

def test_embedding():
    text = 'The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox jumps over the lazy dog The quick brown fox'
    embedder = Embed4All()
    output = embedder.embed(text)
    #for i, value in enumerate(output):
        #print(f'Value at index {i}: {value}')
    assert len(output) == 384

def test_empty_embedding():
    text = ''
    embedder = Embed4All()
    with pytest.raises(ValueError):
        output = embedder.embed(text)
