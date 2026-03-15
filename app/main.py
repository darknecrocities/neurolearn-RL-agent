import os
import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from dotenv import load_dotenv
import cv2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vision.hand_tracker import HandTracker
from vision.landmark_processor import LandmarkProcessor
from app.cursor_controller import CursorController
from app.gesture_controller import GestureController
from app.lesson_manager import LessonManager
from visualization.neuron_graph import NeuronGraph
from visualization.graph_renderer import GraphRenderer
from visualization.camera_rotation import CameraRotation
from visualization.info_panel import InfoPanel
from utils.math_utils import calculate_distance

# Load .env
load_dotenv()
CAMERA_INDEX = int(os.environ.get('CAMERA_INDEX', 0))
GESTURE_MODEL_PATH = os.environ.get('GESTURE_MODEL_PATH', 'models/gesture_model.pth')
LESSON_DATA = os.environ.get('LESSON_DATA', 'data/rl_lessons.json')
CURSOR_SMOOTHING = float(os.environ.get('CURSOR_SMOOTHING', 0.75))
PINCH_THRESHOLD = float(os.environ.get('PINCH_THRESHOLD', 0.04))
GRAPH_ROTATION_SPEED = float(os.environ.get('GRAPH_ROTATION_SPEED', 0.6))

def init_opengl(width, height):
    glClearColor(0.02, 0.02, 0.04, 1.0) # Matches high-contrast fog color
    glEnable(GL_DEPTH_TEST)
    try:
        if bool(glutInit):
            glutInit()
    except Exception:
        pass
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width/height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_surface_to_opengl(surface, display_w, display_h):
    """Render a Pygame surface over the OpenGL scene."""
    img_data = pygame.image.tostring(surface, "RGBA", True)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, display_w, 0, display_h, -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(), 
                 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
                 
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(display_w, 0)
    glTexCoord2f(1, 1); glVertex2f(display_w, display_h)
    glTexCoord2f(0, 1); glVertex2f(0, display_h)
    glEnd()
    
    glDeleteTextures(1, [tex_id])
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def draw_background_camera(frame, display_w, display_h):
    """Render the camera frame as a fullscreen background in OpenGL."""
    # Frame comes in as RGB from cv2.cvtColor
    frame = cv2.flip(frame, 1) # Mirror the camera frame
    img_data = frame.tobytes()
    frame_h, frame_w, _ = frame.shape
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, display_w, 0, display_h, -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST) # Draw behind everything
    glEnable(GL_TEXTURE_2D)
    
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # OpenCV image origin is top-left, but OpenGL is bottom-left, so it'll render upside down if not flipped
    # OpenCV tobytes() packs row by row from top to bottom
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, frame_w, frame_h, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
                 
    # Map texture to quad. To fix upside down frame, flip V coordinates.
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0) # White multiplies by texture colors directly
    glTexCoord2f(0, 1); glVertex2f(0, 0)
    glTexCoord2f(1, 1); glVertex2f(display_w, 0)
    glTexCoord2f(1, 0); glVertex2f(display_w, display_h)
    glTexCoord2f(0, 0); glVertex2f(0, display_h)
    glEnd()
    
    glDeleteTextures(1, [tex_id])
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST) # Re-enable depth for 3D elements
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def main():
    if not pygame.get_init():
        pygame.init()
    display = (1024, 768)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("NeuroLearn Gesture Navigator")
    
    overlay_surface = pygame.Surface(display, pygame.SRCALPHA)
    init_opengl(*display)
    
    # Initialize Core Components
    tracker = HandTracker()
    processor = LandmarkProcessor()
    gesture_ctrl = GestureController(GESTURE_MODEL_PATH)
    cursor_ctrl = CursorController(display[0], display[1], CURSOR_SMOOTHING)
    
    graph = NeuronGraph(LESSON_DATA)
    renderer = GraphRenderer(graph)
    cam_rot = CameraRotation(GRAPH_ROTATION_SPEED)
    panel = InfoPanel(*display)
    lesson_mgr = LessonManager(graph, panel)
    
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print(f"Error: Could not open camera {CAMERA_INDEX}")
        return
        
    clock = pygame.time.Clock()
    running = True
    
    prev_pinch_dist = None
    prev_two_hand_dist = None
    cursor_trail = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                
        ret, frame = cap.read()
        if not ret:
            continue
            
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = tracker.process(frame_rgb)
        
        cursor_pos = None
        is_pinching = False
        is_rotating = False
        is_canceling = False
        hovered_node = None
        
        overlay_surface.fill((0, 0, 0, 0)) # Clear overlay
        
        if results.multi_hand_landmarks:
            # --- Primary Hand Processing (Index 0) ---
            landmarks = results.multi_hand_landmarks[0]
            features = processor.extract_features(landmarks)
            
            # Machine Learning Prediction
            prediction = gesture_ctrl.predict(features)
            predicted_class = prediction if prediction is not None else 0
            
            # Get Key Points for primary hand
            key_points = processor.get_key_points(landmarks, display[0], display[1])
            index_screen = key_points['index_tip']
            thumb_screen = key_points['thumb_tip']
            
            # Cursor Update
            wrist_norm = landmarks.landmark[0]
            index_norm = landmarks.landmark[8]
            cursor_pos = cursor_ctrl.update((index_norm.x, index_norm.y))
            
            # Pinch Info
            pinch_dist = calculate_distance(index_screen, thumb_screen)
            manual_pinch = pinch_dist < 40
            
            # State Flags
            is_pinching = (predicted_class == 1 or manual_pinch)
            is_rotating = (predicted_class == 2)
            is_canceling = (predicted_class == 3)
            
            # --- Two-Hand Zoom Interaction ---
            two_hand_zoom_active = False
            if len(results.multi_hand_landmarks) >= 2:
                # Use Middle MCP (9) landmarks for stable center-to-center zoom
                h1 = results.multi_hand_landmarks[0].landmark[9]
                h2 = results.multi_hand_landmarks[1].landmark[9]
                
                # Convert to absolute screen coordinates
                p1 = (h1.x * display[0], h1.y * display[1])
                p2 = (h2.x * display[0], h2.y * display[1])
                curr_two_hand_dist = calculate_distance(p1, p2)
                
                if prev_two_hand_dist is not None:
                    # Multiplier for 2-hand zoom - Boosted for snappier tracking
                    zoom_delta = (curr_two_hand_dist - prev_two_hand_dist) * 0.5
                    cam_rot.update_zoom(zoom_delta)
                    two_hand_zoom_active = True
                prev_two_hand_dist = curr_two_hand_dist
            else:
                prev_two_hand_dist = None

            # Fallback to single-hand zoom - ONLY trigger if pinching
            if not two_hand_zoom_active and is_pinching:
                if prev_pinch_dist is not None:
                    # Multiplier for 1-hand pinch - Boosted to "Turbo" sensitivity
                    zoom_delta = (pinch_dist - prev_pinch_dist) * 0.85
                    cam_rot.update_zoom(zoom_delta)
            
            prev_pinch_dist = pinch_dist
            
            if is_rotating:
                # Use wrist movement for rotation
                dy = (wrist_norm.x - 0.5) * GRAPH_ROTATION_SPEED
                dx = (wrist_norm.y - 0.5) * GRAPH_ROTATION_SPEED
                cam_rot.update(dy, dx)
                
            if is_canceling:
                lesson_mgr.close()
        else:
            prev_pinch_dist = None
            prev_two_hand_dist = None

        # --- Post-Processing / Universal Simulation (Runs every frame) ---
        cam_rot.interpolate_zoom()  
        cam_rot.apply_momentum()
        graph.apply_repulsion(hovered_node)
        
        # Determine hovered node using current projection
        glPushMatrix()
        glTranslatef(0.0, 0.0, cam_rot.get_z())
        ax, ay = cam_rot.get_angles()
        glRotatef(ax, 1, 0, 0)
        glRotatef(ay, 0, 1, 0)
        screen_positions = renderer.get_node_screen_positions(*display)
        glPopMatrix()
        
        if cursor_pos:
            for node_id, pos in screen_positions.items():
                if calculate_distance(cursor_pos, (pos[0], pos[1])) < 40:
                    hovered_node = node_id
                    break
                    
        renderer.hovered_node = hovered_node
        
        # Info Panel Logic
        if hovered_node:
            lesson_mgr.open(hovered_node)
        else:
            # Auto-close only if we aren't in a canceling state (safety)
            if not is_canceling:
                lesson_mgr.close()
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # 1. Draw Background Camera
        draw_background_camera(frame_rgb, display[0], display[1])
        
        # 2. Draw 3D Graph Node Scene
        glPushMatrix()
        glTranslatef(0.0, 0.0, cam_rot.get_z())
        ax, ay = cam_rot.get_angles()
        glRotatef(ax, 1, 0, 0)
        glRotatef(ay, 0, 1, 0)
        renderer.render()
        glPopMatrix()
        
        # 2D Render
        if cursor_pos:
            cursor_trail.append(cursor_pos)
            if len(cursor_trail) > 20:
                cursor_trail.pop(0)
        else:
            if len(cursor_trail) > 0:
                cursor_trail.pop(0)
                
        for i, pos in enumerate(cursor_trail):
            alpha = int(255 * (i / len(cursor_trail)))
            radius = int(8 * (i / len(cursor_trail)))
            pygame.draw.circle(overlay_surface, (100, 200, 255, alpha), pos, radius)

        if cursor_pos:
            color = (255, 100, 100) if is_pinching else (100, 200, 255)
            pygame.draw.circle(overlay_surface, color, cursor_pos, 15)
            pygame.draw.circle(overlay_surface, (255, 255, 255), cursor_pos, 15, 2)
            
        lesson_mgr.draw(overlay_surface)
        
        draw_surface_to_opengl(overlay_surface, display[0], display[1])
        pygame.display.flip()
        clock.tick(60)

    cap.release()
    pygame.quit()

if __name__ == "__main__":
    main()
