import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
import sys

# Add parent directory to path to allow importing gesture_classifier
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.gesture_classifier import GestureClassifier

def generate_synthetic_data(num_samples_per_class=1000):
    """
    Generates synthetic landmark data for training.
    """
    X = []
    y = []
    
    for _ in range(num_samples_per_class):
        for label in range(6):
            features = np.random.uniform(-1, 1, 42)
            
            # Simple heuristic modifiers to separate classes
            if label == 1: # pinch: thumb tip (8,9) close to index tip (16,17)
                features[8] = features[16] + np.random.uniform(-0.05, 0.05)
                features[9] = features[17] + np.random.uniform(-0.05, 0.05)
            elif label == 2: # open hand: tips far from wrist
                # Indices for tips: 8, 16, 24, 32, 40 (x) and +1 for (y)
                for i in [8, 16, 24, 32, 40]:
                    features[i] = np.random.uniform(0.6, 1.0) * np.sign(features[i])
                    features[i+1] = np.random.uniform(0.6, 1.0) * np.sign(features[i])
            elif label == 3: # closed fist: tips near wrist (0, 0)
                for i in [8, 16, 24, 32, 40]:
                    features[i] = np.random.uniform(-0.2, 0.2)
                    features[i+1] = np.random.uniform(-0.2, 0.2)

            X.append(features)
            y.append(label)
            
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int64)

def train():
    print("Generating synthetic data...")
    X, y = generate_synthetic_data(2000)
    X_tensor = torch.tensor(X)
    y_tensor = torch.tensor(y)
    
    model = GestureClassifier()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    epochs = 50
    print("Starting training...")
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X_tensor)
        loss = criterion(outputs, y_tensor)
        loss.backward()
        optimizer.step()
        
        if (epoch+1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
            
    os.makedirs('models', exist_ok=True)
    save_path = 'models/gesture_model.pth'
    torch.save(model.state_dict(), save_path)
    print(f"Model saved to {save_path}")

if __name__ == "__main__":
    train()
