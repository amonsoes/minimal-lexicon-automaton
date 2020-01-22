from collections import OrderedDict

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