from lex_automaton import LexAutomaton
from auto_state import State


def run():
    
    user_input = input("\nDo you want load the automaton from a word list or from a file? \n\n\tw = from word list \n\tf = from file\n")
    if user_input == "f":
        path = input("Enter path:")
        try:
            automaton = LexAutomaton.from_file(path)
        except:
            raise FileNotFoundError 
    elif user_input == "w":
        words = input("Paste words, separated by space :")
        list = words.split(" ")
        print(list)
        automaton = LexAutomaton(list)
    run = True
    while run:
        main_menu = input("\nWhat do you want to do? \n\n\t[1] traverse for word \n\t[2] draw automaton \n\t[3] return lexicon \n\t[4] exit\n")
        if main_menu == "1":
            word = input("Enter word: \n")
            check = automaton.traverse(word)
            if check:
                print("word is in lex")
            else:
                print("word is not in lex")
        elif main_menu == "2":
            g = automaton.draw_automaton()
            g.render()
        elif main_menu == "3":
            print(automaton.return_lexicon(automaton.s))
        else:
            run = False
    exit = input("Do you want to save your current automaton? [y/n]")
    if exit == "y":
        path = automaton.to_file()
        print("File was saved here: ", path)
        
if __name__ == "__main__":
    
    run()