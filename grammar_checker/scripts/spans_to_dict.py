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
    nlp = spacy.blank(lang)
    class_weights = dict()
    labels_list = []
    for subset in ['train', 'dev']:
        fetched_files = list(Path(loc).rglob(f'{subset}.*.spacy'))
        all_subset_docs= []
        for f in tqdm(fetched_files):
            y_labels = []
            span_key = "_".join(f.stem.split("_")[:-1])
            if subset == 'train':
                labels_list.append(span_key)
            docbin = DocBin().from_disk(f)
            docs = list(docbin.get_docs(nlp.vocab))[:100]# TODO: use all docs in final v
            for doc in docs:
                ents = list(doc.ents)
                spans = []
                for ent in ents:
                    span = doc.char_span(ent.start, ent.end, label=span_key)
                    spans.append(span)
                doc.spans["sc"] = spans
                type_ = doc.ents[0].label_
                y_labels.extend([type_] * len(list(doc.ents)))
            class_weights_e = compute_class_weight('balanced', classes=np.unique(y_labels), y=np.array(y_labels))
            class_weights[span_key] = dict(zip(np.unique(y_labels).tolist(), class_weights_e.tolist()))
            all_subset_docs.extend(docs)
        subset_filename=f'{subset}.spacy'
        DocBin(docs=all_subset_docs).to_disk(Path(loc) / subset_filename)
    with open(str(Path(loc).parent) + '/class_weights.json', 'w', encoding='utf-8') as f:
        json.dump(class_weights, f, ensure_ascii=False, indent=4)
    with open(str(Path(loc).parent) + '/spancat.json', 'w') as json_file:
        json.dump(labels_list, json_file, indent=2)

if __name__ == "__main__":
    typer.run(main)
