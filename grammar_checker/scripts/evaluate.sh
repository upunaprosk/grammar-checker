for i in "$@"
do
    python -m spacy benchmark accuracy ./training/"$i"/model-best ./realec/"$i"_dev.spacy --output ./metrics/"$i".json --gpu-id 0
done
