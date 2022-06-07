from pathlib import Path
import typer
import json
from thinc.api import Config    

def main(loc_config: Path, loc_weights: Path):
    """
    Assign class weights used within the loss function
    """
    basic_config = Config().from_disk(loc_config)
    with open(str(loc_weights) + "/class_weights.json") as f:
        d = json.load(f)
        for group_err, weights in d.items():
            new_weights = {"spans_" + error + "_f": round(weight/sum(weights.values()), 3) for error,weight in weights.items()}
            new_config = basic_config.copy()
            new_config['training']['score_weights'] = new_weights
            new_config['training']['logger']["run_name"] = group_err
            new_config['components']['spancat']["spans_key"] = group_err
            new_config['paths']['train'] = f"./realec/{group_err}_train.spacy"
            new_config['corpora']['train']['path'] = f"./realec/{group_err}_train.spacy"
            new_config['paths']['dev'] = f"./realec/{group_err}_dev.spacy"
            new_config['corpora']['dev']['path'] = f"./realec/{group_err}_dev.spacy"
            new_config.to_disk(f"{loc_config.parent}/config_{group_err}.cfg")

if __name__ == "__main__":
    typer.run(main)