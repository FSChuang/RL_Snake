import pygame
import random
from enum import Enum
from collections import namedtuple
import sys

pygame.init()
font = pygame.font.Font('AykaPoT.ttf', 24)

class Direction(Enum):
    RIGHT =  1
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

class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        #init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        
        #init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2) #respawn in the middle
        self.snake = [self.head,
                      Point(self.head.x-Block_size, self.head.y),
                      Point(self.head.x-2*Block_size, self.head.y)] #initial length = 3

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(Block_size/2, (self.w-Block_size/2)//Block_size)*Block_size
        y = random.randint(Block_size/2, (self.h-Block_size/2)//Block_size)*Block_size
        self.food = Point(x, y)
        if self.food in self.snake: # food been eaten
            self._place_food

    def GamePlay(self):
        # 1. collect input from user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # 2. Move
        self._move(self.direction)
        self.snake.insert(0, self.head) # update the head of the snake

        # 3. check if the game is over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop() # there's an addition in length in move()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(Speed)

        # 6. return game over and score
        return game_over, self.score
    
    def _is_collision(self):
        # hit boundary of the window
        if self.head.x > self.w-Block_size/2 or self.head.x < Block_size/2 or self.head.y > self.h-Block_size/2 or self.head.y < Block_size/2:
            return True
        # hit itself
        if self.head in self.snake[1:]:
            return True
        
        return False
    
    def _update_ui(self):
        self.display.fill(BLACK)

        # snake
        for pt in self.snake:
            pygame.draw.circle(self.display, BLUE1, (pt.x, pt.y), Block_size/2, 0)
        # apple
        pygame.draw.circle(self.display, RED, (self.food.x, self.food.y), Block_size/2, 0)
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()
        

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += Block_size
        elif direction == Direction.LEFT:
            x -= Block_size
        elif direction == Direction.UP:
            y -= Block_size
        elif direction == Direction.DOWN:
            y += Block_size
        
        self.head = Point(x, y)

if __name__ == '__main__':
    game = SnakeGame()

    while True:
        game_over, score = game.GamePlay()

        if game_over == True:
            break
    print('Final Score: ', score)

    pygame.quit()