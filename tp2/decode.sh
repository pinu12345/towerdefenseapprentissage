#!/bin/sh
#MOY.sh script par Pierre-Olivier Brosseau (brosseap)

if [ $# -ne 1 ]; then
	echo "Usage : $0 nom-fichier"
	exit 1
fi

if [ ! -f $1 ]; then
	echo "File $1 does not exist."
	exit 1
fi

FILE="translations.txt"
> $FILE
FIRSTLINE="TRUE"
while read line
do
    python gentraducs.py "$line"
    /u/pift6010/bin/64/ngram -lm sms.3g.lm -ppl translations.txt -unk -debug 1 > logprobs.txt
    python parser.py
done < $1


