"""
[ML ENGINE] PyTorch Geometric Graph Neural Network (GNN) for Disaster Cascade Prediction.
Nodes represent geographic zones/districts.
Edges represent hazard influence and spatial adjacency.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

class CascadeGNN(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(CascadeGNN, self).__init__()
        # TODO: Define Graph Attention Convolution layers (GATConv)
        self.fc1 = nn.Linear(in_channels, hidden_channels)
        self.fc2 = nn.Linear(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return torch.sigmoid(x)
