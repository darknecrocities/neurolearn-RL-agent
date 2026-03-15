import torch
import torch.nn as nn
import torch.nn.functional as F

class GestureClassifier(nn.Module):
    def __init__(self, input_size=42, num_classes=6):
        super(GestureClassifier, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, num_classes)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return x
        
    def predict(self, x):
        """Predicts the class index from features."""
        # Add batch dimension if necessary
        if len(x.shape) == 1:
            x = x.unsqueeze(0)
            
        with torch.no_grad():
            logits = self(x)
            probs = F.softmax(logits, dim=1)
            return torch.argmax(probs, dim=1).item()
