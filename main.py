# main.py
import pygame
import sys
from game import Game

def main():
    # Initialize all imported pygame modules
    pygame.init()
    
    # Create the game instance and run the loop
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
