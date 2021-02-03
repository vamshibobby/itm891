# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 22:23:16 2021

@author: SAI VAMSHI
"""

#Changing the path - only use it when codeing in standalone Jupyter or Spyder
import os
os.chdir("C:/Users/SAI VAMSHI/Desktop/MSU MSBA/CSE801A/itm891/exercises/04")

#Importing the PointyGame module
import PointyGame.pointy_game as PointyGame
from PointyGame.strategy import *
from PointyGame.creature import Creature
import pandas as pd

#Initializing the creature
creature = Creature(1000, (9,9), (4,4), init_facing='N')
game = PointyGame.Game((9,9), creature)
#Creating a dictionary to save the data at end of each step
ex4_dict = {}
#Looping the three functions, 30 replicates and 100 steps
for func in [play_greedily,play_randomly,play_greedy_with_random]:
    for i in range(1,31):
        creature = Creature(1000, (9,9), (4,4), init_facing='N')
        game = PointyGame.Game((9,9), creature)
        for j in range(1,101):
            #Playing one step of the game
            game.play(func)
            #If the creature is dead, stop the loop
            if creature.score > 0:
                #Save the data as a dataframe and add it to the dictionary using unique key
                ex4_dict[str(func).split(" ")[1] + " " + str(i) +" "+ str(j)] = pd.DataFrame([[str(func).split(" ")[1],
                                      i,
                                      j,
                                      creature.current_location[0],
                                      creature.current_location[1],
                                      creature.score,
                                      game.last_move,
                                      num_rewards_remaining(game.points_matrix())]],
                                      columns = ["Treatment_Function","Replicate_Num",
                                                 "Step_Num","X_Location","Y_Location",
                                                 "Score","Last_Move","Rewards_rem"])
            else:
                break

#Concatenating the dictionaries inside dictionary and writing into csv file        
pd.concat(ex4_dict).sort_values(["Treatment_Function","Replicate_Num","Step_Num"]).to_csv("ex4b_output.csv",index=False)
