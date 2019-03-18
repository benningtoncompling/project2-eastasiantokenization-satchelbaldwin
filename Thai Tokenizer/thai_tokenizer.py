#!/usr/bin/env python3

import sys


v1 = ['เ','แ','โ','ใ','ไ']
c1 = ['ก', 'ข', 'ฃ', 'ค', 'ฅ', 'ฆ', 'ง', 'จ', 'ฉ', 'ช', 'ซ', 'ฌ', 'ญ', 'ฎ', 'ฏ', 'ฐ', 'ฑ', 'ฒ', 'ณ', 'ด', 'ต', 'ถ', 'ท', 'ธ', 'น', 'บ', 'ป', 'ผ', 'ฝ', 'พ', 'ฟ', 'ภ', 'ม', 'ย', 'ร', 'ฤ', 'ล', 'ฦ', 'ว', 'ศ', 'ษ', 'ส', 'ห', 'ฬ', 'อ', 'ฮ']
c2 = ['ร', 'ล', 'ว', 'น', 'ม']
v2 = ['\u0E31', '\u0E34', '\u0E35', '\u0E36', '\u0E37', '\u0E38', '\u0E39', '\u0E47']
t = ['\u0E48', '\u0E49', '\u0E4A', '\u0E4B']
v3 = ['า', 'อ', 'ย', 'ว']
c3 = ['ง', 'น', 'ม', 'ด', 'บ', 'ก', 'ย', 'ว']

class T:
    def __init__(self, n, c, t, s = False):
        self.name = n
        self.condition = c
        self.to = t
        self.space = s

class StateMachine:
    def __init__(self, c, cs, a, t):
        self.categories = c
        self.current_state = cs
        self.accumulator = a
        self.transitions = t
    def run(self, text):
        for char in text:
            print("character: " + char)
            self.step(char)
        return self.accumulator
    def step(self, char, retry = False):
        char_category = ""
        category_fallbacks = []
        for k, v in self.categories.items():
            if char in v:
                print('category m: {}'.format(k))
                char_category = k
                category_fallbacks.append(k)
        if retry:
            char_category = category_fallbacks[0]
        print("\tcategory: " + char_category)
        valid_starting = []
        for t in transitions:
            if t.name == self.current_state:
                valid_starting.append(t)
        if len(valid_starting) == 0:
            self.step(char, True)
        for t in valid_starting:
            if len(self.accumulator) != 0:
                if self.accumulator[-1] == ' ':
                    for possible_category in category_fallbacks:
                        if possible_category[-1] == '1':
                            print("CATEGORY:" + possible_category)
                            char_category = possible_category
            if t.condition == "*":
                print("\t\tepsilon transition: {} -> {}, restepping".format(t.name, t.to))
                self.current_state = t.to 
                if (t.name == "q9"):
                    print("\t\t\tq9: re-stepping with space")
                    self.accumulator = self.accumulator + " "
                    self.step(char)
                else:
                    self.step(char)
                    # self.step(char)
            elif t.condition == char_category:
                self.transition(char, t)
    def transition(self, char, t):
        print("\taccumulator: {} \n\t\ttransition: {} -> {} ({} : {})".format(self.accumulator, t.name, t.to, char, t.condition))
        if t.space:
            print("\t\tadding space after.")
            self.accumulator = self.accumulator + " "
        self.accumulator = self.accumulator + char
        self.current_state = t.to
    def reset(self):
        self.current_state = "q0"
        self.accumulator = ""


categories = {
        "v1":v1
    ,   "c1":c1
    ,   "c2":c2
    ,   "v2":v2
    ,   "t":t
    ,   "v3":v3
    ,   "c3":c3
    }
transitions = [   
        # FROM  COND   TO   SPACE
        T("q0", "v1", "q1")
    ,   T("q0", "c1", "q2")
    ,   T("q1", "c1", "q2")
    ,   T("q2", "v1", "q7", True)
    ,   T("q2", "c1", "q8", True)
    ,   T("q2", "c2", "q3")
    ,   T("q2", "v2", "q4")
    ,   T("q2", "t",  "q5")
    ,   T("q2", "v3", "q6")
    ,   T("q2", "c3", "q9")
    ,   T("q3", "v2", "q4")
    ,   T("q3", "t",  "q5")
    ,   T("q3", "v3", "q6")
    ,   T("q3", "c3", "q9")
    ,   T("q4", "v1", "q7", True)
    ,   T("q4", "c1", "q8", True)
    ,   T("q4", "t",  "q5")
    ,   T("q4", "v3", "q6")
    ,   T("q4", "c3", "q9")
    ,   T("q5", "v1", "q7", True) 
    ,   T("q5", "c1", "q8", True)
    ,   T("q5", "v3", "q6")
    ,   T("q5", "c3", "q9")
    ,   T("q6", "v1", "q7", True) 
    ,   T("q6", "c1", "q8", True)
    ,   T("q6", "c3", "q9")
    ,   T("q7", "*",  "q1")
    ,   T("q8", "*",  "q2")
    ,   T("q9", "*",  "q0", True)
    ]

sm = StateMachine(categories, "q0", "", transitions)

def tokenize(line):
        sm.reset()
        return sm.run(line) + "\n"

in_file = sys.argv[1]
out_file = sys.argv[2]

with open(in_file, 'r') as open_in:
	with open(out_file, 'w') as open_out:
		for line in open_in.readlines():
			spaced_line = tokenize(line)
			open_out.write(spaced_line)
