import torch
from game_for_AI import SnakeGame_AI, Direction, Point
from agent import Agent

file = './model/model.pth'
model = torch.load(file)

game = SnakeGame_AI()
agent = Agent()

while True:
    # get current state
    state_old = agent.get_state(game)
        
    # get AI movement
    final_move = agent.get_action(state_old)

    # perform movement and get new state
    reward, done, score = game.GamePlay(final_move)

    if done:
        game.reset()