import random, os
from random import randint
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

os.system("mode con cols=50 lines=20")  
os.environ['COLS'] = "50"
os.environ['LINES'] = "20"

# ▒ шю
HEIGHT =  20
WIDTH = 50
TIMEOUT = 500

class Game(object):

    def __init__(self):
        curses.initscr()
        self.window = curses.newwin(HEIGHT, WIDTH, 0, 0)
        self.window.bkgd(curses.ACS_CKBOARD)
        self.window.clear()
        self.window.keypad(1)
        self.key = KEY_RIGHT
        self.worm = [[4, 10], [4, 9], [4, 8]]
        self.food = [10, 20]
        self.map = []
        self.render()

    def render(self):
        self.window.addstr(0, 0, 'O R M')
        self.window.addch(self.food[0], self.food[1], '*')
    
    def start(self):
        while True:
            # fill previous coordinates with ' '
            if len(self.map) > 0: 
                for (i, j) in self.map:
                    self.window.addch(i, j, ' ')
            self.window.refresh()
            self.window.addstr(0, 0, 'O R M')
            self.window.timeout(TIMEOUT)
            prev_key = self.key

            event = self.window.getch()
            self.key = self.key if event == -1 else event

            # spacebar to pause game
            if self.key == ord(' '):
                self.key = -1
                while self.key != ord(' '):
                    self.key = self.window.getch()
                self.key = prev_key
                continue
            
            if self.key not in [KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP]:
                self.key = prev_key

            # update head of worm
            self.worm.insert(0, [self.worm[0][0] + (self.key == KEY_DOWN and 1) + (self.key == KEY_UP and -1), self.worm[0][1] + (self.key == KEY_LEFT and -1) + (self.key == KEY_RIGHT and 1)])
            # check for wall collision // fix later: change direction on collision 
            if self.worm[0][0] == 0 or self.worm[0][0] == HEIGHT - 1 or self.worm[0][1] == 0 or self.worm[0][1] == WIDTH - 1:
                print("hit wall")
                if self.worm[0][0] == 0: #left wall
                    self.key = KEY_RIGHT
                elif self.worm[0][0] == HEIGHT - 1: #bottom wall
                    self.key = KEY_UP
                elif self.worm[0][1] == 0: #top wall
                    self.key = KEY_DOWN
                else:
                    self.key = KEY_LEFT

            if self.worm[0] == self.food:
                self.food = []
                while self.food == []:
                    self.food = [randint(1, HEIGHT - 2), randint(1, WIDTH - 2)]
                    if self.food in self.worm:
                        self.food = []
                self.window.addch(self.food[0], self.food[1], '*')
            else:
                self.last = self.worm.pop()
                self.window.addch(self.last[0], self.last[1], ' ')
            
            self.window.addch(self.worm[0][0], self.worm[0][1], 'ю')
            self.map.append((self.worm[0][0], self.worm[0][1]))
            print(self.map)
            # to fix: add blank char to every point in the map
            #render 1            ###
            #render 2             ###
            #render 3              ###
        curses.endwin()

game = Game()
game.start()