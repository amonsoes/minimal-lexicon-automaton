# minimal-lexicon-automaton

This alogrithm creates a minimal lexicon automaton, which efficiently stores a lexicon and reduces time complexity of a lexicon look up. It is based on the algorithm by Daciuk, as proposed in this paper:
https://www.aclweb.org/anthology/J00-1002.pdf.

The program runs through the terminal. There are no additional arguments for running the program as of this moment.


## running the program ##

Upon running, you will be asked wether you want to load the automaton from a file or initialize the automaton
with a space-separated word list.

## the main menu ##

Here you can choose some of the available operations by user input:. You can:

- check if a word is in the lexicon [1]
- draw the loaded/initialized automaton [2]
- return the entire lexicon [3]
- exit the program [4]

## exit ##

upon quitting, you will be asked wether you want to serialize and store your automaton. If so,
the program gives the automaton the name "lexautomaton" and checks for name-collision.


