class LessonManager:
    def __init__(self, neuron_graph, info_panel):
        self.graph = neuron_graph
        self.panel = info_panel
        self.active_node = None
        
    def open(self, node_id):
        if node_id in self.graph.nodes_data:
            self.active_node = node_id
            
    def close(self):
        self.active_node = None
        
    def is_open(self):
        return self.active_node is not None
        
    def draw(self, surface):
        if self.active_node:
            node_data = self.graph.nodes_data[self.active_node]
            self.panel.draw(surface, node_data)
