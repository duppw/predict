# predict
Randomly predicting the next word in a sentence.

## What is it?
*predict.py* is just a simple python script that parses words of .epub file and randomically create a text based on it.

## Usage
`-h`: print the help page
`--start-word`: set the phrase with selected word
`--lenght`: set the number of words to create

The script can only read .epub files.
It creates a .csv wordbase with all the matches.

Example: `python3 predict.py "Anna Kariênina (Lev Tolstói).epub" "wordbase.csv" --start-word "eu" --length 50`
