"""Modul who contain the program class"""
import pygame
from pygame.locals import *
from random import randrange


import constants as c


class Level:
    """Class to create a level"""

    def __init__(self, myFile):
        self.myFile = myFile
        self.myMape = 0

    def generate(self):
        """Method to generate a level
        according to a file"""

        #open the file
        with open(self.myFile, 'r') as myFile:
            mapLevel = []  # structure of the labyrinth
            #read trought the file lines
            for line in myFile:
                lineLevel = []  # hold on the file lines
                for char in line:
                    if char is not '\n':  # not EOF
                        lineLevel.append(char)
                mapLevel.append(lineLevel)
            self.myMape = mapLevel  # save the generated level

    def show(self, robot, windows):
        """Method who permit to print the level
        according to the maze structure
        parssed in arguments"""

        #loading the pictures
        wall = pygame.image.load(c.wallPicture).convert()
        guardian = pygame.image.load(c.guardPicture).convert()
        syringue = pygame.image.load(c.syringuePicture).convert()
        needle = pygame.image.load(c.needlePicture).convert()
        ether = pygame.image.load(c.etherPicture).convert()

        #print each case of the maze line
        numLine = 0
        for line in robot.level.myMape:
            numCase = 0
            for sprite in line:
                #calculate the real position in pixel
                x = numCase * c.spriteSize
                y = numLine * c.spriteSize
                if sprite is '#':  # wall = '#'
                    windows.blit(wall, (x, y))
                elif sprite is 'R':  # hero
                    windows.blit(robot.character, (x, y))
                elif sprite is 'G':  # the guardian
                    windows.blit(guardian, (x, y))
                elif sprite is 'S':  # syringue tube
                    windows.blit(syringue, (x, y))
                elif sprite is 'N':  # needle
                    windows.blit(needle, (x, y))
                elif sprite is 'E':  # ether
                    windows.blit(ether, (x, y))
                numCase += 1
            numLine += 1


class Bot:
    """Class who permit to create a character"""

    def __init__(self, character, level):
        self.x = 0  # position in case
        self.y = 0
        self.pix = 0  # position in pixel
        self.piy = 0
        self.level = level  # character level
        self.character = pygame.image.load(character).convert_alpha()
        self.bag = []  # bag to pick up utilities

    def move(self, sens, tabUtilities):
        """Method what permit to
        move a character"""

        #moving rigth
        if sens == 'droite':
            #verifies not to exceed the maze limit
            if self.x < (c.nbSideCase - 1):
                #verifies if the destination case
                #is'nt a wall
                if self.level.myMape[self.y][self.x + 1] is not '#':
                    #if an utility is found, we pick it of
                    for utility in tabUtilities:
                        if self.level.myMape[self.y][self.x + 1]\
                           == utility.name:
                            self.pickUp(utility)
                            self.bag.append(utility.name)
                    #next case
                    self.x += 1
                    #calculate the real position in pixel
                    self.pix = self.x * c.spriteSize
                    #the box where the character is replaced by a
                    #letter representing a passage, here 0
                    self.level.myMape[self.y][self.x - 1] = '0'
                    #the box where the character is located is replaced by
                    #the image of the character, here R
                    self.level.myMape[self.y][self.x] = 'R'

        #moving left
        if sens == 'gauche':
            if self.x > 0:
                if self.level.myMape[self.y][self.x - 1] is not '#':
                    #if an utility is found, we pick it of
                    for utility in tabUtilities:
                        if self.level.myMape[self.y][self.x - 1]\
                           == utility.name:
                            self.pickUp(utility)
                            self.bag.append(utility.name)
                    #update the differents cases characters
                    self.x -= 1
                    self.pix = self.x * c.spriteSize
                    self.level.myMape[self.y][self.x + 1] = '0'
                    self.level.myMape[self.y][self.x] = 'R'

        #moving up
        if sens == 'haut':
            if self.y > 0:
                if self.level.myMape[self.y - 1][self.x] is not '#':
                    #if an utility is found, we pick it of
                    for utility in tabUtilities:
                        if self.level.myMape[self.y - 1][self.x]\
                           == utility.name:
                            self.pickUp(utility)
                            self.bag.append(utility.name)
                    #update the differents cases characters
                    self.y -= 1
                    self.piy = self.y * c.spriteSize
                    self.level.myMape[self.y + 1][self.x] = '0'
                    self.level.myMape[self.y][self.x] = 'R'

        #moving down
        if sens == 'bas':
            if self.y < (c.nbSideCase - 1):
                if self.level.myMape[self.y + 1][self.x] is not '#':
                    #if an utility is found, we pick it of
                    for utility in tabUtilities:
                        if self.level.myMape[self.y + 1][self.x]\
                           == utility.name:
                            self.pickUp(utility)
                            self.bag.append(utility.name)
                    #update the differents cases characters
                    self.y += 1
                    self.piy = self.y * c.spriteSize
                    self.level.myMape[self.y - 1][self.x] = '0'
                    self.level.myMape[self.y][self.x] = 'R'

    def pickUp(self, utility):
        """Method to pickUp an Utility object"""

        #compare the positions of Utility and the character
        if (self.y, self.x) == (utility.y, utility.x):
            #update the object state
            utility.isPicked(True)

    def listUtility(self, windows):
        """Method who display the number of utilities remaining"""
        remainUtility = c.nbUtilities - len(self.bag)
        #the message to show
        message = "{} utility(ies) found; {} remaining".\
            format(len(self.bag), remainUtility)
        messageFont = pygame.font.Font(None, 20)
        messageText = messageFont.render(message, 1, (85, 255, 255))
        #insert the message in the pygame windows
        windows.blit(messageText, (250, 6))


class Utility:
    """Class to create some utilities"""

    def __init__(self, name, level):
        self.x = 0  # position in case
        self.y = 0
        self.pix = 0  # position in pixel
        self.piy = 0
        self.name = name  # a character that represent the object
        self.level = level
        #put the utility randomly
        self.putRandomly()

    def putRandomly(self):
        """Method for randomly inserting an object
        into the labyrinth"""

        self.x, self.y = randrange(c.nbSideCase), randrange(c.nbSideCase)
        #if we are not on an empty space, here 0
        while(self.level.myMape[self.y][self.x] is not '0'):
            self.x, self.y = randrange(c.nbSideCase), randrange(c.nbSideCase)
        #if we find an adequate place
        self.level.myMape[self.x][self.y] = self.name  # insert it
        #save the position in pixel
        self.pix, self.piy = self.x * c.spriteSize, self.y * c.spriteSize

    def isPicked(self, reponse):
        """Method who check if the object has been
        picked up"""

        if reponse:
            #turn the object character on a passage, here 0
            self.name = '0'
