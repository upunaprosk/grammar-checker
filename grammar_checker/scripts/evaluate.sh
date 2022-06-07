for i in "$@"
do
    python -m spacy evaluate ./training/"$i"/model-best ./realec/"$i"_dev.spacy --output ./metrics/"$i".json --gpu-id 0
done
