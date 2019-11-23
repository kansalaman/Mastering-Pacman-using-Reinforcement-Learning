import pygame
from pygame.locals import * 
from random import randint
from classes import *
import simulate

if __name__ == "__main__" or __name__ == "pacman" :

    GAME = Maze()
    HERO = Pacman()
    VILLIAN = Ghost()

    pygame.init()
    GAME.scorefont = pygame.font.Font(None,30)
    done = False
    clock = pygame.time.Clock()

    while done == False:
        x = simulate.nextIteration()
        if x == -1:
            break      
        HERO.pacPosition(GAME)
        GAME.scoredisp()            
        GAME.screen.fill(GAME.BLACK)
        VILLIAN.ghostPosition(GAME)
          

        GAME.countfinal=0
        GAME.dispmaze()
        GAME.drawwalls() 
        HERO.pos(GAME)
        VILLIAN.pos(GAME)

        clock.tick(5)
        pygame.display.flip()
    pygame.quit()   
