#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 11:39:10 2021

@author: maudmeijer
"""
import math
import numpy as np
import matplotlib.pyplot as plt
import random

def convert_hand(handplayer,dealer_card):
    hand_0 = list(range(len(handplayer)))
    dealer_card_0 = 0
    for n, i in enumerate(handplayer):
        if i == "A":
            hand_0[n]=1
        elif i=="J" or i=="Q" or i=="K":
            hand_0[n]=10
        else:
            hand_0[n]=int(handplayer[n])
    if dealer_card == "A":
        dealer_card_0=1
    if dealer_card=="J" or dealer_card=="Q" or dealer_card=="K":
        dealer_card_0=10
    return hand_0, int(dealer_card_0)


def strategy(hand, dealer_card):
    hard_count=sum(hand)
    cards=len(hand)
    aces_count= 1*(1 in hand)
    soft_count=hard_count
    good_cards=[1,7,8,9,10]
    
    if cards<2:
        return 'Not enough cards'
    
    if hard_count<=11:
        soft_count= hard_count + 10*aces_count
        
    # black jack    
    if cards==2 and soft_count==21:
        return 0
    
    
    if soft_count>=19:
        return 0
    
    
    if hard_count>=17 :
       # print("in hard_count>=17",hand)
        return 0

    
    if cards>2:
        if hard_count==soft_count:
            if hard_count<=11:
                return 1

            if hard_count==12 and dealer_card <=3:
                return 1

            if dealer_card in good_cards:
                return 1

            return 0
        
        
        if soft_count<=17:
            return 1
        
        if soft_count==18 and dealer_card in [1,9,10]:
            return 1
        
        
        
        return 0
    
            
        
    
    if cards==2:
        # geen split; geen dubbel
            
        if hard_count==soft_count:
            
            if hard_count<=11:
                return 1

            if hard_count==12 and dealer_card <=3:
                return 1

            if dealer_card in good_cards:
                return 1

            return 0
            
        
        if hard_count!=soft_count:
            

                
            if soft_count==18:
                
                if dealer_card in [2,7,8]:
                    return 0
            
            return 1

def play():
    w=0
    #eerst een lijst van 2*52 kaarten maken
    deck = []
    #eerst de getallen nul t/m 10 8x voor laten komen
    for i in range(2,11):
        for j in range(0,8):
            deck.append(i)
    
    #nu 8maal een J, Q, K, en A
    for i in ['J','Q','K','A']:
        for j in range(0,8):
            deck.append(i)
    
    #trek twee kaarten voor de speler en voor de Ai
    handplayer = random.sample(deck,2)
    #nu moeten deze kaarten uit het dek verwijderd worden
    for card in handplayer:
        deck.pop(deck.index(card))
    #nu twee kaarten voor de AI:
    handAI = random.sample(deck,2)
    for card in handAI:
        deck.pop(deck.index(card))
    
    
    #bereken de som van de hand
    def som(hand):
        som1=0
        som2=0
        for card in hand:
            if isinstance(card,int):
                som1 = som1+card
                som2 = som2+card
            if card == 'J' or card == 'K' or card == 'Q':
                som1 = som1 + 10
                som2 = som2 + 10
            if card == 'A': 
                som1=som1+1
                som2=som2+11
        somlist = [som1,som2]
        return somlist
            
    #print het deck van de player
    #simuleer het trekken van een kaart
    
    
    
    playerstuk=0
    Q=1
    while Q>0:
        #print ("Jouw hand bevat", handplayer, "een totaal van", som(handplayer))
        #print ("Jouw tegenspeler heeft een", handAI[1],'...')
        #Q=int(input("ga je door of ga je stoppen (een 0 is stoppen, een 1 is door)"))
        #Q=random.randint(0, 1)
        #Q wordt bepaald door de strategie functie. Eerst de hand en dealer card omzetten
        hand_1, dealer_card = convert_hand(handplayer,handAI[1])
        #print(hand_1, dealer_card)
        
        Q=strategy(hand_1, dealer_card)
        #print("Q=",Q)
        if Q==1:
            #trek een nieuwe kaart 
            newcard = random.sample(deck,1)
            for card in newcard:
                handplayer.append(card)
                deck.pop(deck.index(card))
        somplayer = som(handplayer)
        if min(somplayer)>21:
            #print( "helaas, je bent stuk!, je hand was", handplayer, "met een som van", somplayer)
            Q=0
            playerstuk=1
            break
    
    #nu simuleren van de AI:
    #De AI blijft kaarten trekken tot er minimaal 16 getrokken is
    P=1
    AIstuk=0
    while P>0:
        #print ("jouw hand bevat", handplayer,"een totaal van", som(handplayer))
        #print ("de tegenspeler heeft", handAI,"een totaal van", som(handAI))
        
        if min(som(handAI))>15 and min(som(handAI))<22:
            #trek geen nieuwe kart
            P=0
            break
        if max(som(handAI))>15 and max(som(handAI))<22:
            P=0
            break
        
        if P==1: #trek een nieuwe kaart
            newcard = random.sample(deck,1)
            for card in newcard:
                handAI.append(card)
                deck.pop(deck.index(card))
     
        if min(som(handAI))>21:
            #print ("de AI heeft verloren met deze hand:", handAI, "met waarde", som(handAI))
            AIstuk = 1
            P=0
            break
    

            
    #en wie heeft er gewonnen?
    #print("AIstuk = ", AIstuk, "playerstuk", playerstuk)
    if playerstuk==1:
        "Jij bent stuk gegaan, de AI heeft sowieso gewonnen"
        w=0
    if AIstuk==1 and playerstuk==0:
        "De AI is stuk, jij hebt gewonnen, yoehoe!"
        w=2
    if AIstuk==0 and playerstuk==0: #nu wordt het lastig
        #zoek eerst uit welke onderdeel van 'som' het dichtst bij 21 zit
        if max(som(handAI))<22:
            AIscore = max(som(handAI))
        else:
            AIscore = min(som(handAI))
        if max(som(handplayer))<22:
            playerscore = max(som(handplayer))
        else: 
            playerscore= min(som(handplayer))
        #print ("jouw score is", playerscore)
        #print ("AI score is", AIscore)
        if playerscore > AIscore:
            #print ("JIJ WINT")
            w=2
        if playerscore == AIscore:
            #print ("gelijkspel :-o")
            w=1
        if playerscore < AIscore:
            #print ("De AI heeft gewonnen, loser!")
            w=0
    
    #print ("bedankt voor het spelen")
    
    #geef resultaat terug als 0 (verlies), 1 (gelijk), 2 (winst)
    return w

win=0
push=0
loss=0

for i in range(1000000):
    result=play()
    if result==0:
        loss=loss+1
    elif result==1:
         push=push+1
    else:
         win=win+1

print("# loss:",loss)
print("# push:",push)
print("# win:",win)

#print("end simulation")
        

    