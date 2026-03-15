import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import time
import random

class GraphRenderer:
    def __init__(self, neuron_graph):
        self.graph = neuron_graph
        self.node_radius = 0.05
        self.hovered_node = None
        self.quadric = gluNewQuadric()
        self.pulses = []
        self.explosions = []

    def draw_sphere(self, radius, slices=16, stacks=16):
        gluSphere(self.quadric, radius, slices, stacks)

    def render(self):
        # Setup Volumetric Fog - Sharpened for high contrast foreground
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogfv(GL_FOG_COLOR, (0.02, 0.02, 0.04, 1.0)) # Darker background
        glFogf(GL_FOG_DENSITY, 0.5)
        glHint(GL_FOG_HINT, GL_NICEST)
        glFogf(GL_FOG_START, 12.0) # Start fog slightly further
        glFogf(GL_FOG_END, 25.0)   # Opaque closer to heighten contrast
 
        # Draw organic wobbly connections - High Contrast Glow
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE) # Additive blending for neon glow
        
        current_time = time.time()
        
        # Pass 1: Outer soft glow (thicker, lower alpha)
        glLineWidth(3.0)
        glBegin(GL_LINES)
        for u, v in self.graph.graph.edges:
            if u in self.graph.positions and v in self.graph.positions:
                p1 = self.graph.positions[u]
                p2 = self.graph.positions[v]
                avg_z = (p1[2] + p2[2]) / 2.0
                depth_alpha = max(0.02, min(0.15, 0.15 + (avg_z * 0.04)))
                glColor4f(0.0, 0.8, 1.0, depth_alpha) # Neon Cyan Glow
                
                mid_x = (p1[0] + p2[0]) / 2.0
                mid_y = (p1[1] + p2[1]) / 2.0
                mid_z = (p1[2] + p2[2]) / 2.0
                dist = math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))
                wobble = math.sin(current_time * 1.5 + hash(f"{u}{v}") % 10) * dist * 0.15
                
                glVertex3f(p1[0], p1[1], p1[2])
                glVertex3f(mid_x, mid_y + wobble, mid_z + wobble)
                glVertex3f(mid_x, mid_y + wobble, mid_z + wobble)
                glVertex3f(p2[0], p1[1], p2[2])
        glEnd()

        # Pass 2: Inner sharp core (thinner, higher alpha)
        glLineWidth(1.2)
        glBegin(GL_LINES)
        for u, v in self.graph.graph.edges:
            if u in self.graph.positions and v in self.graph.positions:
                p1 = self.graph.positions[u]
                p2 = self.graph.positions[v]
                avg_z = (p1[2] + p2[2]) / 2.0
                depth_alpha = max(0.1, min(0.6, 0.6 + (avg_z * 0.06)))
                glColor4f(0.8, 0.9, 1.0, depth_alpha) # Sharp White/Blue core
                
                mid_x = (p1[0] + p2[0]) / 2.0
                mid_y = (p1[1] + p2[1]) / 2.0
                mid_z = (p1[2] + p2[2]) / 2.0
                dist = math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))
                wobble = math.sin(current_time * 1.5 + hash(f"{u}{v}") % 10) * dist * 0.15
                
                glVertex3f(p1[0], p1[1], p1[2])
                glVertex3f(mid_x, mid_y + wobble, mid_z + wobble)
                glVertex3f(mid_x, mid_y + wobble, mid_z + wobble)
                glVertex3f(p2[0], p1[1], p2[2])
        glEnd()
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # Reset to standard blend
        
        # Synaptic Pulses
        if random.random() < 0.2 and self.graph.graph.edges:
            edge = random.choice(list(self.graph.graph.edges))
            self.pulses.append({'edge': edge, 'progress': 0.0, 'speed': random.uniform(0.01, 0.04)})
            
        glPointSize(4.0)
        glBegin(GL_POINTS)
        glColor4f(0.9, 1.0, 1.0, 1.0) # Bright glowing cyan/white particles
        new_pulses = []
        for p in self.pulses:
            u, v = p['edge']
            if u in self.graph.positions and v in self.graph.positions:
                p1 = self.graph.positions[u]
                p2 = self.graph.positions[v]
                x = p1[0] + (p2[0] - p1[0]) * p['progress']
                y = p1[1] + (p2[1] - p1[1]) * p['progress']
                z = p1[2] + (p2[2] - p1[2]) * p['progress']
                glVertex3f(x, y, z)
            p['progress'] += p['speed']
            if p['progress'] < 1.0:
                new_pulses.append(p)
        self.pulses = new_pulses
        glEnd()

        # Draw living nodes (Dual-layered 3D)
        for node_id, pos in self.graph.positions.items():
            glPushMatrix()
            glTranslatef(pos[0], pos[1], pos[2])
            
            # Sine wave biological pulsation based on string hash to randomize phase offset
            offset = hash(node_id) % 10
            pulse = (math.sin(current_time * 2.5 + offset) + 1.0) * 0.5
            pulsating_radius = self.node_radius * (1.0 + pulse * 0.6)
            
            # Depth of field dimming logic
            z_fade = max(0.1, min(1.0, 1.0 + (pos[2] * 0.08)))
            
            if node_id == self.hovered_node:
                # Hover: Electric Hot Pink / Intense Gold
                glColor4f(1.0, 0.2, 0.6, 1.0) # Hot Pink Core
                self.draw_sphere(self.node_radius * 0.9)
                # Middle Layer
                glColor4f(1.0, 0.8, 0.0, 0.9) # Electric Gold
                self.draw_sphere(self.node_radius * 2.0)
                # Outer membrane
                glColor4f(1.0, 0.5, 0.0, 0.3) 
                self.draw_sphere(self.node_radius * 4.5)
                
                # Spawn explosion particles if newly hovered
                if not getattr(self, '_last_hovered', None) == node_id:
                    self._last_hovered = node_id
                    for _ in range(30):
                        self.explosions.append({
                            'pos': [pos[0], pos[1], pos[2]],
                            'vel': [random.uniform(-0.15, 0.15), random.uniform(-0.15, 0.15), random.uniform(-0.15, 0.15)],
                            'life': 1.0
                        })
            else:
                # High Contrast Neon Cyan Core
                core_alpha = 1.0 * z_fade
                glColor4f(0.0, 1.0, 1.0, core_alpha) # Pure Neon Cyan
                self.draw_sphere(self.node_radius * 0.35)
                
                # Inner Shell
                inner_alpha = 0.8 * z_fade
                glColor4f(0.5, 0.9, 1.0, inner_alpha)
                self.draw_sphere(self.node_radius * 0.8)
                
                # Outer pulsating membrane
                outer_alpha = (0.2 + (pulse * 0.25)) * z_fade
                glColor4f(0.0, 0.4, 1.0, outer_alpha)
                self.draw_sphere(pulsating_radius)
                
            glPopMatrix()
            
        # Clear hover tracking if nothing is hovered to allow re-explosion
        if not self.hovered_node:
            self._last_hovered = None
            
        # Draw Particle Explosions
        if self.explosions:
            glPointSize(3.0)
            glBegin(GL_POINTS)
            active_explosions = []
            for p in self.explosions:
                p['life'] -= 0.03
                if p['life'] > 0:
                    p['pos'][0] += p['vel'][0]
                    p['pos'][1] += p['vel'][1]
                    p['pos'][2] += p['vel'][2]
                    glColor4f(1.0, 0.8, 0.3, p['life'])
                    glVertex3f(p['pos'][0], p['pos'][1], p['pos'][2])
                    active_explosions.append(p)
            self.explosions = active_explosions
            glEnd()

    def get_node_screen_positions(self, width, height):
        """Returns map of node_id to (x,y) screen coordinates."""
        mv_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        proj_matrix = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        
        screen_pos = {}
        for node_id, pos in self.graph.positions.items():
            try:
                # gluProject returns (x, y, z) window coordinates
                win_x, win_y, win_z = gluProject(
                    pos[0], pos[1], pos[2],
                    mv_matrix, proj_matrix, viewport
                )
                # Pygame Y axis goes top-down, OpenGL is bottom-up
                screen_pos[node_id] = (win_x, height - win_y, win_z)
            except Exception:
                pass
                
        return screen_pos
