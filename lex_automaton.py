import pickle
import os
import argparse

from collections import OrderedDict

"""
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--from_file", help="choose wether to load automaton from file or not", type=dir_path)
args = parser.parse_args()

if args.f:
    auto = LexAutomaton.from_file("./lexautomaton")
    print("automaton loaded")
"""


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
                    print("word is in lex")
                    return None
                else:
                    print("word is not in lex")
                    return None
            target = current.traverse(char)
            if target != None:
                word = word[1:]
                current = target
            else:
                print("word is not in lex")
                return None
                
        

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

words = ["acker","alle","alraune","as","aspekt","bahn","weltraum","zaun", "zombie"]

auto = LexAutomaton(words)
print([i.num for i in auto.Q])
auto.traverse("ack")   

