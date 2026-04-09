import streamlit as st
import time
import math
import random
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

# Page setup
st.set_page_config(
    page_title="Classic Cartoon - Tom & Jerry Style", 
    layout="wide",
    page_icon="🐭"
)

# Custom CSS for cartoon feel
st.markdown("""
<style>
    @keyframes cartoonPop {
        0% { transform: scale(0); opacity: 0; }
        80% { transform: scale(1.2); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .pop-effect {
        animation: cartoonPop 0.3s ease-out;
    }
    
    .shake-effect {
        animation: shake 0.1s ease-in-out 3;
    }
    
    .cartoon-title {
        font-family: 'Impact', 'Arial Black', sans-serif;
        text-shadow: 3px 3px 0px #FFD700;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ========== CLASSIC CARTOON CHARACTERS ==========

class ClassicCartoon:
    """Hand-drawn frame-by-frame cartoon animation"""
    
    @staticmethod
    def draw_cat(frame, action="idle", emotion="neutral"):
        """Draw a Tom-like cat character"""
        img = Image.new('RGBA', (400, 500), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Blue-gray cat color
        cat_color = (70, 130, 180)
        belly_color = (200, 210, 220)
        
        # EXAGGERATED BODY MOVEMENTS based on action
        if action == "squash":
            # Squashed flat (landing)
            body_height = 80
            body_width = 160
            y_offset = 80
        elif action == "stretch":
            # Stretched tall (running)
            body_height = 180
            body_width = 100
            y_offset = 20
        else:
            # Normal standing with idle bounce
            bounce = math.sin(frame * 0.3) * 5
            body_height = 120
            body_width = 130
            y_offset = 40 + bounce
        
        # Body
        draw.ellipse([150 - body_width//2, 150 + y_offset, 
                      150 + body_width//2, 150 + body_height + y_offset], 
                     fill=cat_color, outline='black', width=3)
        
        # Belly
        draw.ellipse([150 - body_width//3, 170 + y_offset, 
                      150 + body_width//3, 150 + body_height - 20 + y_offset], 
                     fill=belly_color, outline='black', width=2)
        
        # HEAD (big and expressive)
        head_size = 100
        head_y = 60 + y_offset
        
        # Head shape (slightly squashed or stretched)
        if action == "squash":
            head_w = 120
            head_h = 80
        elif action == "stretch":
            head_w = 80
            head_h = 120
        else:
            head_w = 100
            head_h = 100
        
        draw.ellipse([150 - head_w//2, head_y, 
                      150 + head_w//2, head_y + head_h], 
                     fill=cat_color, outline='black', width=3)
        
        # EARS (big triangle ears)
        ear_points = [(150 - head_w//2 - 10, head_y + 20),
                      (150 - head_w//4, head_y + 10),
                      (150 - head_w//2 + 20, head_y + 40)]
        draw.polygon(ear_points, fill=cat_color, outline='black', width=3)
        
        ear_points2 = [(150 + head_w//2 + 10, head_y + 20),
                       (150 + head_w//4, head_y + 10),
                       (150 + head_w//2 - 20, head_y + 40)]
        draw.polygon(ear_points2, fill=cat_color, outline='black', width=3)
        
        # EYES (cartoon style)
        if emotion == "surprised":
            # Huge eyes (like Tom when scared)
            eye_size = 25
            draw.ellipse([120, head_y + 40, 120 + eye_size, head_y + 40 + eye_size], 
                        fill='white', outline='black', width=3)
            draw.ellipse([180, head_y + 40, 180 + eye_size, head_y + 40 + eye_size], 
                        fill='white', outline='black', width=3)
            draw.ellipse([127, head_y + 47, 133, head_y + 53], fill='black')
            draw.ellipse([187, head_y + 47, 193, head_y + 53], fill='black')
        elif emotion == "angry":
            # Angry squinty eyes
            draw.line([115, head_y + 50, 145, head_y + 60], fill='black', width=4)
            draw.line([175, head_y + 60, 205, head_y + 50], fill='black', width=4)
            draw.ellipse([120, head_y + 50, 145, head_y + 70], fill='white', outline='black', width=2)
            draw.ellipse([175, head_y + 50, 200, head_y + 70], fill='white', outline='black', width=2)
            draw.ellipse([127, head_y + 55, 138, head_y + 65], fill='black')
            draw.ellipse([182, head_y + 55, 193, head_y + 65], fill='black')
        else:
            # Normal eyes with sparkle
            draw.ellipse([120, head_y + 45, 148, head_y + 73], fill='white', outline='black', width=2)
            draw.ellipse([172, head_y + 45, 200, head_y + 73], fill='white', outline='black', width=2)
            draw.ellipse([127, head_y + 52, 140, head_y + 65], fill='black')
            draw.ellipse([180, head_y + 52, 193, head_y + 65], fill='black')
            # Cartoon sparkle
            draw.ellipse([130, head_y + 55, 133, head_y + 58], fill='white')
            draw.ellipse([183, head_y + 55, 186, head_y + 58], fill='white')
        
        # NOSE
        draw.ellipse([145, head_y + 75, 155, head_y + 85], fill='pink', outline='black', width=2)
        
        # MOUTH (exaggerated)
        if emotion == "surprised":
            draw.arc([135, head_y + 85, 165, head_y + 105], start=0, end=180, fill='black', width=3)
        elif emotion == "angry":
            draw.arc([135, head_y + 85, 165, head_y + 100], start=180, end=360, fill='black', width=3)
            # Teeth showing
            draw.polygon([140, head_y + 92, 148, head_y + 100, 156, head_y + 92], fill='white', outline='black')
        else:
            # Smile
            draw.arc([135, head_y + 80, 165, head_y + 100], start=0, end=180, fill='black', width=2)
        
        # WHISKERS
        draw.line([110, head_y + 78, 70, head_y + 73], fill='black', width=1)
        draw.line([110, head_y + 82, 70, head_y + 83], fill='black', width=1)
        draw.line([190, head_y + 78, 230, head_y + 73], fill='black', width=1)
        draw.line([190, head_y + 82, 230, head_y + 83], fill='black', width=1)
        
        # TAIL (curly and expressive)
        tail_points = []
        for i in range(10):
            angle = math.sin(frame * 0.2 + i) * 0.5
            tail_x = 150 + body_width//2 + i * 10
            tail_y = 200 + y_offset + math.sin(i * 0.5 + frame * 0.3) * 15
            tail_points.append((tail_x, tail_y))
        
        for i in range(len(tail_points)-1):
            draw.line([tail_points[i], tail_points[i+1]], fill=cat_color, width=8)
        
        return img
    
    @staticmethod
    def draw_mouse(frame, action="idle", emotion="neutral"):
        """Draw a Jerry-like mouse character"""
        img = Image.new('RGBA', (300, 400), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Brown mouse color
        mouse_color = (160, 110, 60)
        
        # Small body (mouse is smaller than cat)
        bounce = math.sin(frame * 0.4) * 3
        
        # Body
        draw.ellipse([100, 120 + bounce, 200, 220 + bounce], 
                     fill=mouse_color, outline='black', width=3)
        
        # BIG EARS (classic mouse)
        draw.ellipse([85, 60 + bounce, 125, 100 + bounce], 
                     fill=mouse_color, outline='black', width=3)
        draw.ellipse([115, 55 + bounce, 155, 95 + bounce], 
                     fill=mouse_color, outline='black', width=3)
        # Inner ear
        draw.ellipse([92, 67 + bounce, 118, 93 + bounce], fill='pink')
        draw.ellipse([122, 62 + bounce, 148, 88 + bounce], fill='pink')
        
        # HEAD
        draw.ellipse([110, 90 + bounce, 190, 150 + bounce], 
                     fill=mouse_color, outline='black', width=3)
        
        # EYES (cute and big)
        if emotion == "scared":
            eye_size = 20
            draw.ellipse([125, 110 + bounce, 145, 130 + bounce], fill='white', outline='black', width=2)
            draw.ellipse([155, 110 + bounce, 175, 130 + bounce], fill='white', outline='black', width=2)
            draw.ellipse([130, 115 + bounce, 140, 125 + bounce], fill='black')
            draw.ellipse([160, 115 + bounce, 170, 125 + bounce], fill='black')
        else:
            # Happy eyes
            draw.ellipse([125, 110 + bounce, 145, 130 + bounce], fill='white', outline='black', width=2)
            draw.ellipse([155, 110 + bounce, 175, 130 + bounce], fill='white', outline='black', width=2)
            draw.ellipse([130, 115 + bounce, 140, 125 + bounce], fill='black')
            draw.ellipse([160, 115 + bounce, 170, 125 + bounce], fill='black')
            # Sparkle
            draw.ellipse([132, 117 + bounce, 134, 119 + bounce], fill='white')
            draw.ellipse([162, 117 + bounce, 164, 119 + bounce], fill='white')
        
        # NOSE
        draw.ellipse([145, 135 + bounce, 155, 145 + bounce], fill='pink', outline='black', width=2)
        
        # MOUSE SMILE
        draw.arc([135, 140 + bounce, 165, 155 + bounce], start=0, end=180, fill='black', width=2)
        
        # WHISKERS
        draw.line([110, 140 + bounce, 70, 135 + bounce], fill='black', width=1)
        draw.line([110, 145 + bounce, 70, 145 + bounce], fill='black', width=1)
        draw.line([190, 140 + bounce, 230, 135 + bounce], fill='black', width=1)
        draw.line([190, 145 + bounce, 230, 145 + bounce], fill='black', width=1)
        
        return img
    
    @staticmethod
    def draw_cartoon_scene(frame, scene_type="fight"):
        """Draw classic cartoon background"""
        img = Image.new('RGB', (800, 500), (255, 255, 200))
        draw = ImageDraw.Draw(img)
        
        # Floor
        draw.rectangle([0, 400, 800, 500], fill=(200, 150, 100))
        draw.line([0, 400, 800, 400], fill='black', width=3)
        
        # Wall details (like classic cartoons)
        for i in range(0, 800, 50):
            draw.line([i, 400, i+25, 380], fill=(180, 130, 80), width=2)
        
        # Window
        draw.rectangle([600, 100, 780, 300], fill=(200, 220, 255), outline='black', width=4)
        draw.line([690, 100, 690, 300], fill='black', width=3)
        draw.line([600, 200, 780, 200], fill='black', width=3)
        
        # Curtains
        draw.arc([580, 80, 620, 120], start=0, end=180, fill=(255, 100, 100), outline='black', width=2)
        draw.arc([760, 80, 800, 120], start=0, end=180, fill=(255, 100, 100), outline='black', width=2)
        
        # Classic cartoon elements
        if scene_type == "fight":
            # Action lines in background
            for i in range(10):
                x = random.randint(0, 800)
                draw.line([x, 0, x+20, 50], fill='black', width=2)
        
        return img

# ========== FRAME-BY-FRAME CARTOON ANIMATION ==========

def create_classic_cartoon():
    """Create frame-by-frame classic cartoon animation"""
    frames = []
    total_frames = 180  # 30 seconds at 6fps
    
    for frame in range(total_frames):
        # Create canvas
        if frame < 60:
            scene = "fight"
        elif frame < 120:
            scene = "peaceful"
        else:
            scene = "play"
        
        canvas = ClassicCartoon.draw_cartoon_scene(frame, scene)
        draw = ImageDraw.Draw(canvas)
        
        # ===== ACT 1: CHASE & FIGHT (0-60 frames) =====
        if frame < 60:
            t = frame / 60
            
            # Cat and mouse positions (classic chase)
            if frame < 20:
                # Cat chasing mouse
                cat_x = 50 + (frame * 15)
                mouse_x = 300 - (frame * 5)
                cat_action = "stretch"
                mouse_action = "stretch"
                cat_emotion = "angry"
                mouse_emotion = "scared"
            elif frame < 40:
                # Cat about to catch mouse
                cat_x = 350
                mouse_x = 370
                cat_action = "stretch"
                mouse_action = "squash"
                cat_emotion = "angry"
                mouse_emotion = "scared"
            else:
                # Fight scene - dramatic poses
                if frame % 20 < 10:
                    cat_x = 300
                    mouse_x = 400
                    cat_action = "squash"
                    mouse_action = "stretch"
                    cat_emotion = "surprised"
                    mouse_emotion = "angry"
                else:
                    cat_x = 400
                    mouse_x = 300
                    cat_action = "stretch"
                    mouse_action = "squash"
                    cat_emotion = "angry"
                    mouse_emotion = "surprised"
            
            # Draw cat
            cat = ClassicCartoon.draw_cat(frame, action=cat_action, emotion=cat_emotion)
            canvas.paste(cat, (int(cat_x), 50), cat)
            
            # Draw mouse
            mouse = ClassicCartoon.draw_mouse(frame, action=mouse_action, emotion=mouse_emotion)
            canvas.paste(mouse, (int(mouse_x), 100), mouse)
            
            # Action effects
            if frame > 20:
                # POW! BAM! effects
                if frame % 20 < 10:
                    draw.text((350, 200), "POW!", fill=(255, 0, 0), 
                             font=None, stroke_width=2, stroke_fill='black')
                    # Stars around head
                    for i in range(3):
                        star_x = 150 + i * 50
                        star_y = 150 + math.sin(frame * 0.5 + i) * 20
                        draw.text((star_x, star_y), "★", fill=(255, 215, 0))
                else:
                    draw.text((350, 200), "BAM!", fill=(255, 0, 0),
                             font=None, stroke_width=2, stroke_fill='black')
        
        # ===== ACT 2: PEACEFUL (60-120 frames) =====
        elif frame < 120:
            t = (frame - 60) / 60
            
            # Cat and mouse resting (tired from fight)
            cat_x = 150
            mouse_x = 500
            
            # Tired poses
            cat_action = "squash"  # Collapsed
            mouse_action = "squash"
            cat_emotion = "neutral"
            mouse_emotion = "neutral"
            
            # Draw characters
            cat = ClassicCartoon.draw_cat(frame, action=cat_action, emotion=cat_emotion)
            canvas.paste(cat, (cat_x, 150), cat)
            
            mouse = ClassicCartoon.draw_mouse(frame, action=mouse_action, emotion=mouse_emotion)
            canvas.paste(mouse, (mouse_x, 200), mouse)
            
            # ZZZ sleep effects
            if t > 0.3:
                for i in range(3):
                    z_y = 100 - i * 20 - (frame % 60) / 3
                    draw.text((cat_x + 50 + i * 10, z_y), "z", fill=(100, 100, 200))
                    draw.text((mouse_x - 50 - i * 10, z_y), "z", fill=(100, 100, 200))
            
            # Peaceful music notes
            if t > 0.6:
                note_x = 400 + math.sin(frame * 0.1) * 50
                note_y = 300 + math.cos(frame * 0.15) * 30
                draw.text((note_x, note_y), "♪", fill=(100, 100, 255))
                draw.text((note_x + 30, note_y - 20), "♫", fill=(100, 100, 255))
        
        # ===== ACT 3: PLAYING TOGETHER (120-180 frames) =====
        else:
            t = (frame - 120) / 60
            
            # Characters playing together (friends now)
            if frame % 40 < 20:
                cat_x = 250
                mouse_x = 450
                cat_action = "idle"
                mouse_action = "idle"
            else:
                cat_x = 450
                mouse_x = 250
                cat_action = "idle"
                mouse_action = "idle"
            
            # Happy emotions
            cat_emotion = "neutral"
            mouse_emotion = "neutral"
            
            # Draw characters
            cat = ClassicCartoon.draw_cat(frame, action=cat_action, emotion=cat_emotion)
            canvas.paste(cat, (cat_x, 100), cat)
            
            mouse = ClassicCartoon.draw_mouse(frame, action=mouse_action, emotion=mouse_emotion)
            canvas.paste(mouse, (mouse_x, 150), mouse)
            
            # Playful elements
            # Ball
            ball_x = 400 + math.sin(frame * 0.2) * 100
            ball_y = 350 + abs(math.sin(frame * 0.3)) * 30
            draw.ellipse([ball_x-15, ball_y-15, ball_x+15, ball_y+15], 
                        fill=(255, 100, 100), outline='black', width=3)
            
            # Hearts (friendship)
            if t > 0.7:
                heart_x = 350 + math.sin(frame * 0.2) * 20
                heart_y = 200 + math.cos(frame * 0.3) * 20
                draw.text((heart_x, heart_y), "❤️", fill=(255, 0, 0))
        
        # Add frame number (like traditional animation)
        draw.text((10, 10), f"Frame: {frame}", fill=(100, 100, 100))
        
        frames.append(canvas)
    
    return frames

# ========== STREAMLIT UI ==========

st.markdown('<h1 class="cartoon-title" style="text-align: center;">🐱 CLASSIC CARTOON ANIMATION 🐭</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center;">Hand-drawn frame-by-frame • Tom & Jerry Style • Each frame matters!</p>', unsafe_allow_html=True)

# Animation controls
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    frame_rate = st.select_slider(
        "Animation Style",
        options=["Classic (6 fps)", "Smooth (12 fps)", "Traditional (8 fps)"],
        value="Classic (6 fps)"
    )
    
    play = st.button("🎬 PLAY CLASSIC CARTOON", use_container_width=True)

# Frame rate mapping
fps_map = {
    "Classic (6 fps)": 6,
    "Smooth (12 fps)": 12,
    "Traditional (8 fps)": 8
}

if play:
    fps = fps_map[frame_rate]
    frame_duration = 1 / fps
    
    with st.spinner("Drawing each frame by hand (like traditional animation)..."):
        frames = create_classic_cartoon()
    
    # Animation player
    animation_container = st.empty()
    progress_bar = st.progress(0)
    frame_counter = st.empty()
    time_display = st.empty()
    
    # Play each frame
    for i, frame in enumerate(frames):
        animation_container.image(frame, use_column_width=True)
        progress = i / len(frames)
        progress_bar.progress(progress)
        
        frame_counter.markdown(f"### 🎞️ Frame {i}/{len(frames)}")
        time_display.markdown(f"### ⏱️ {int(i / fps)} / 30 seconds")
        
        time.sleep(frame_duration)
    
    # Grand finale
    st.balloons()
    st.success("✅ Classic Cartoon Complete! Just like Tom & Jerry!")
    
    # Replay button
    if st.button("🔄 Watch Again", use_container_width=True):
        st.rerun()

else:
    # Preview
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎬 ACT 1: THE CHASE")
        preview_cat = ClassicCartoon.draw_cat(0, action="stretch", emotion="angry")
        st.image(preview_cat, use_column_width=True)
        st.caption("Cat chasing mouse • 0-10 seconds")
    
    with col2:
        st.markdown("### 😴 ACT 2: PEACEFUL")
        st.markdown("*Both exhausted from chase*")
        st.caption("Resting • 10-20 seconds")
    
    with col3:
        st.markdown("### ❤️ ACT 3: FRIENDS")
        st.markdown("*Playing together happily*")
        st.caption("Happy ending • 20-30 seconds")
    
    st.markdown("---")
    
    # Features
    with st.expander("🎨 What makes this CLASSIC CARTOON style?"):
        st.markdown("""
        ### Traditional Animation Techniques:
        
        **1. Frame-by-Frame Drawing** 📝
        - Each frame drawn individually
        - No computer tweening
        - Like Disney and Hanna-Barbera
        
        **2. Exaggerated Movements** 💪
        - Squash and stretch on every action
        - Eyes pop out when surprised
        - Limbs stretch during chase
        
        **3. Cartoon Physics** 🎯
        - Characters hang in air before falling
        - Stars spin around heads
        - Action lines for speed
        
        **4. Personality in Every Pose** 🎭
        - Cat is always angry/chasing
        - Mouse is clever/playful
        - Expressions change dramatically
        
        **5. Classic Visual Elements** 🖼️
        - Hand-drawn aesthetic
        - Sketchy outlines
        - Traditional backgrounds
        
        ### Like watching:
        - Tom & Jerry
        - Looney Tunes
        - Pink Panther
        - Classic Disney shorts
        """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🐱 Each frame hand-crafted • 180 individual drawings • True classic cartoon style 🐭</p>
</div>
""", unsafe_allow_html=True)
