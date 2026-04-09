import streamlit as st
import time
import math
import random
from PIL import Image, ImageDraw

# Page setup
st.set_page_config(
    page_title="Classic Cartoon - Tom & Jerry Style", 
    layout="wide",
    page_icon="🐱"
)

# Custom CSS
st.markdown("""
<style>
    @keyframes cartoonPop {
        0% { transform: scale(0); opacity: 0; }
        80% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .cartoon-title {
        font-family: 'Impact', 'Arial Black', sans-serif;
        text-shadow: 4px 4px 0px #FFD700;
        letter-spacing: 3px;
        font-size: 48px;
        text-align: center;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%);
        color: black;
        font-size: 24px;
        font-weight: bold;
        font-family: 'Impact', sans-serif;
        border: 3px solid black;
        border-radius: 50px;
        padding: 15px 30px;
    }
    
    div.stButton > button:hover {
        transform: scale(1.05);
        transition: all 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# ========== SIMPLIFIED CARTOON DRAWING FUNCTIONS ==========

def draw_cat(frame, x_pos, action="idle"):
    """Draw cat at specific position"""
    img = Image.new('RGBA', (150, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Simple bounce
    bounce = math.sin(frame * 0.2) * 3
    
    # Body
    if action == "stretch":
        draw.ellipse([50, 30 + bounce, 130, 140 + bounce], fill=(70, 130, 180), outline='black', width=2)
    elif action == "squash":
        draw.ellipse([40, 60 + bounce, 140, 130 + bounce], fill=(70, 130, 180), outline='black', width=2)
    else:
        draw.ellipse([50, 50 + bounce, 130, 140 + bounce], fill=(70, 130, 180), outline='black', width=2)
    
    # Head
    draw.ellipse([55, 20 + bounce, 125, 80 + bounce], fill=(70, 130, 180), outline='black', width=2)
    
    # Ears
    draw.polygon([(55, 30 + bounce), (65, 15 + bounce), (75, 35 + bounce)], fill=(70, 130, 180), outline='black', width=2)
    draw.polygon([(105, 30 + bounce), (115, 15 + bounce), (125, 35 + bounce)], fill=(70, 130, 180), outline='black', width=2)
    
    # Eyes
    draw.ellipse([70, 35 + bounce, 85, 50 + bounce], fill='white', outline='black', width=1)
    draw.ellipse([95, 35 + bounce, 110, 50 + bounce], fill='white', outline='black', width=1)
    draw.ellipse([75, 40 + bounce, 82, 47 + bounce], fill='black')
    draw.ellipse([100, 40 + bounce, 107, 47 + bounce], fill='black')
    
    # Nose and mouth
    draw.ellipse([87, 55 + bounce, 93, 61 + bounce], fill='pink', outline='black', width=1)
    draw.arc([80, 60 + bounce, 100, 75 + bounce], start=0, end=180, fill='black', width=1)
    
    return img

def draw_mouse(frame, x_pos, action="idle"):
    """Draw mouse at specific position"""
    img = Image.new('RGBA', (120, 150), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    bounce = math.sin(frame * 0.25) * 3
    
    # Body
    if action == "stretch":
        draw.ellipse([40, 20 + bounce, 100, 100 + bounce], fill=(160, 110, 60), outline='black', width=2)
    elif action == "squash":
        draw.ellipse([35, 40 + bounce, 105, 90 + bounce], fill=(160, 110, 60), outline='black', width=2)
    else:
        draw.ellipse([40, 30 + bounce, 100, 100 + bounce], fill=(160, 110, 60), outline='black', width=2)
    
    # Ears
    draw.ellipse([30, 10 + bounce, 55, 35 + bounce], fill=(160, 110, 60), outline='black', width=2)
    draw.ellipse([65, 10 + bounce, 90, 35 + bounce], fill=(160, 110, 60), outline='black', width=2)
    draw.ellipse([35, 15 + bounce, 50, 30 + bounce], fill=(255, 200, 200))
    draw.ellipse([70, 15 + bounce, 85, 30 + bounce], fill=(255, 200, 200))
    
    # Head
    draw.ellipse([45, 25 + bounce, 95, 65 + bounce], fill=(160, 110, 60), outline='black', width=2)
    
    # Eyes
    draw.ellipse([55, 35 + bounce, 65, 45 + bounce], fill='white', outline='black', width=1)
    draw.ellipse([75, 35 + bounce, 85, 45 + bounce], fill='white', outline='black', width=1)
    draw.ellipse([58, 38 + bounce, 62, 42 + bounce], fill='black')
    draw.ellipse([78, 38 + bounce, 82, 42 + bounce], fill='black')
    
    # Nose and smile
    draw.ellipse([67, 48 + bounce, 73, 54 + bounce], fill='black')
    draw.arc([60, 50 + bounce, 80, 60 + bounce], start=0, end=180, fill='black', width=1)
    
    return img

def draw_background(frame, scene):
    """Draw simple background"""
    img = Image.new('RGB', (800, 500), (255, 240, 200))
    draw = ImageDraw.Draw(img)
    
    # Floor
    draw.rectangle([0, 380, 800, 500], fill=(200, 150, 100))
    draw.line([0, 380, 800, 380], fill='black', width=3)
    
    # Simple window
    draw.rectangle([600, 100, 750, 250], fill=(200, 220, 255), outline='black', width=3)
    draw.line([675, 100, 675, 250], fill='black', width=2)
    draw.line([600, 175, 750, 175], fill='black', width=2)
    
    # Action lines for fight
    if scene == "fight":
        for i in range(10):
            x = random.randint(0, 800)
            draw.line([x, 0, x+20, 50], fill='black', width=2)
    
    return img

# ========== STREAMING ANIMATION ==========

st.markdown('<div class="cartoon-title">🐱 CLASSIC CARTOON 🐭</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center;">Tom & Jerry Style • Frame-by-Frame Animation</p>', unsafe_allow_html=True)

st.markdown("---")

# Animation controls
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    play = st.button("🎬 PLAY CARTOON 🎬", use_container_width=True)

if play:
    # Setup animation containers
    animation_container = st.empty()
    progress_bar = st.progress(0)
    status_text = st.empty()
    time_text = st.empty()
    
    total_frames = 180  # 30 seconds at 6fps
    fps = 6
    frame_duration = 1 / fps
    
    # Play each frame one by one
    for frame in range(total_frames):
        # Determine scene
        if frame < 60:
            scene = "fight"
            if frame < 20:
                # Chase
                cat_x = 50 + int(frame * 15)
                mouse_x = 400 - int(frame * 10)
                cat_action = "stretch"
                mouse_action = "stretch"
            elif frame < 40:
                # Almost caught
                cat_x = 350
                mouse_x = 370
                cat_action = "stretch"
                mouse_action = "squash"
            else:
                # Fight
                if frame % 20 < 10:
                    cat_x = 300
                    mouse_x = 450
                    cat_action = "squash"
                    mouse_action = "stretch"
                else:
                    cat_x = 450
                    mouse_x = 300
                    cat_action = "stretch"
                    mouse_action = "squash"
            
            action_text = "⚔️ FIGHT! ⚔️"
            
        elif frame < 120:
            scene = "peaceful"
            cat_x = 200
            mouse_x = 550
            cat_action = "squash"
            mouse_action = "squash"
            action_text = "😴 RESTING... 😴"
        else:
            scene = "play"
            if frame % 40 < 20:
                cat_x = 280
                mouse_x = 470
            else:
                cat_x = 470
                mouse_x = 280
            cat_action = "idle"
            mouse_action = "idle"
            action_text = "❤️ PLAYING TOGETHER! ❤️"
        
        # Draw frame
        canvas = draw_background(frame, scene)
        
        # Draw cat
        cat = draw_cat(frame, cat_x, cat_action)
        canvas.paste(cat, (cat_x, 250), cat)
        
        # Draw mouse
        mouse = draw_mouse(frame, mouse_x, mouse_action)
        canvas.paste(mouse, (mouse_x, 300), mouse)
        
        # Add action text
        draw = ImageDraw.Draw(canvas)
        if scene == "fight" and frame > 20:
            if frame % 20 < 10:
                draw.text((350, 150), "POW!", fill=(255, 0, 0))
            else:
                draw.text((350, 150), "BAM!", fill=(255, 0, 0))
        
        # Add ZZZ for peaceful scene
        if scene == "peaceful" and frame > 70:
            for i in range(3):
                z_y = 150 - i * 20
                draw.text((cat_x + 30, z_y), "z", fill=(100, 100, 200))
                draw.text((mouse_x - 30, z_y), "z", fill=(100, 100, 200))
        
        # Add hearts for play scene
        if scene == "play" and frame > 150:
            heart_x = 380 + int(math.sin(frame * 0.2) * 20)
            heart_y = 200 + int(math.cos(frame * 0.25) * 15)
            draw.text((heart_x, heart_y), "❤️", fill=(255, 0, 0))
        
        # Show frame
        animation_container.image(canvas, use_column_width=True)
        
        # Update progress
        seconds = int(frame / fps)
        progress = frame / total_frames
        progress_bar.progress(progress)
        time_text.markdown(f"### ⏱️ {seconds} / 30 seconds")
        
        if seconds < 10:
            status_text.info(f"⚔️ ACT 1: The Chase! ⚔️ ({seconds}s)")
        elif seconds < 20:
            status_text.info(f"😴 ACT 2: Peaceful Rest 😴 ({seconds}s)")
        else:
            status_text.info(f"❤️ ACT 3: New Friends! ❤️ ({seconds}s)")
        
        time.sleep(frame_duration)
    
    # Animation complete
    progress_bar.progress(1.0)
    status_text.success("🎉 THE END! Classic cartoon complete! 🎉")
    st.balloons()
    
    # Replay button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 WATCH AGAIN", use_container_width=True):
            st.rerun()

else:
    # Preview
    st.markdown("### 🎬 Ready to watch!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### ⚔️ ACT 1")
        st.markdown("**The Chase & Fight**")
        st.markdown("0-10 seconds")
        st.markdown("🐱 Cat chases mouse")
        st.markdown("POW! BAM!")
    
    with col2:
        st.markdown("#### 😴 ACT 2")
        st.markdown("**Peaceful Rest**")
        st.markdown("10-20 seconds")
        st.markdown("Both exhausted")
        st.markdown("ZZZ...")
    
    with col3:
        st.markdown("#### ❤️ ACT 3")
        st.markdown("**Playing Together**")
        st.markdown("20-30 seconds")
        st.markdown("New friendship")
        st.markdown("Balloons & hearts")
    
    st.markdown("---")
    st.info("💡 **Click the PLAY button above to watch the 30-second classic cartoon!**")
    
    st.markdown("""
    ### 🎨 Features:
    - ✅ **Frame-by-frame animation** (180 frames)
    - ✅ **Squash and stretch** effects
    - ✅ **Classic cartoon physics**
    - ✅ **POW! BAM! action text**
    - ✅ **Smooth streaming playback**
    - ✅ **No memory issues**
    """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999;">
    <p>🐱 Classic Cartoon Animation • 30 seconds • Hand-drawn style • Tom & Jerry inspired 🐭</p>
</div>
""", unsafe_allow_html=True)
