import spacy
from spacy.language import Language
from pathlib import Path
from spacy.util import get_model_meta


model_path = Path(__file__).parent
meta = get_model_meta(model_path)
data_dir = f"{meta['lang']}_{meta['name']}-{meta['version']}"
components_path = model_path / data_dir / "training"

@Language.component("vocabulary")
def vocabulary(doc):
    nlp_vocabulary = spacy.load(components_path/"vocabulary")
    return nlp_vocabulary(doc)

@Language.component("articles")
def articles(doc):
    nlp_articles = spacy.load(components_path/"articles")
    return nlp_articles(doc)

@Language.component("punctuation")
def punctuation(doc):
    nlp_punctuation = spacy.load(components_path/"punctuation")
    return nlp_punctuation(doc)

@Language.component("spelling")
def spelling(doc):
    nlp_spelling = spacy.load(components_path/"spelling")
    return nlp_spelling(doc)

@Language.component("grammar_major")
def grammar_major(doc):
    nlp_grammar_major = spacy.load(components_path/"grammar_major")
    return nlp_grammar_major(doc)

@Language.component("grammar_minor")
def grammar_minor(doc):
    nlp_grammar_minor = spacy.load(components_path/"grammar_minor")
    return nlp_grammar_minor(doc)

