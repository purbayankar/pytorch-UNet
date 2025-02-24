import os

from argparse import ArgumentParser
import torch.optim as optim
from unet.model import Model
from unet.dataset import Image2D
from unet.metrics import jaccard_index, f1_score, LogNLLLoss
import torch

parser = ArgumentParser()
parser.add_argument('--dataset', required=True, type=str)
parser.add_argument('--results_path', required=True, type=str)
parser.add_argument('--model_path', required=True, type=str)
parser.add_argument('--device', default='cpu', type=str)
args = parser.parse_args()

predict_dataset = Image2D(args.dataset)
unet = torch.load(args.model_path)
loss = LogNLLLoss()
optimizer = optim.Adam(unet.parameters(), lr=1e-3)

if not os.path.exists(args.results_path):
    os.makedirs(args.results_path)

model = Model(unet, loss, optimizer, checkpoint_folder=args.results_path, device=args.device)

model.predict_dataset(predict_dataset, args.results_path)
