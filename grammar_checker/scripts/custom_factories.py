import spacy
from spacy.language import Language
from pathlib import Path
from spacy.util import get_model_meta


model_path = Path(__file__).parent
meta = get_model_meta(model_path)
data_dir = f"{meta['lang']}_{meta['name']}-{meta['version']}"
components_path = model_path / data_dir / "training"


@Language.component("grammar_checker")
def grammar_checker(doc):
    nlp_grammar = spacy.load(components_path)
    return nlp_grammar(doc)