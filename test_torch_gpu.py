# script to check if GPU is working with torch

import torch

print(torch.cuda.is_available())
print(torch.cuda.device_count())
