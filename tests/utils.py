import guidance
import pytest
import torch

opanai_model_cache = {}

def get_llm(model_name, caching=False, **kwargs):
    """ Get an LLM by name.
    """
    if model_name.startswith("openai:"):
        return get_openai_llm(model_name[7:], caching, **kwargs)
    elif model_name.startswith("transformers:"):
        return get_transformers_llm(model_name[13:], caching, **kwargs)

def get_openai_llm(model_name, caching=False, **kwargs):
    """ Get an OpenAI LLM with model reuse and smart test skipping.
    """

    # we cache the models so lots of tests using the same model don't have to
    # load it over and over again
    key = model_name+"_"+str(caching)
    if key not in opanai_model_cache:
        opanai_model_cache[key] = guidance.llms.OpenAI(model_name, caching=caching, **kwargs)
    llm = opanai_model_cache[key]

    if llm.api_key is None:
        pytest.skip("OpenAI token not found")

    return llm

transformers_model_cache = {}

def get_transformers_llm(model_name, caching=False):
    """ Get an OpenAI LLM with model reuse.
    """

    # we cache the models so lots of tests using the same model don't have to
    # load it over and over again
    key = model_name+"_"+str(caching)
    if key not in transformers_model_cache:
        #check gpu
        if torch.cuda.is_available():
            transformers_model_cache[key] = guidance.llms.Transformers(model_name, caching=caching, device="cuda:0")
        else:
            transformers_model_cache[key] = guidance.llms.Transformers(model_name, caching=caching)

    return transformers_model_cache[key]
