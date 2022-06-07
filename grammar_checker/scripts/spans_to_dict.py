from pathlib import Path
import json
import typer
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
from sklearn.utils.class_weight import compute_class_weight
import numpy as np


def main(loc: Path, lang: str):
    """
    Set the NER data into the doc.spans.
    (The SpanCategorizer component uses the doc.spans)
    """
    paths = list(Path(loc).rglob('*.spacy'))
    nlp = spacy.blank(lang)
    class_weights = dict()
    for f in tqdm(paths):
        y_labels = []
        span_key = "_".join(f.stem.split("_")[:-1])
        docbin = DocBin().from_disk(f)
        docs = list(docbin.get_docs(nlp.vocab))
        for doc in docs:
            doc.spans[span_key] = list(doc.ents)
            type_ = doc.ents[0].label_
            y_labels.extend([type_] * len(list(doc.ents)))
        class_weights_e = compute_class_weight('balanced', classes=np.unique(y_labels), y=np.array(y_labels))
        class_weights[span_key] = dict(zip(np.unique(y_labels).tolist(), class_weights_e.tolist()))
        DocBin(docs=docs).to_disk(f)
    with open(str(Path(loc).parent) + '/class_weights.json', 'w', encoding='utf-8') as f:
        json.dump(class_weights, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    typer.run(main)
