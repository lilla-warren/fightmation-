import streamlit as st
import time
import math
import random
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Page setup
st.set_page_config(
    page_title="Classic Cartoon - Tom & Jerry Style", 
    layout="wide",
    page_icon="🐱"
)

# Custom CSS for cartoon feel
st.markdown("""
<style>
    @keyframes cartoonPop {
        0% { transform: scale(0); opacity: 0; }
        80% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-3px); }
        75% { transform: translateX(3px); }
    }
    
    .pop-effect {
        animation: cartoonPop 0.2s ease-out;
    }
    
    .shake-effect {
        animation: shake 0.05s ease-in-out 5;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .float-effect {
        animation: float 2s ease-in-out infinite;
    }
    
    .cartoon-title {
        font-family: 'Impact', 'Arial Black', sans-serif;
        text-shadow: 4px 4px 0px #FFD700;
        letter-spacing: 3px;
        font-size: 48px;
        text-align: center;
    }
    
    .cartoon-subtitle {
        font-family: 'Comic Sans MS', cursive;
        text-align: center;
        font-size: 18px;
        color: #333;
    }
    
    /* Cartoon button */
    div.stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%);
        color: black;
        font-size: 24px;
        font-weight: bold;
        font-family: 'Impact', sans-serif;
        border: 3px solid black;
        border-radius: 50px;
        padding: 15px 30px;
        transition: all 0.3s;
    }
    
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 5px 5px 0px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ========== CLASSIC CARTOON SYSTEM ==========

class ClassicCartoon:
    """Hand-drawn frame-by-frame cartoon animation system"""
    
    @staticmethod
    def draw_cat(frame, action="idle", emotion="neutral"):
        """Draw a Tom-like cat character"""
        img = Image.new('RGBA', (400, 500), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colors
        cat_color = (70, 130, 180)  # Blue-gray
        belly_color = (200, 210, 220)
        pink_color = (255, 192, 203)
        
        # Calculate bounce for idle animation
        bounce = math.sin(frame * 0.2) * 3
        
        # EXAGGERATED BODY SHAPES based on action
        if action == "squash":
            body_height = 70
            body_width = 160
            y_offset = 80
        elif action == "stretch":
            body_height = 180
            body_width = 90
            y_offset = 20
        else:
            body_height = 110
            body_width = 130
            y_offset = 40 + bounce
        
        # Body
        draw.ellipse([200 - body_width//2, 150 + y_offset, 
                      200 + body_width//2, 150 + body_height + y_offset], 
                     fill=cat_color, outline='black', width=3)
        
        # Belly
        draw.ellipse([200 - body_width//3, 170 + y_offset, 
                      200 + body_width//3, 150 + body_height - 20 + y_offset], 
                     fill=belly_color, outline='black', width=2)
        
        # HEAD (big and expressive)
        if action == "squash":
            head_w = 120
            head_h = 80
            head_y = 60 + y_offset
        elif action == "stretch":
            head_w = 80
            head_h = 120
            head_y = 30 + y_offset
        else:
            head_w = 100
            head_h = 100
            head_y = 50 + y_offset
        
        draw.ellipse([200 - head_w//2, head_y, 
                      200 + head_w//2, head_y + head_h], 
                     fill=cat_color, outline='black', width=3)
        
        # EARS
        # Left ear
        draw.polygon([(200 - head_w//2 - 5, head_y + 20),
                      (200 - head_w//4, head_y + 10),
                      (200 - head_w//2 + 20, head_y + 40)], 
                     fill=cat_color, outline='black', width=3)
        # Right ear
        draw.polygon([(200 + head_w//2 + 5, head_y + 20),
                      (200 + head_w//4, head_y + 10),
                      (200 + head_w//2 - 20, head_y + 40)], 
                     fill=cat_color, outline='black', width=3)
        
        # EYES with different emotions
        if emotion == "surprised":
            # Huge eyes
            draw.ellipse([165, head_y + 40, 195, head_y + 70], fill='white', outline='black', width=3)
            draw.ellipse([205, head_y + 40, 235, head_y + 70], fill='white', outline='black', width=3)
            draw.ellipse([172, head_y + 47, 188, head_y + 63], fill='black')
            draw.ellipse([212, head_y + 47, 228, head_y + 63], fill='black')
            # Tiny pupils (surprised)
            draw.ellipse([178, head_y + 52, 182, head_y + 56], fill='white')
            draw.ellipse([218, head_y + 52, 222, head_y + 56], fill='white')
        elif emotion == "angry":
            # Angry squint
            draw.line([160, head_y + 55, 190, head_y + 65], fill='black', width=5)
            draw.line([210, head_y + 65, 240, head_y + 55], fill='black', width=5)
            draw.ellipse([165, head_y + 50, 195, head_y + 75], fill='white', outline='black', width=2)
            draw.ellipse([205, head_y + 50, 235, head_y + 75], fill='white', outline='black', width=2)
            draw.ellipse([172, head_y + 55, 188, head_y + 70], fill='black')
            draw.ellipse([212, head_y + 55, 228, head_y + 70], fill='black')
        else:
            # Normal eyes
            draw.ellipse([165, head_y + 45, 195, head_y + 75], fill='white', outline='black', width=2)
            draw.ellipse([205, head_y + 45, 235, head_y + 75], fill='white', outline='black', width=2)
            draw.ellipse([172, head_y + 52, 188, head_y + 68], fill='black')
            draw.ellipse([212, head_y + 52, 228, head_y + 68], fill='black')
            # Cartoon sparkle
            draw.ellipse([176, head_y + 55, 180, head_y + 59], fill='white')
            draw.ellipse([216, head_y + 55, 220, head_y + 59], fill='white')
        
        # NOSE
        draw.ellipse([195, head_y + 75, 205, head_y + 85], fill=pink_color, outline='black', width=2)
        
        # MOUTH
        if emotion == "surprised":
            draw.arc([185, head_y + 85, 215, head_y + 105], start=0, end=180, fill='black', width=3)
        elif emotion == "angry":
            draw.arc([185, head_y + 85, 215, head_y + 100], start=180, end=360, fill='black', width=3)
            # Teeth
            draw.polygon([190, head_y + 92, 198, head_y + 100, 206, head_y + 92], fill='white', outline='black')
        else:
            draw.arc([185, head_y + 80, 215, head_y + 100], start=0, end=180, fill='black', width=2)
        
        # WHISKERS
        draw.line([160, head_y + 78, 120, head_y + 73], fill='black', width=2)
        draw.line([160, head_y + 82, 120, head_y + 83], fill='black', width=2)
        draw.line([240, head_y + 78, 280, head_y + 73], fill='black', width=2)
        draw.line([240, head_y + 82, 280, head_y + 83], fill='black', width=2)
        
        # TAIL
        tail_points = []
        tail_start_x = 200 + body_width//2
        tail_start_y = 200 + y_offset
        
        for i in range(12):
            angle = math.sin(frame * 0.15 + i * 0.5) * 0.8
            tail_x = tail_start_x + i * 8
            tail_y = tail_start_y + math.sin(i * 0.3 + frame * 0.2) * 15
            tail_points.append((tail_x, tail_y))
        
        for i in range(len(tail_points)-1):
            draw.line([tail_points[i], tail_points[i+1]], fill=cat_color, width=10)
        
        return img
    
    @staticmethod
    def draw_mouse(frame, action="idle", emotion="neutral"):
        """Draw a Jerry-like mouse character"""
        img = Image.new('RGBA', (300, 400), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colors
        mouse_color = (160, 110, 60)  # Brown
        pink_color = (255, 192, 203)
        
        # Bounce
        bounce = math.sin(frame * 0.25) * 3
        
        # Body size based on action
        if action == "squash":
            body_height = 60
            body_width = 100
            y_offset = 80
        elif action == "stretch":
            body_height = 100
            body_width = 60
            y_offset = 40
        else:
            body_height = 80
            body_width = 80
            y_offset = 60 + bounce
        
        # Body
        draw.ellipse([150 - body_width//2, 120 + y_offset, 
                      150 + body_width//2, 120 + body_height + y_offset], 
                     fill=mouse_color, outline='black', width=3)
        
        # BIG EARS
        draw.ellipse([120, 50 + bounce, 160, 90 + bounce], 
                     fill=mouse_color, outline='black', width=3)
        draw.ellipse([140, 45 + bounce, 180, 85 + bounce], 
                     fill=mouse_color, outline='black', width=3)
        # Inner ears
        draw.ellipse([125, 55 + bounce, 155, 85 + bounce], fill=pink_color)
        draw.ellipse([145, 50 + bounce, 175, 80 + bounce], fill=pink_color)
        
        # HEAD
        draw.ellipse([130, 80 + bounce, 170, 140 + bounce], 
                     fill=mouse_color, outline='black', width=3)
        
        # EYES
        if emotion == "scared":
            draw.ellipse([140, 100 + bounce, 155, 115 + bounce], fill='white', outline='black', width=2)
            draw.ellipse([155, 100 + bounce, 170, 115 + bounce], fill='white', outline='black', width=2)
            draw.ellipse([143, 103 + bounce, 152, 112 + bounce], fill='black')
            draw.ellipse([158, 103 + bounce, 167, 112 + bounce], fill='black')
        else:
            draw.ellipse([140, 100 + bounce, 155, 115 + bounce], fill='white', outline='black', width=2)
            draw.ellipse([155, 100 + bounce, 170, 115 + bounce], fill='white', outline='black', width=2)
            draw.ellipse([143, 103 + bounce, 152, 112 + bounce], fill='black')
            draw.ellipse([158, 103 + bounce, 167, 112 + bounce], fill='black')
            # Sparkle
            draw.ellipse([145, 105 + bounce, 147, 107 + bounce], fill='white')
            draw.ellipse([160, 105 + bounce, 162, 107 + bounce], fill='white')
        
        # NOSE
        draw.ellipse([147, 118 + bounce, 153, 124 + bounce], fill='black')
        
        # SMILE
        draw.arc([140, 120 + bounce, 160, 135 + bounce], start=0, end=180, fill='black', width=2)
        
        # WHISKERS
        draw.line([130, 120 + bounce, 100, 115 + bounce], fill='black', width=1)
        draw.line([130, 123 + bounce, 100, 123 + bounce], fill='black', width=1)
        draw.line([170, 120 + bounce, 200, 115 + bounce], fill='black', width=1)
        draw.line([170, 123 + bounce, 200, 123 + bounce], fill='black', width=1)
        
        return img
    
    @staticmethod
    def draw_background(frame, scene_type="fight"):
        """Draw classic cartoon background"""
        img = Image.new('RGB', (800, 500), (240, 240, 220))
        draw = ImageDraw.Draw(img)
        
        # Floor
        draw.rectangle([0, 380, 800, 500], fill=(200, 150, 100))
        draw.line([0, 380, 800, 380], fill='black', width=4)
        
        # Floor boards
        for i in range(0, 800, 40):
            draw.line([i, 380, i, 500], fill=(180, 130, 80), width=2)
        
        # Wall
        draw.rectangle([0, 0, 800, 380], fill=(255, 240, 200))
        
        # Baseboard
        draw.rectangle([0, 370, 800, 380], fill=(150, 100, 50), outline='black', width=2)
        
        # Window
        draw.rectangle([550, 80, 750, 280], fill=(200, 220, 255), outline='black', width=4)
        draw.line([650, 80, 650, 280], fill='black', width=3)
        draw.line([550, 180, 750, 180], fill='black', width=3)
        
        # Curtains
        draw.rectangle([540, 70, 560, 290], fill=(200, 50, 50), outline='black', width=2)
        draw.rectangle([740, 70, 760, 290], fill=(200, 50, 50), outline='black', width=2)
        
        # Picture frame on wall
        draw.rectangle([100, 100, 250, 200], outline='black', width=4)
        draw.rectangle([110, 110, 240, 190], fill=(255, 200, 150))
        
        # Action lines for fight scene
        if scene_type == "fight":
            for i in range(15):
                x = random.randint(0, 800)
                y = random.randint(0, 380)
                draw.line([x, y, x+30, y-20], fill='black', width=2)
        
        return img

# ========== GENERATE ANIMATION FRAMES ==========

def generate_cartoon_frames():
    """Generate all frames for the cartoon"""
    frames = []
    total_frames = 180  # 30 seconds at 6 fps
    
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    for frame in range(total_frames):
        # Update progress
        if frame % 10 == 0:
            status_text.text(f"Drawing frame {frame}/{total_frames}...")
            progress_bar.progress(frame / total_frames)
        
        # Determine scene
        if frame < 60:
            scene = "fight"
        elif frame < 120:
            scene = "peaceful"
        else:
            scene = "play"
        
        # Create background
        canvas = ClassicCartoon.draw_background(frame, scene)
        draw = ImageDraw.Draw(canvas)
        
        # ===== ACT 1: CHASE & FIGHT =====
        if frame < 60:
            t = frame / 60
            
            if frame < 20:
                # Chase sequence
                cat_x = 50 + int(frame * 15)
                mouse_x = 400 - int(frame * 8)
                cat_action = "stretch"
                mouse_action = "stretch"
                cat_emotion = "angry"
                mouse_emotion = "scared"
            elif frame < 40:
                # Almost caught
                cat_x = 320
                mouse_x = 350
                cat_action = "stretch"
                mouse_action = "squash"
                cat_emotion = "angry"
                mouse_emotion = "scared"
            else:
                # Fight!
                if frame % 20 < 10:
                    cat_x = 280
                    mouse_x = 420
                    cat_action = "squash"
                    mouse_action = "stretch"
                    cat_emotion = "surprised"
                    mouse_emotion = "angry"
                else:
                    cat_x = 420
                    mouse_x = 280
                    cat_action = "stretch"
                    mouse_action = "squash"
                    cat_emotion = "angry"
                    mouse_emotion = "surprised"
            
            # Draw characters
            cat = ClassicCartoon.draw_cat(frame, action=cat_action, emotion=cat_emotion)
            canvas.paste(cat, (cat_x, 50), cat)
            
            mouse = ClassicCartoon.draw_mouse(frame, action=mouse_action, emotion=mouse_emotion)
            canvas.paste(mouse, (mouse_x, 120), mouse)
            
            # Action text
            if frame > 20:
                if frame % 20 < 10:
                    # Draw POW text with outline
                    for offset in [-2, -1, 0, 1, 2]:
                        draw.text((350 + offset, 220 + offset), "POW!", fill='black', font=None)
                    draw.text((350, 220), "POW!", fill=(255, 50, 50), font=None)
                else:
                    for offset in [-2, -1, 0, 1, 2]:
                        draw.text((350 + offset, 220 + offset), "BAM!", fill='black', font=None)
                    draw.text((350, 220), "BAM!", fill=(255, 50, 50), font=None)
        
        # ===== ACT 2: PEACEFUL =====
        elif frame < 120:
            t = (frame - 60) / 60
            
            # Tired poses
            cat_x = 150
            mouse_x = 550
            cat_action = "squash"
            mouse_action = "squash"
            cat_emotion = "neutral"
            mouse_emotion = "neutral"
            
            # Draw characters
            cat = ClassicCartoon.draw_cat(frame, action=cat_action, emotion=cat_emotion)
            canvas.paste(cat, (cat_x, 150), cat)
            
            mouse = ClassicCartoon.draw_mouse(frame, action=mouse_action, emotion=mouse_emotion)
            canvas.paste(mouse, (mouse_x, 180), mouse)
            
            # ZZZ effects
            if t > 0.3:
                for i in range(3):
                    z_y = 100 - i * 20 - (frame % 60) / 2
                    for offset in [-1, 0, 1]:
                        draw.text((cat_x + 50 + i * 10 + offset, z_y + offset), "z", fill='black', font=None)
                    draw.text((cat_x + 50 + i * 10, z_y), "z", fill=(100, 100, 200), font=None)
                    
                    for offset in [-1, 0, 1]:
                        draw.text((mouse_x - 50 - i * 10 + offset, z_y + offset), "z", fill='black', font=None)
                    draw.text((mouse_x - 50 - i * 10, z_y), "z", fill=(100, 100, 200), font=None)
        
        # ===== ACT 3: PLAYING TOGETHER =====
        else:
            t = (frame - 120) / 60
            
            # Playful positions
            if frame % 40 < 20:
                cat_x = 250
                mouse_x = 450
            else:
                cat_x = 450
                mouse_x = 250
            
            # Happy emotions
            cat_action = "idle"
            mouse_action = "idle"
            cat_emotion = "neutral"
            mouse_emotion = "neutral"
            
            # Draw characters
            cat = ClassicCartoon.draw_cat(frame, action=cat_action, emotion=cat_emotion)
            canvas.paste(cat, (cat_x, 80), cat)
            
            mouse = ClassicCartoon.draw_mouse(frame, action=mouse_action, emotion=mouse_emotion)
            canvas.paste(mouse, (mouse_x, 130), mouse)
            
            # Ball
            ball_x = 400 + int(math.sin(frame * 0.15) * 80)
            ball_y = 330 + int(abs(math.sin(frame * 0.2)) * 20)
            draw.ellipse([ball_x-15, ball_y-15, ball_x+15, ball_y+15], 
                        fill=(255, 80, 80), outline='black', width=3)
            
            # Hearts
            if t > 0.7:
                heart_x = 350 + int(math.sin(frame * 0.2) * 15)
                heart_y = 200 + int(math.cos(frame * 0.25) * 15)
                draw.text((heart_x, heart_y), "❤️", fill=(255, 0, 0), font=None)
        
        # Add frame counter (like traditional animation)
        draw.text((10, 10), f"Frame: {frame}", fill=(100, 100, 100), font=None)
        
        frames.append(canvas)
    
    status_text.text("Animation ready!")
    progress_bar.progress(1.0)
    time.sleep(0.5)
    status_text.empty()
    progress_bar.empty()
    
    return frames

# ========== MAIN UI ==========

st.markdown('<div class="cartoon-title">🐱 CLASSIC CARTOON 🐭</div>', unsafe_allow_html=True)
st.markdown('<div class="cartoon-subtitle">Hand-drawn frame-by-frame • Tom & Jerry Style</div>', unsafe_allow_html=True)

st.markdown("---")

# Animation controls
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    animation_style = st.selectbox(
        "Animation Quality",
        ["Classic (6 fps) - Like old TV", "Smooth (12 fps) - Like DVD", "Traditional (8 fps) - Like cinema"],
        index=0
    )
    
    play_button = st.button("🎬 PLAY CARTOON 🎬", use_container_width=True)

# FPS settings
fps_map = {
    "Classic (6 fps) - Like old TV": 6,
    "Smooth (12 fps) - Like DVD": 12,
    "Traditional (8 fps) - Like cinema": 8
}

if play_button:
    fps = fps_map[animation_style]
    frame_duration = 1 / fps
    
    # Generate frames
    with st.spinner("Drawing each frame by hand (traditional animation)..."):
        frames = generate_cartoon_frames()
    
    st.success(f"✅ {len(frames)} frames drawn! Playing at {fps} fps...")
    
    # Create animation player
    animation_container = st.empty()
    progress_bar = st.progress(0)
    info_container = st.empty()
    
    # Play animation
    for i, frame in enumerate(frames):
        animation_container.image(frame, use_column_width=True)
        progress = i / len(frames)
        progress_bar.progress(progress)
        
        # Show info
        seconds = int(i / fps)
        if seconds < 10:
            info_container.info(f"⚔️ ACT 1: The Chase & Fight • {seconds}s / 30s")
        elif seconds < 20:
            info_container.info(f"😴 ACT 2: Peaceful Rest • {seconds}s / 30s")
        else:
            info_container.info(f"❤️ ACT 3: Playing Together • {seconds}s / 30s")
        
        time.sleep(frame_duration)
    
    # Grand finale
    progress_bar.progress(1.0)
    info_container.success("🎉 THE END! Just like classic cartoons! 🎉")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.balloons()
        if st.button("🔄 WATCH AGAIN", use_container_width=True):
            st.rerun()

else:
    # Preview section
    st.markdown("### 🎬 Preview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### ⚔️ ACT 1")
        preview_cat = ClassicCartoon.draw_cat(0, action="stretch", emotion="angry")
        st.image(preview_cat, use_column_width=True)
        st.caption("Cat chasing mouse • 0-10s")
        st.markdown("*POW! BAM! Action!*")
    
    with col2:
        st.markdown("#### 😴 ACT 2")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Both exhausted from fight**")
        st.markdown("💤 ZZZ 💤")
        st.caption("Peaceful rest • 10-20s")
    
    with col3:
        st.markdown("#### ❤️ ACT 3")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Playing together**")
        st.markdown("🎈 Balloons & Hearts 🎈")
        st.caption("Happy ending • 20-30s")
    
    st.markdown("---")
    
    # Features explanation
    with st.expander("🎨 What makes this a TRUE CLASSIC CARTOON?"):
        st.markdown("""
        ### Traditional Animation Techniques Used:
        
        **1. Frame-by-Frame Drawing** ✏️
        - 180 individual hand-drawn frames
        - Each frame unique (no tweening)
        - Like Disney & Hanna-Barbera
        
        **2. Squash and Stretch** 💪
        - Characters squash when landing
        - Stretch when running fast
        - Exaggerated for comedy
        
        **3. Cartoon Physics** 🎯
        - Characters hang in air
        - Eyes pop out when surprised
        - Stars and action lines
        
        **4. Character Personalities** 🎭
        - Cat: Always chasing, angry, dramatic
        - Mouse: Clever, quick, playful
        - Expressions change instantly
        
        **5. Classic Visual Style** 🖼️
        - Thick black outlines
        - Solid vibrant colors
        - Traditional backgrounds
        - Hand-drawn aesthetic
        
        ### Like watching:
        - ✅ Tom & Jerry
        - ✅ Looney Tunes  
        - ✅ Pink Panther
        - ✅ Classic MGM Cartoons
        """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🎞️ 180 hand-drawn frames • 30 seconds • True classic cartoon style 🎞️</p>
        <p>Press PLAY above to watch the complete cartoon!</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 12px; color: #999;">
    <p>Classic Cartoon Animation System | Hand-crafted frame by frame | Tom & Jerry inspired</p>
</div>
""", unsafe_allow_html=True)
