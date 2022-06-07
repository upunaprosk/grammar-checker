import typer
from custom_factories import *


def main(loc_output: Path):
    """
    Assemble SpanCategorizer pipelines
    """
    nlp = spacy.blank("en")
    nlp.add_pipe("punctuation", last=True)
    nlp.add_pipe("spelling", last=True)
    nlp.add_pipe("articles", last=True)
    nlp.add_pipe("grammar_major", last=True)
    nlp.add_pipe("grammar_minor", last=True)
    nlp.add_pipe("vocabulary", last=True)
    nlp.to_disk(loc_output)
    return


if __name__ == "__main__":
    typer.run(main)
