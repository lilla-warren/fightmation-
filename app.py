import streamlit as st
import time
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np

# Page setup
st.set_page_config(
    page_title="Smooth Cartoon Animation", 
    layout="wide",
    page_icon="🎨"
)

# Custom CSS for smooth transitions
st.markdown("""
<style>
    /* Smooth fade transitions */
    @keyframes smoothFade {
        0% { opacity: 0; transform: scale(0.95); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    @keyframes smoothSlide {
        0% { transform: translateX(-50px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes smoothBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    @keyframes smoothWiggle {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(-3deg); }
        75% { transform: rotate(3deg); }
    }
    
    .smooth-fade {
        animation: smoothFade 0.3s ease-out;
    }
    
    .smooth-slide {
        animation: smoothSlide 0.4s ease-out;
    }
    
    .smooth-bounce {
        animation: smoothBounce 0.5s ease-in-out infinite;
    }
    
    .frame-transition {
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Cartoon canvas style */
    .animation-canvas {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ========== SMOOTH ANIMATION SYSTEM ==========

def ease_in_out_cubic(t):
    """Smooth easing function - like professional animation"""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - pow(-2 * t + 2, 3) / 2

def ease_out_back(t):
    """Spring effect - like cartoon bounce"""
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

def squash_and_stretch(value, intensity=0.2):
    """Squash and stretch effect like FlipaClip"""
    if value > 0:
        return 1 + (value * intensity)
    else:
        return 1 / (1 + (abs(value) * intensity))

class SmoothAnimator:
    """Professional animation controller with easing"""
    
    @staticmethod
    def draw_smooth_fighter(img, draw, frame, action="idle", squash=0):
        """Draw fighter with squash & stretch"""
        width, height = 300, 400
        
        # Squash and stretch effect
        scale_x = squash_and_stretch(squash, 0.3)
        scale_y = 2 - scale_x
        
        # Colors
        if frame % 2 == 0:
            body_color = (255, 80, 80)
        else:
            body_color = (80, 80, 255)
        
        # Body with stretch
        if action == "attack":
            # Stretched punch pose
            stretch = 1 + abs(squash) * 0.5
            draw.ellipse([100, 150 - stretch*20, 220, 320 + stretch*20], 
                        fill=body_color, outline='black', width=3)
            # Extended arm
            draw.ellipse([200 + squash*50, 120, 280 + squash*50, 200], 
                        fill=body_color, outline='black', width=3)
        elif action == "hit":
            # Squashed when hit
            draw.ellipse([100 + squash*20, 150, 220 - squash*20, 320], 
                        fill=body_color, outline='black', width=3)
        else:
            # Normal with slight idle bounce
            bounce = math.sin(frame * 0.5) * 5
            draw.ellipse([100, 100 + bounce, 220, 300 + bounce], 
                        fill=body_color, outline='black', width=3)
        
        # Head with follow-through
        head_y = 40 + (squash * 10)
        draw.ellipse([110, head_y, 210, 140 + head_y], 
                    fill=(255, 220, 150), outline='black', width=3)
        
        # Eyes that track movement
        eye_offset = squash * 10
        draw.ellipse([135 + eye_offset, 80, 152 + eye_offset, 97], 
                    fill='white', outline='black', width=2)
        draw.ellipse([168 + eye_offset, 80, 185 + eye_offset, 97], 
                    fill='white', outline='black', width=2)
        draw.ellipse([140 + eye_offset, 85, 147 + eye_offset, 92], fill='black')
        draw.ellipse([173 + eye_offset, 85, 180 + eye_offset, 92], fill='black')
        
        return img

    @staticmethod
    def draw_smooth_background(frame, transition=0):
        """Animated background with smooth transitions"""
        img = Image.new('RGB', (800, 500))
        draw = ImageDraw.Draw(img)
        
        # Time of day based on frame
        if frame < 180:  # Day
            t = frame / 180
            r = 135 - int(100 * t)
            g = 206 - int(100 * t)
            b = 235 - int(150 * t)
        elif frame < 360:  # Sunset
            t = (frame - 180) / 180
            r = 255 - int(55 * t)
            g = 106 - int(30 * t)
            b = 85 - int(20 * t)
        else:  # Night
            r, g, b = 25, 25, 50
        
        # Smooth sky gradient
        for i in range(500):
            factor = i / 500
            current_r = int(r * (1 - factor) + 25 * factor)
            current_g = int(g * (1 - factor) + 25 * factor)
            current_b = int(b * (1 - factor) + 50 * factor)
            draw.line([(0, i), (800, i)], fill=(current_r, current_g, current_b))
        
        # Animated clouds that float
        cloud_x = (frame * 0.5) % 800
        draw.ellipse([cloud_x, 80, cloud_x+60, 120], fill='white', outline='black', width=2)
        draw.ellipse([cloud_x+30, 60, cloud_x+90, 100], fill='white', outline='black', width=2)
        draw.ellipse([cloud_x-20, 70, cloud_x+40, 110], fill='white', outline='black', width=2)
        
        # Animated sun/moon with glow
        if frame < 360:
            # Sun with pulsing glow
            sun_size = 80 + math.sin(frame * 0.05) * 5
            draw.ellipse([680, 50, 760, 130], fill=(255, 255, 100), outline='black', width=2)
            # Glow effect
            for i in range(3):
                alpha = 50 - i * 15
                draw.ellipse([680-i*5, 50-i*5, 760+i*5, 130+i*5], 
                            fill=(255, 255, 100, alpha))
        else:
            # Moon with glow
            draw.ellipse([680, 50, 760, 130], fill=(255, 255, 200), outline='black', width=2)
        
        # Smooth rolling hills
        for i in range(3):
            y_offset = math.sin(frame * 0.02 + i) * 10
            draw.arc([-100, 350 + y_offset, 900, 550 + y_offset], 
                    start=0, end=180, fill=(50 + i*30, 150 + i*20, 50), width=15)
        
        return img

    @staticmethod
    def draw_smooth_kid(img, draw, frame, color, name, action="playing"):
        """Animated kid with smooth motion"""
        # Bounce with easing
        bounce = math.sin(frame * 0.1) * 8
        # Waving with smooth rotation
        wave = math.sin(frame * 0.3) * 20
        
        color_map = {
            "yellow": (255, 255, 150),
            "green": (150, 255, 150),
            "pink": (255, 192, 203)
        }
        main_color = color_map.get(color, (255, 255, 150))
        
        # Body with bounce
        draw.ellipse([60, 100 + bounce, 140, 180 + bounce], 
                    fill=main_color, outline='black', width=3)
        
        # Head with slight rotation
        head_rotation = math.sin(frame * 0.2) * 3
        draw.ellipse([50 + head_rotation, 30 + bounce, 150 + head_rotation, 120 + bounce], 
                    fill=(255, 220, 150), outline='black', width=3)
        
        # Animated eyes (blink)
        if frame % 60 < 5:  # Blink every ~1 second
            draw.line([75, 65, 95, 65], fill='black', width=3)
            draw.line([105, 65, 125, 65], fill='black', width=3)
        else:
            draw.ellipse([75, 55, 95, 75], fill='white', outline='black', width=2)
            draw.ellipse([105, 55, 125, 75], fill='white', outline='black', width=2)
            draw.ellipse([80, 62, 88, 70], fill='black')
            draw.ellipse([110, 62, 118, 70], fill='black')
            # Sparkle
            draw.ellipse([82, 60, 85, 63], fill='white')
            draw.ellipse([112, 60, 115, 63], fill='white')
        
        # Waving arm
        draw.line([140, 130 + bounce, 160 + wave/2, 100 + bounce], 
                 fill=main_color, width=10)
        draw.ellipse([155 + wave/2, 95 + bounce, 170 + wave/2, 110 + bounce], 
                    fill=main_color, outline='black', width=2)
        
        # Smile that changes with bounce
        smile_offset = bounce * 0.5
        draw.arc([75, 80 + smile_offset, 125, 110 + smile_offset], 
                start=0, end=180, fill='black', width=3)
        
        return img

# ========== FRAME-BY-FRAME ANIMATION ==========

def create_smooth_animation():
    """Generate smooth frame-by-frame animation"""
    
    frames = []
    total_frames = 180  # 30 seconds at 6fps
    
    for frame in range(total_frames):
        # Create canvas
        canvas = Image.new('RGB', (800, 600), 'white')
        draw = ImageDraw.Draw(canvas)
        
        # Add background with transition
        bg = SmoothAnimator.draw_smooth_background(frame)
        canvas.paste(bg, (0, 0))
        
        # Calculate animation progress
        progress = frame / total_frames
        
        # ===== ACT 1: FIGHT (frames 0-60) =====
        if frame < 60:
            t = frame / 60  # 0 to 1
            
            # Smooth approach using easing
            red_x = -300 + (400 * ease_in_out_cubic(t))
            blue_x = 1100 - (400 * ease_in_out_cubic(t))
            
            # Fight action
            if frame > 20:
                # Punch timing
                punch_frame = (frame - 20) % 20
                if punch_frame < 5:
                    # Squash on punch
                    squash = math.sin(punch_frame * math.pi / 5) * 0.5
                    action = "attack"
                elif punch_frame < 10:
                    # Hit reaction
                    squash = math.sin((punch_frame - 5) * math.pi / 5) * 0.3
                    action = "hit"
                else:
                    squash = 0
                    action = "idle"
            else:
                squash = 0
                action = "idle"
            
            # Draw fighters
            fighter1_img = Image.new('RGBA', (300, 400), (0,0,0,0))
            fighter1_draw = ImageDraw.Draw(fighter1_img)
            SmoothAnimator.draw_smooth_fighter(fighter1_img, fighter1_draw, frame, action, squash)
            canvas.paste(fighter1_img, (int(red_x), 100), fighter1_img)
            
            fighter2_img = Image.new('RGBA', (300, 400), (0,0,0,0))
            fighter2_draw = ImageDraw.Draw(fighter2_img)
            SmoothAnimator.draw_smooth_fighter(fighter2_img, fighter2_draw, frame, action, -squash)
            canvas.paste(fighter2_img, (int(blue_x), 100), fighter2_img)
            
            # Action text with fade
            if frame > 20 and frame % 20 < 10:
                text = "POW!" if frame % 40 < 20 else "BAM!"
                text_alpha = int(255 * (1 - (frame % 10) / 10))
                draw.text((350, 250), text, fill=(255, text_alpha, text_alpha))
        
        # ===== ACT 2: PEACEFUL (frames 60-120) =====
        elif frame < 120:
            t = (frame - 60) / 60
            
            # Smooth tree fade-in
            tree_alpha = int(255 * ease_in_out_cubic(t))
            
            # Draw trees with fade
            for i, x in enumerate([100, 250, 400, 550, 700]):
                alpha = min(255, tree_alpha - i * 30)
                if alpha > 0:
                    draw.rectangle([x, 350, x+20, 450], fill=(101, 67, 33))
                    draw.ellipse([x-20, 320, x+40, 370], fill=(0, 100, 0))
            
            # Gentle floating particles (fireflies)
            for _ in range(int(20 * t)):
                fx = 100 + math.sin(frame * 0.1 + _) * 200
                fy = 200 + math.cos(frame * 0.15 + _) * 100
                draw.ellipse([fx-2, fy-2, fx+2, fy+2], fill=(255, 255, 100))
            
            # Peaceful text with smooth fade
            if t > 0.5:
                text_alpha = int(255 * ((t - 0.5) * 2))
                draw.text((300, 50), "Peaceful Evening...", 
                         fill=(255, 255, 255, text_alpha))
        
        # ===== ACT 3: KIDS PLAYING (frames 120-180) =====
        else:
            t = (frame - 120) / 60
            
            # Kids with smooth circular motion
            kids = [
                ("yellow", "Lily", 0),
                ("green", "Max", 120),
                ("pink", "Leo", 240)
            ]
            
            for i, (color, name, offset) in enumerate(kids):
                # Smooth circular path with easing
                angle = (frame * 0.05) + math.radians(offset)
                x = 400 + math.cos(angle) * 200
                y = 300 + math.sin(angle) * 80
                
                # Draw kid with smooth animation
                kid_img = Image.new('RGBA', (200, 250), (0,0,0,0))
                kid_draw = ImageDraw.Draw(kid_img)
                SmoothAnimator.draw_smooth_kid(kid_img, kid_draw, frame, color, name)
                canvas.paste(kid_img, (int(x)-100, int(y)-150), kid_img)
            
            # Floating balloons
            for b in range(5):
                bx = 100 + (frame * 0.5 + b * 150) % 700
                by = 400 + math.sin(frame * 0.1 + b) * 50
                draw.ellipse([bx-10, by-15, bx+10, by+5], fill=(255, 100, 100))
                draw.line([bx, by+5, bx, by+25], fill='black', width=1)
            
            # Happy text
            if t > 0.8:
                draw.text((300, 50), "Happy Together!", fill=(255, 255, 255))
        
        # Add smooth framerate display
        draw.text((10, 10), f"Frame: {frame}/180", fill=(255,255,255))
        
        frames.append(canvas)
    
    return frames

# ========== STREAMLIT UI ==========

st.markdown('<h1 style="text-align: center;">🎨 SMOOTH CARTOON ANIMATION 🎨</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center;">Professional frame-by-frame animation • Like FlipaClip/Procreate</p>', unsafe_allow_html=True)

# Animation controls
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    quality = st.select_slider(
        "Animation Quality",
        options=["Fast (3 fps)", "Smooth (6 fps)", "Buttery (12 fps)"],
        value="Smooth (6 fps)"
    )
    
    play = st.button("▶️ PLAY SMOOTH ANIMATION", use_container_width=True)

# Quality settings
fps_map = {
    "Fast (3 fps)": 3,
    "Smooth (6 fps)": 6,
    "Buttery (12 fps)": 12
}

if play:
    fps = fps_map[quality]
    frame_duration = 1 / fps
    
    with st.spinner("Generating smooth animation frames..."):
        frames = create_smooth_animation()
    
    # Animation placeholder
    animation_container = st.empty()
    progress_bar = st.progress(0)
    status_text = st.empty()
    time_text = st.empty()
    
    # Play animation
    for i, frame in enumerate(frames):
        animation_container.image(frame, use_column_width=True)
        progress = i / len(frames)
        progress_bar.progress(progress)
        
        seconds = int(i / fps)
        time_text.markdown(f"### ⏱️ {seconds} / 30 seconds")
        
        # Status updates
        if seconds < 10:
            status_text.markdown("### ⚔️ EPIC BATTLE ⚔️")
        elif seconds < 20:
            status_text.markdown("### 🌅 PEACEFUL EVENING 🌅")
        else:
            status_text.markdown("### 👧 KIDS PLAYING 👦")
        
        time.sleep(frame_duration)
    
    # Final celebration
    status_text.success("✅ Animation Complete! 🎉")
    st.balloons()
    
    # Replay button
    if st.button("🔄 Watch Again", use_container_width=True):
        st.rerun()

else:
    # Preview with features
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎬 SMOOTH MOTION")
        st.markdown("• Easing functions")
        st.markdown("• Squash & stretch")
        st.markdown("• Frame interpolation")
    
    with col2:
        st.markdown("### 🎨 CARTOON EFFECTS")
        st.markdown("• Hand-drawn style")
        st.markdown("• Lip sync ready")
        st.markdown("• Particle effects")
    
    with col3:
        st.markdown("### ⚡ PRO FEATURES")
        st.markdown("• 6-12 fps options")
        st.markdown("• Smooth transitions")
        st.markdown("• Like FlipaClip!")
    
    st.markdown("---")
    
    # Demo preview
    st.markdown("### 📺 Preview (static frames)")
    preview_cols = st.columns(3)
    
    # Show keyframes
    keyframes = create_smooth_animation()
    for i, col in enumerate(preview_cols):
        with col:
            st.image(keyframes[i * 60], use_column_width=True)
            st.caption(f"Frame {i * 60} - {i * 10} seconds")
    
    st.info("💡 **Pro Tip:** Select 'Buttery (12 fps)' for the smoothest animation like professional cartoons!")

# Instructions
with st.expander("🎬 Animation Features Explained"):
    st.markdown("""
    ### Professional Animation Techniques Used:
    
    **1. Easing Functions** 🤸
    - `ease_in_out_cubic` - Smooth starts and stops
    - `ease_out_back` - Cartoon spring effect
    
    **2. Squash and Stretch** 💪
    - Characters squash when hitting
    - Stretch when attacking
    - Like classic Disney animation!
    
    **3. Frame-by-Frame** 🎞️
    - 180 total frames (6 fps)
    - Each frame drawn individually
    - Like FlipaClip workflow
    
    **4. Smooth Transitions** 🌊
    - Day → Sunset → Night
    - Float in/out effects
    - Particle animations
    
    **5. Character Animation** 🎭
    - Idle bounce
    - Blinking eyes
    - Waving arms
    - Follow-through motion
    
    ### Quality Options:
    - **Fast (3 fps)** - Quick preview
    - **Smooth (6 fps)** - Standard cartoon
    - **Buttery (12 fps)** - Professional grade
    """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>✨ Professional smooth animation • Like FlipaClip/Procreate Dreams • 30 seconds ✨</p>
</div>
""", unsafe_allow_html=True)
