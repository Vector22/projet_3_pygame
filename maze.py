#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""
Game or McGyver must escape from a labyrinth after
have pick up objects that will allow him to fall asleep
the guard and to flee

files used
classes.py, maze.py, maps/level1.txt, maps/level2.txt
"""
import pygame
from pygame.locals import *
import pygame.image as pim

from classes import Bot
from classes import Level
from classes import Utility
import constants as c

pygame.init()

#opening the pygame windows
windows = pygame.display.set_mode((c.windowsSide, c.windowsSide))
#the icon
icon = pim.load(c.iconPicture)
pygame.display.set_icon(icon)
#title
pygame.display.set_caption(c.windowsTitle)
#background end color
endColor = (100, 100, 0)
#font to writte if victory or defeat
victoryFont = pygame.font.Font(None, 40)
victoryText = victoryFont.render("Victory! You escaped.", 1, (255, 255, 255))
defeatFont = pygame.font.Font(None, 40)
defeatText = defeatFont.render("You're dead, party lost.", 1, (255, 0, 0))
#font to writte in the menu screen
font = pygame.font.Font(None, 50)
text = font.render("Choose a level", 1, (0, 0, 200))
font1 = pygame.font.Font(None, 50)
text1 = font1.render("1: Easy", 1, (0, 200, 0))
font2 = pygame.font.Font(None, 50)
text2 = font2.render("2: Difficult", 1, (0, 200, 0))

#main loop
loop = True
pygame.key.set_repeat(50, 50)
while loop:
    #print the menu screen
    windows.blit(text, (110, 80))
    windows.blit(text1, (150, 150))
    windows.blit(text2, (150, 220))
    #refresh the screen
    pygame.display.flip()

    repeatMenu = True  # loop variables
    repeatGame = True

    while repeatMenu:
        #limit the loop speed
        pygame.time.Clock().tick(20)

        for event in pygame.event.get():
            #If the user leaves, we put the loop variables
            #at false to not browse any and close
            if event.type == QUIT or event.type == KEYDOWN\
               and event.key == K_ESCAPE:
                loop = False
                repeatMenu = False
                repeatGame = False

                #the player level choice
                choice = 0
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    repeatMenu = False  # quit the menu
                    choice = 'maps/level1.txt'  # define the level to load
                elif event.key == K_2:
                    repeatMenu = False
                    choice = 'maps/level2.txt'

    #we check that the player has made a level choice
    #to not load if he leaves
    if choice is not 0:
        #load the background image
        background = pim.load(c.bgPicture).convert()
        #define the door position
        door = (14, 14)

        #generate the level
        level = Level(choice)
        level.generate()
        #create the utilities objects
        #and append them to a table
        tabUtilities = []
        tabUtilities.append(Utility('S', level))
        tabUtilities.append(Utility('E', level))
        tabUtilities.append(Utility('N', level))
        #create the character
        bot = Bot(c.heroPicture, level)
        #print the labyrinth
        level.show(bot, windows)

    #game loop
    while repeatGame:
        #limit the clock speed
        pygame.time.Clock().tick(20)

        for even in pygame.event.get():

            #If the user leaves, we put the variable
            #that continues the game AND the general variable
            #to false to close the window
            if even.type == QUIT:
                repeatGame = False
                loop = False
            elif even.type == KEYDOWN:
                #we only return to the menu If the user press Esc
                if even.key == K_ESCAPE:
                    repeatGame = False
            #moving the hero
            elif even.key == K_DOWN:
                bot.move('bas', tabUtilities)

            elif even.key == K_UP:
                bot.move('haut', tabUtilities)

            elif even.key == K_LEFT:
                bot.move('gauche', tabUtilities)

            elif even.key == K_RIGHT:
                bot.move('droite', tabUtilities)

        #print the labyrinth with news positions
        windows.blit(background, (0, 0))
        level.show(bot, windows)
        pygame.display.flip()

        #back up to menu if victory or defeat
        if (bot.y, bot.x) == door and len(bot.bag) == 3:
            windows.fill(endColor)
            windows.blit(victoryText, (75, 300))
            pygame.display.flip()
            repeatGame = False
        if (bot.y, bot.x) == door and len(bot.bag) < 3:
            windows.fill(endColor)
            windows.blit(defeatText, (75, 300))
            pygame.display.flip()
            repeatGame = False
