for i in "$@"
do
    mkdir ./training/"$i"
    python -m spacy train configs/config_"$i".cfg --output ./training/"$i" --paths.train ./realec/"$i"_train.spacy --paths.dev ./realec/"$i"_dev.spacy --gpu-id 0
done