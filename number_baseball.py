# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 22:04:22 2023

@author: replica
"""

from math import log2
from itertools import permutations
from random import sample

def list_to_text(list_):
    return ''.join(list(map(str,list_)))

class Baseball:
    def __init__(self, numbers, length):
        self.numbers = numbers
        self.length = length
        
    def get_nsmb(self, candidate, guess):
        m = 0
        for i in candidate:
            if i in guess:
                m += 1  
        n = 0
        for j in range(self.length):
            if candidate[j] == guess[j]:
                n += 1
        m = m-n
        return '%ds%db'%(n, m)
    
    def grouping(self, candidates, guess):
        group = {}
        for candidate in candidates:
            nsmb = self.get_nsmb(candidate, guess)
            try: 
                group[nsmb].append(candidate)
            except:
                group[nsmb] = [candidate]
        return group
    
    #@jit
    def get_entropy(self, candidates, guess):
        num = len(candidates) # number of candidates
        group = self.grouping(candidates, guess)
        entropy = 0
        for i in group.values():
            p = len(i)/num
            entropy -= p*log2(p)
        return entropy, group
    
    def get_guess(self, candidates):
        max_entropy = -1
        for candidate in candidates:
            entropy, group = self.get_entropy(candidates, candidate)
            if entropy > max_entropy:
                max_entropy = entropy
                guess = candidate
                guess_group = group
        return guess, guess_group, max_entropy
    
    def get_sorted_lists(self, candidates):
        lists = [] 
        for candidate in candidates:
            entropy, group = self.get_entropy(candidates, candidate)
            group = dict(sorted(group.items(), key=lambda group: len(group[1]), reverse=True))
            lists.append([candidate, group, entropy])
        lists = sorted(lists, key=lambda lists: lists[2], reverse=True)
        return lists

if __name__ == '__main__':
    # 숫자야구에 사용될 숫자들
    numbers = list(range(0,10))
    
    # 숫자야구할때 숫자의 길이
    length = 2
    
    bb = Baseball(numbers, length)   
    
    # 후보군 생성
    candidates = list(permutations(numbers, length))
    candidates = list(map(list_to_text,candidates))
    
    # 컴퓨터의 정답생성
    com_ans = list_to_text(sample(numbers, length))
    
    # 첫번째 추측
    guess = list_to_text(sample(numbers, length))
    print('Computer guess: ' + guess)
    
    # 추측에 따른 후보 그룹
    group = bb.grouping(candidates, guess)
        
    while True:
        nsmb = input('>> ')
        if nsmb == '%ds0b'%(length):
            print('YOU LOSE!')
            break
        try:
            candidates = group[nsmb]
        except:
            print('Contradiction!')
            break
        player_guess = input('Your guess: ')
        if player_guess == com_ans:
            print('YOU WIN!')
            break
        print('>> ' + bb.get_nsmb(com_ans, player_guess))
        
        guess, group, entropy = bb.get_guess(candidates)
        print("Computer's guess: " + guess, entropy)