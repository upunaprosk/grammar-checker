from pathlib import Path
import typer
import json
from thinc.api import Config    

def main(loc_config: Path, loc_weights: Path):
    """
    Assign class weights used within the loss function
    """
    basic_config = Config().from_disk(loc_config)
    # with open(str(loc_weights) + "/class_weights.json") as f:
    #     d = json.load(f)
    # new_config['training']['score_weights'] = new_weights TODO: add weighted loss
    new_config = basic_config.copy()
    new_config['training']['logger']["run_name"] = 'test_grammar_checker'
    new_config['initialize']['components']['spancat']["labels"]['path'] = str(loc_weights) + "/spancat.json"
    new_config['paths']['train'] = "./realec/train.spacy"
    new_config['corpora']['train']['path'] = "./realec/train.spacy"
    new_config['paths']['dev'] = f"./realec/dev.spacy"
    new_config['corpora']['dev']['path'] = f"./realec/dev.spacy"
    new_config.to_disk(f"{loc_config.parent}/config.cfg")


if __name__ == "__main__":
    typer.run(main)