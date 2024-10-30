import typer
from custom_factories import *


def main(loc_output: Path):
    """
    Assemble SpanCategorizer pipelines
    """
    nlp = spacy.blank("en")
    nlp.add_pipe("grammar-checker", last=True)
    nlp.to_disk(loc_output)
    return


if __name__ == "__main__":
    typer.run(main)
