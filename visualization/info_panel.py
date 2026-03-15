import pygame

class InfoPanel:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        if not pygame.font.get_init():
            pygame.font.init()
        self.font_title = pygame.font.SysFont('Arial', 32, bold=True)
        self.font_body = pygame.font.SysFont('Arial', 24)
        
    def draw(self, surface, node_data):
        if not node_data:
            return
            
        panel_w = 600
        panel_h = 320
        panel_x = (self.width - panel_w) // 2
        panel_y = self.height - panel_h - 40
        
        panel_surface = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (25, 25, 35, 230), panel_surface.get_rect(), border_radius=15)
        pygame.draw.rect(panel_surface, (80, 150, 255, 255), panel_surface.get_rect(), width=3, border_radius=15)
        
        title_surf = self.font_title.render(node_data.get('title', 'Unknown Node'), True, (255, 255, 255))
        
        # Word wrap description
        words = node_data.get('description', '').split(' ')
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if self.font_body.size(test_line)[0] > panel_w - 40:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
            
        panel_surface.blit(title_surf, (20, 20))
        y_offset = 60
        for line in lines:
            line_surf = self.font_body.render(line, True, (210, 210, 220))
            panel_surface.blit(line_surf, (20, y_offset))
            y_offset += 25
            
        surface.blit(panel_surface, (panel_x, panel_y))
