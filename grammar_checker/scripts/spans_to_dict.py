from pathlib import Path
import json
import typer
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
from spacy.tokens import SpanGroup


def main(loc: Path, lang: str):
    """
    Process NER data from the train.spacy file, compute class weights,
    and save labels and class weights for pipeline training with SpanCategorizer.
    """
    nlp = spacy.blank(lang)
    train_file = loc / "train.spacy"
    y_labels = []

    if train_file.exists():
        docbin = DocBin().from_disk(train_file)
        docs = list(docbin.get_docs(nlp.vocab))

        for doc in tqdm(docs):
            for span in doc.spans["error"]:
                y_labels.append(span.label_)

        labels_list = np.unique(y_labels)
        class_weights = dict(
            zip(labels_list, compute_class_weight('balanced', classes=labels_list, y=np.array(y_labels)).tolist())
        )
        labels_list = list(labels_list)

        with open(loc / 'class_weights.json', 'w', encoding='utf-8') as f:
            json.dump(class_weights, f, ensure_ascii=False, indent=4)
        with open(loc / 'spancat.json', 'w', encoding='utf-8') as f:
            json.dump(labels_list, f, indent=2)
        print("Labels and class weights saved successfully.")
    else:
        print(f"File {train_file} not found.")


if __name__ == "__main__":
    typer.run(main)