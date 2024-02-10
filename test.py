from IPython.display import display, Image
import matplotlib.pyplot as plt
import numpy as np
import torch

device = torch.device('cuda')
if device.type == 'cuda':
    print("True")