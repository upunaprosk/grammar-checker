for i in "$@"
do
    cp training/"$i"/model-best/* -r training/"$i"/
    rm -Rfv training/"$i"/model-best
    rm -Rfv training/"$i"/model-last
done