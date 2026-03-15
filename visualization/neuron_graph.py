import json
import networkx as nx
import numpy as np

class NeuronGraph:
    def __init__(self, json_path):
        self.graph = nx.DiGraph()
        self.nodes_data = {}
        self.base_positions = {}
        self.positions = {}
        self.load_data(json_path)
        self.generate_layout()

    def load_data(self, path):
        with open(path, 'r') as f:
            data = json.load(f)

        for node in data.get('nodes', []):
            node_id = node.get('id')
            self.nodes_data[node_id] = {
                'title': node.get('title', ''),
                'description': node.get('description', '')
            }
            self.graph.add_node(node_id)
            
            # Ensure "reward" exists if referenced in connections
            for conn in node.get('connections', []):
                self.graph.add_edge(node_id, conn)

        # Make sure target nodes exist in nodes_data if not explicitly defined
        for node_id in self.graph.nodes:
            if node_id not in self.nodes_data:
                self.nodes_data[node_id] = {'title': node_id.capitalize(), 'description': ''}

    def generate_layout(self):
        """Generates a 3D spring layout for the graph nodes."""
        pos = nx.spring_layout(self.graph, dim=3, iterations=100, seed=42)
        
        # Scale positions for better OpenGL visualization
        for k, v in pos.items():
            # v is [x, y, z] array from -1 to 1 mostly
            scaled = v * 5.0
            self.base_positions[k] = scaled
            self.positions[k] = np.copy(scaled)
            
    def apply_repulsion(self, hovered_node):
        """
        Spring physics to softly repel nodes from the hovered node.
        """
        for node_id in self.positions:
            base = self.base_positions[node_id]
            curr = self.positions[node_id]
            
            if hovered_node and node_id != hovered_node:
                hover_pos = self.base_positions[hovered_node]
                # Vector from hover to this node
                diff = base - hover_pos
                dist = np.linalg.norm(diff)
                
                # If too close to the hovered point, repel outwards naturally
                if dist > 0 and dist < 1.5:
                    repulsion_force = (1.5 - dist) * 0.5
                    target = base + (diff / dist) * repulsion_force
                else:
                    target = base
            else:
                target = base
                
            # Spring towards target smoothly
            self.positions[node_id] += (target - curr) * 0.1
