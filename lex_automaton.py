import pickle
import os
import graphviz

from collections import OrderedDict

def renumber_states(ls):
    ls = sorted(ls, key= lambda x: x.num)
    for e, state in enumerate(ls[:-1]):
        highest = state.num
        if ls[e+1].num != highest + 1:
            ls[e+1].num = highest + 1
        

class LexAutomaton:
    
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.Q = []
        self.delta = {}
        self.s = State(False, self)
        self.F = set()
        self.register = []
        self.daciuk()
        
    def common_prefix(self, word):
        current_state = self.s
        for e, char in enumerate(word):
            if (current_state, char) in self.delta.keys():
                current_state = self.delta[current_state, char]
            else:
                return (current_state, e)
        return current_state # add method to finalize at a given point
    
    def add_suffix(self, suffix, last_state):
        for e, char in enumerate(suffix):
            
            is_final = True if e == len(suffix)-1 else False
            new_state = State(is_final, self)
            last_state.add_transition(char, new_state)
            self.delta[(last_state, char)] = new_state
            last_state = new_state
    
    def daciuk(self):
        for word in self.lexicon:
            last_state, suff_index = self.common_prefix(word)
            suffix = word[suff_index:]
            if last_state.has_children():
                self.replace_or_register(last_state)   #replace or register
            self.add_suffix(suffix,last_state)
            
        self.replace_or_register(self.s)
        renumber_states(self.Q)
        del self.delta
        print("lexicon added")
        
    def replace_or_register(self,state):
        found = False
        label, child = state.get_last_child()
        if child.has_children():
            self.replace_or_register(child)
        for i in self.register:
            if i.ids() == child.ids():
                found = True
                state.remove_transition(label)
                state.add_transition(label, i)
        if found:
            self.Q.remove(child)
            del child
        else:
            child.move_to_register(self)
    
    def to_file(self):
        path = "./lexautomaton"
        while os.path.exists(path):
            counter = 1
            path += str(counter)
            counter += 1
        with open(path, "wb") as b:
            pickle.dump(self, b)
        return path
    
    @classmethod
    def from_file(cls, path):
        with open(path, "rb") as b:
            automaton = pickle.load(b)
        return automaton
    
    def traverse(self, word):
        current = self.s
        is_in_lex = False
        while not is_in_lex:
            char = word[0]
            if len(word) == 1:
                if current.traverse(char) in self.F:
                    is_in_lex = True
                    return True
                else:
                    return False
            target = current.traverse(char)
            if target != None:
                word = word[1:]
                current = target
            else:
                return False


    def return_lexicon(self, original, prefix="", ls = []):
        current = original
        word = prefix
        copy_knot = [i for i in current.transitions.keys()]
        for char in copy_knot:
            while current not in self.F:
                word += char
                next = current.transitions[char]
                current = next
                if len(current.transitions.keys()) > 1:
                    self.return_lexicon(current, word, ls)
                    word = False # deal with erroneous last recursion step
                    break                
                elif current.transitions.keys():
                    char = [i for i in current.transitions.keys()][0]
                else:
                    continue
            if word:
                ls.append(word)
            current = original
            word = prefix
        return ls 
         
    
    def draw_automaton(self):
        
        g = graphviz.Digraph("Automaton")
        
        for state in self.Q:
            if state in self.F:
                g.attr("node", style="bold")
            if state == self.s:
                g.node(str(state.num), label="-> " + str(state.num))
            else:
                g.node(str(state.num))
            g.attr('node',style='solid')
            
        ls = []
        for i in self.Q:
            for key, value in i.transitions.items():
                ls.append((i,key,value))
        
        for x,label,y in ls:
            g.edge(str(x.num),str(y.num),label=" " + label+ " ")
        
        return g
            
                
        

class State:
    
    next_id = 0
    
    def __init__(self, is_final, automaton):
        self.is_final = is_final
        if is_final:
            automaton.F.add(self)
        self.num = State.next_id
        self.is_in_register = False
        if self.is_in_register:
            self.move_to_register()
        self.transitions = OrderedDict()  
        State.next_id += 1  
        automaton.Q.append(self)

    def __str__(self):
        return str(self.num)

    
    def ids(self):
        n_f = "F" if self.is_final else "N"
        trans = "".join([label + str(target.num) for label, target in self.transitions.items()])
        return n_f + trans
    
    def traverse(self, char):
        if char in self.transitions.keys():
            return self.transitions[char]
        else:
            return None

    def add_transition(self,label,target_state):
        self.transitions[label] = target_state
        
    def remove_transition(self,label):
        del self.transitions[label]
        
    def has_children(self):
        if len(self.transitions):
        
            return True if len(self.transitions) else False

    def get_last_child(self):
        if self.transitions.items():
            return [i for i in self.transitions.items()][-1]

    def move_to_register(self,automaton):
        self.is_in_register = True
        automaton.register.append(self)


if __name__ == "__main__":
    
    user_input = input("Do you want load the automaton from a word list or from a file? w = from word list, f = from file")
    if user_input == "f":
        path = input("Enter path:")
        try:
            automaton = LexAutomaton.from_file(path)
        except:
            raise FileNotFoundError 
    elif user_input == "w":
        words = input("Paste Words:")
        list = words.split(" ")
        print(list)
        automaton = LexAutomaton(list)
    run = True
    while run:
        main_menu = input("What do you want to do? [1] traverse for word [2] draw automaton [3] return lexicon [4] exit")
        if main_menu == "1":
            word = input("Enter word: ")
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