#!/bin/bash

# rm $1.tex
python $1.py 

rm $1.pdf
pdflatex $1.tex
rm *.aux *.log *.vscodeLog
rm *.tex

if [[ "$OSTYPE" == "darwin"* ]]; then
    open $1.pdf
else
    xdg-open $1.pdf
fi
