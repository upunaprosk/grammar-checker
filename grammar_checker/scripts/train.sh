mkdir ./training
python -m spacy train configs/config.cfg --output ./training/ --paths.train ./realec/train.spacy --paths.dev ./realec/dev.spacy --gpu-id 0