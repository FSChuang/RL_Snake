import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('AykaPot.ttf', 24)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

#RGB Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

Block_size = 20
Speed = 15

class SnakeGame_AI:

    def __init__(self, w = 640, h = 480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        #init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-Block_size/2, self.head.y-Block_size/2),
                      Point(self.head.x-Block_size, self.head.y-Block_size)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        
    def _place_food(self):
        x = random.randint(Block_size/2, (self.w-Block_size/2)//Block_size)*Block_size
        y = random.randint(Block_size/2, (self.h-Block_size/2)//Block_size)*Block_size
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def GamePlay(self, action):
        self.frame_iteration += 1

        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move(action)
        self.snake.insert(0, self.head)

        # 3. check if the game is over
        reward = 0 
        game_over =  False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            g Trame_over =ue
            reward = -10
            return reward, game_over, self.score
        
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(Speed)

        #6. return game over and score
        return reward, game_over, self.score
    
    def is_collision(self, pt=None):
        if pt == None:
            pt = self.head
        # hit boundary
        if pt.x > self.w-Block_size/2 or pt.x < Block_size/2 or pt.y > self.h-Block_size/2 or pt.y < Block_size/2:
            return True
        # hit itself
        if pt in self.snake[1:]:
            return True
        
        return False
    
    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.circle(self.display, BLUE1, (pt.x, pt.y), Block_size/2, 0)

        pygame.draw.circle(self.display, RED, (self.food.x, self.food.y), Block_size/2, 0)

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()

    def _move(self, action):
        # action = [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction) # current direction

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # keep straight, no change on direction
        elif np.array_equal(action, [0, 1, 0]): # right
            next_idx = (idx+1) % 4 
            new_dir = clock_wise[next_idx]
        elif np.array_equal(action, [0, 0, 1]):
            next_idx = (idx-1) % 4
            new_dir = clock_wise[next_idx]
        
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += Block_size
        elif self.direction == Direction.LEFT:
            x -= Block_size
        elif self.direction == Direction.UP:
            y -= Block_size
        elif self.direction == Direction.DOWN:
            y += Block_size

        self.head = Point(x, y)