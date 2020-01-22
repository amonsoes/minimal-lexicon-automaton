import pickle
import os
import graphviz
from auto_state import State

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
