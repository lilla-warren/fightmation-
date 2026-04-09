import streamlit as st
import time
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io

# Page setup
st.set_page_config(
    page_title="Cartoon Adventure - 30 Second Animation", 
    layout="wide",
    page_icon="🎨"
)

# Custom CSS for cartoon styling
st.markdown("""
<style>
    /* Cartoon-style background */
    .stApp {
        background: linear-gradient(135deg, #87CEEB 0%, #FFE4B5 100%);
    }
    
    /* Cartoon text bounce animation */
    @keyframes cartoonBounce {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(-2deg); }
    }
    
    @keyframes wiggle {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(-5deg); }
        75% { transform: rotate(5deg); }
    }
    
    .cartoon-text {
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Comic Neue', cursive;
        animation: cartoonBounce 0.5s ease-in-out;
    }
    
    .speech-bubble {
        position: relative;
        background: white;
        border-radius: 40px;
        padding: 20px;
        margin: 20px;
        border: 3px solid black;
        font-family: 'Comic Sans MS', cursive;
        font-weight: bold;
    }
    
    .speech-bubble:before {
        content: '';
        position: absolute;
        bottom: -20px;
        left: 20px;
        border-width: 20px 20px 0 0;
        border-style: solid;
        border-color: white transparent transparent transparent;
    }
    
    .cartoon-button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%);
        border: 3px solid black;
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 24px;
        font-weight: bold;
        font-family: 'Comic Sans MS', cursive;
        transition: transform 0.2s;
    }
    
    .cartoon-button:hover {
        transform: scale(1.05);
        cursor: pointer;
    }
    
    /* Cartoon panel styling */
    .cartoon-panel {
        background: white;
        border: 4px solid black;
        border-radius: 20px;
        padding: 20px;
        margin: 10px;
        box-shadow: 10px 10px 0 rgba(0,0,0,0.1);
    }
    
    /* Action lines */
    .action-lines {
        position: relative;
        overflow: hidden;
    }
    
    .action-lines:after {
        content: '';
        position: absolute;
        top: -10px;
        right: -10px;
        width: 50px;
        height: 50px;
        background: radial-gradient(circle, yellow, transparent);
        animation: wiggle 0.3s infinite;
    }
</style>
""", unsafe_allow_html=True)

# ========== CARTOON CHARACTER FUNCTIONS ==========

def draw_cartoon_fighter(color, expression="angry", action="idle"):
    """Draw a cartoon-style fighter character"""
    img = Image.new('RGBA', (300, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if color == "red":
        body_color = (255, 80, 80)
        name = "Rex"
    else:
        body_color = (80, 80, 255)
        name = "Blu"
    
    # Cartoon body (rounded, exaggerated)
    if action == "attack":
        # Stretching punch pose
        draw.ellipse([100, 150, 220, 320], fill=body_color, outline='black', width=3)
        draw.ellipse([200, 120, 280, 200], fill=body_color, outline='black', width=3)  # Punching arm
        # Action lines
        for i in range(5):
            draw.line([280 + i*5, 150, 300 + i*5, 150], fill='black', width=3)
    elif action == "hurt":
        # Hurt pose
        draw.ellipse([90, 160, 210, 330], fill=body_color, outline='black', width=3)
        # Stars around head (cartoon hurt effect)
        for i in range(3):
            draw.text((80 + i*30, 80), "★", fill=(255, 215, 0), font=None)
    else:
        # Normal standing
        draw.ellipse([100, 100, 220, 300], fill=body_color, outline='black', width=3)
        draw.ellipse([60, 200, 100, 260], fill=body_color, outline='black', width=3)
        draw.ellipse([220, 200, 260, 260], fill=body_color, outline='black', width=3)
    
    # Cartoon head (big and expressive)
    draw.ellipse([110, 40, 210, 140], fill=(255, 220, 150), outline='black', width=3)
    
    # Eyes (cartoon style)
    if expression == "angry":
        # Angry eyebrows
        draw.line([125, 80, 150, 90], fill='black', width=4)
        draw.line([195, 80, 170, 90], fill='black', width=4)
        # Small angry eyes
        draw.ellipse([135, 85, 150, 100], fill='white', outline='black', width=2)
        draw.ellipse([170, 85, 185, 100], fill='white', outline='black', width=2)
        draw.ellipse([140, 90, 147, 97], fill='black')
        draw.ellipse([173, 90, 180, 97], fill='black')
    elif expression == "happy":
        # Happy eyes (curved)
        draw.arc([130, 85, 155, 105], start=0, end=180, fill='black', width=3)
        draw.arc([165, 85, 190, 105], start=0, end=180, fill='black', width=3)
        # Big smile
        draw.arc([140, 100, 180, 130], start=0, end=180, fill='black', width=3)
    else:
        # Normal eyes
        draw.ellipse([135, 80, 152, 97], fill='white', outline='black', width=2)
        draw.ellipse([168, 80, 185, 97], fill='white', outline='black', width=2)
        draw.ellipse([140, 85, 147, 92], fill='black')
        draw.ellipse([173, 85, 180, 92], fill='black')
    
    # Mouth
    if expression == "angry":
        draw.arc([140, 110, 180, 135], start=180, end=360, fill='black', width=3)
    else:
        draw.arc([145, 105, 175, 125], start=0, end=180, fill='black', width=2)
    
    # Cartoon hair
    draw.ellipse([120, 20, 200, 60], fill=(50, 50, 50), outline='black', width=2)
    
    # Name tag
    draw.rectangle([120, 310, 200, 340], fill='white', outline='black', width=2)
    draw.text((135, 315), name, fill='black', font=None)
    
    return img

def draw_cartoon_background(time_of_day="day", weather="clear"):
    """Draw cartoon-style background"""
    img = Image.new('RGB', (800, 500), (135, 206, 235))
    draw = ImageDraw.Draw(img)
    
    if time_of_day == "sunset":
        # Sunset gradient
        for i in range(500):
            r = 255 - int(i * 0.3)
            g = 140 - int(i * 0.2)
            b = 100 - int(i * 0.1)
            draw.line([(0, i), (800, i)], fill=(r, g, b))
    elif time_of_day == "night":
        # Night sky
        for i in range(500):
            r = 25 - int(i * 0.05)
            g = 25 - int(i * 0.05)
            b = 50 - int(i * 0.05)
            draw.line([(0, i), (800, i)], fill=(r, g, b))
    else:
        # Day sky
        for i in range(500):
            r = 135 - int(i * 0.1)
            g = 206 - int(i * 0.1)
            b = 235 - int(i * 0.1)
            draw.line([(0, i), (800, i)], fill=(r, g, b))
    
    # Cartoon clouds
    cloud_positions = [(100, 80), (400, 50), (650, 100)]
    for x, y in cloud_positions:
        draw.ellipse([x, y, x+60, y+40], fill='white', outline='black', width=2)
        draw.ellipse([x+30, y-20, x+90, y+20], fill='white', outline='black', width=2)
        draw.ellipse([x-20, y-10, x+40, y+30], fill='white', outline='black', width=2)
    
    # Cartoon sun or moon
    if time_of_day == "night":
        draw.ellipse([680, 50, 760, 130], fill=(255, 255, 200), outline='black', width=2)
        # Cartoon moon face
        draw.ellipse([705, 75, 720, 90], fill=(200, 200, 150))
        draw.arc([700, 85, 725, 105], start=0, end=180, fill='black', width=2)
    else:
        draw.ellipse([680, 50, 760, 130], fill=(255, 255, 100), outline='black', width=2)
        # Sun rays
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1 = 720 + int(50 * math.cos(rad))
            y1 = 90 + int(50 * math.sin(rad))
            x2 = 720 + int(70 * math.cos(rad))
            y2 = 90 + int(70 * math.sin(rad))
            draw.line([(x1, y1), (x2, y2)], fill='yellow', width=3)
    
    # Cartoon ground (curved, like a storybook)
    draw.arc([-100, 350, 900, 550], start=0, end=180, fill=(50, 150, 50), width=10)
    draw.rectangle([0, 450, 800, 500], fill=(34, 139, 34), outline='black', width=2)
    
    # Cartoon flowers
    for i in range(8):
        x = 50 + i * 100
        draw.ellipse([x, 440, x+10, 450], fill='green', outline='black', width=1)
        draw.ellipse([x-3, 435, x+3, 445], fill=(255, 100, 100))
        draw.ellipse([x+2, 435, x+8, 445], fill=(255, 100, 100))
        draw.ellipse([x-1, 432, x+5, 442], fill=(255, 100, 100))
    
    return img

def draw_cartoon_kid(color, name, action="playing"):
    """Draw cartoon-style kid characters"""
    img = Image.new('RGBA', (200, 250), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color_map = {
        "yellow": (255, 255, 150),
        "green": (150, 255, 150),
        "pink": (255, 192, 203)
    }
    
    main_color = color_map.get(color, (255, 255, 150))
    
    # Cartoon body (small and cute)
    draw.ellipse([60, 100, 140, 180], fill=main_color, outline='black', width=3)
    
    # Cartoon head (big head, small body - classic cartoon)
    draw.ellipse([50, 30, 150, 120], fill=(255, 220, 150), outline='black', width=3)
    
    # Big cartoon eyes
    draw.ellipse([75, 55, 95, 75], fill='white', outline='black', width=2)
    draw.ellipse([105, 55, 125, 75], fill='white', outline='black', width=2)
    draw.ellipse([80, 62, 88, 70], fill='black')
    draw.ellipse([110, 62, 118, 70], fill='black')
    
    # Eye highlights (cartoon sparkle)
    draw.ellipse([82, 60, 85, 63], fill='white')
    draw.ellipse([112, 60, 115, 63], fill='white')
    
    # Big cartoon smile
    draw.arc([75, 80, 125, 110], start=0, end=180, fill='black', width=3)
    
    # Rosy cheeks
    draw.ellipse([70, 85, 85, 100], fill=(255, 150, 150))
    draw.ellipse([115, 85, 130, 100], fill=(255, 150, 150))
    
    # Cartoon hair
    draw.ellipse([60, 20, 140, 50], fill=(100, 50, 20), outline='black', width=2)
    
    # Arms
    if action == "waving":
        # Waving arm
        draw.line([140, 130, 170, 100], fill=main_color, width=8)
        draw.ellipse([160, 90, 180, 110], fill=main_color, outline='black', width=2)
        # Action lines for waving
        for i in range(3):
            draw.line([175 + i*5, 95, 180 + i*5, 100], fill='black', width=2)
    else:
        draw.line([130, 130, 160, 160], fill=main_color, width=8)
        draw.ellipse([155, 155, 170, 170], fill=main_color, outline='black', width=2)
    
    # Legs
    draw.line([80, 180, 70, 210], fill=main_color, width=8)
    draw.line([120, 180, 130, 210], fill=main_color, width=8)
    
    # Name tag
    draw.rectangle([70, 200, 130, 220], fill='white', outline='black', width=2)
    draw.text((80, 202), name, fill='black', font=None)
    
    return img

# ========== MAIN ANIMATION ==========

st.markdown('<h1 class="cartoon-text" style="text-align: center;">🎨 CARTOON ADVENTURE 🎨</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 20px;">A 30-Second Animated Cartoon Short</p>', unsafe_allow_html=True)

# Animation placeholders
animation_placeholder = st.empty()
status_placeholder = st.empty()
progress_bar = st.progress(0)
time_placeholder = st.empty()
speech_bubble = st.empty()

# Play button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    play = st.button("🎬 PLAY CARTOON 🎬", use_container_width=True)

if play:
    
    # ========== ACT 1: THE FIGHT (0-10 seconds) ==========
    with status_placeholder.container():
        st.markdown('<div class="speech-bubble">🎬 ACT 1: THE EPIC DUEL! 🎬</div>', unsafe_allow_html=True)
    
    # Characters intro
    for i in range(3):
        col1, col2 = st.columns(2)
        with col1:
            st.image(draw_cartoon_fighter("red", expression="angry"), use_column_width=True)
        with col2:
            st.image(draw_cartoon_fighter("blue", expression="angry"), use_column_width=True)
        progress_bar.progress(i * 0.03)
        time.sleep(0.5)
    
    # Fight sequence with cartoon effects
    for round_num in range(8):
        # Rex attacks
        with animation_placeholder.container():
            st.markdown('<div class="cartoon-panel">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.image(draw_cartoon_fighter("red", action="attack"), use_column_width=True)
            with col2:
                st.image(draw_cartoon_fighter("blue", expression="hurt"), use_column_width=True)
            st.markdown('<p style="text-align: center; font-weight: bold;">💥 POW! 💥</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            with speech_bubble.container():
                st.markdown('<div class="speech-bubble">"Take this!" - Rex</div>', unsafe_allow_html=True)
        
        progress_bar.progress(0.1 + (round_num * 0.03))
        time_placeholder.markdown(f"### ⏱️ {round_num + 1}/8 Rounds")
        time.sleep(0.6)
        
        # Blu counters
        with animation_placeholder.container():
            st.markdown('<div class="cartoon-panel">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.image(draw_cartoon_fighter("red", expression="hurt"), use_column_width=True)
            with col2:
                st.image(draw_cartoon_fighter("blue", action="attack"), use_column_width=True)
            st.markdown('<p style="text-align: center; font-weight: bold;">💥 BAM! 💥</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            with speech_bubble.container():
                st.markdown('<div class="speech-bubble">"Not so fast!" - Blu</div>', unsafe_allow_html=True)
        
        progress_bar.progress(0.15 + (round_num * 0.03))
        time.sleep(0.6)
    
    # Both tired
    with animation_placeholder.container():
        st.markdown('<div class="cartoon-panel">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.image(draw_cartoon_fighter("red", expression="tired"), use_column_width=True)
        with col2:
            st.image(draw_cartoon_fighter("blue", expression="tired"), use_column_width=True)
        st.markdown('<p style="text-align: center;">😫 Both fighters are exhausted! 😫</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    progress_bar.progress(0.33)
    time.sleep(2)
    
    # ========== ACT 2: PEACEFUL EVENING (10-20 seconds) ==========
    with status_placeholder.container():
        st.markdown('<div class="speech-bubble">🌅 ACT 2: A PEACEFUL EVENING 🌅</div>', unsafe_allow_html=True)
    
    # Sunset transition
    for step in range(30):
        if step < 15:
            bg = draw_cartoon_background("sunset")
            message = "The sun begins to set..."
        else:
            bg = draw_cartoon_background("night")
            message = "Stars appear in the sky..."
        
        with animation_placeholder.container():
            st.image(bg, use_column_width=True)
            st.markdown(f'<p style="text-align: center; font-style: italic;">{message}</p>', unsafe_allow_html=True)
        
        progress_bar.progress(0.33 + (step / 100))
        time_placeholder.markdown(f"### ⏱️ {int(10 + step * 0.33)} seconds")
        time.sleep(0.15)
    
    # Add twinkling stars effect
    for star_count in range(20):
        bg = draw_cartoon_background("night")
        draw = ImageDraw.Draw(bg)
        
        # Draw twinkling stars
        for _ in range(star_count):
            x = random.randint(50, 750)
            y = random.randint(50, 300)
            draw.ellipse([x-2, y-2, x+2, y+2], fill=(255, 255, 200))
            draw.ellipse([x-1, y-1, x+1, y+1], fill='white')
        
        with animation_placeholder.container():
            st.image(bg, use_column_width=True)
            st.markdown('<p style="text-align: center;">⭐ The stars are twinkling! ⭐</p>', unsafe_allow_html=True)
        
        progress_bar.progress(0.5 + (star_count / 80))
        time.sleep(0.1)
    
    with speech_bubble.container():
        st.markdown('<div class="speech-bubble">"What a beautiful night..." 🌙</div>', unsafe_allow_html=True)
    
    time.sleep(1)
    
    # ========== ACT 3: KIDS PLAYING (20-30 seconds) ==========
    with status_placeholder.container():
        st.markdown('<div class="speech-bubble">👧 ACT 3: PLAYGROUND FUN! 👦</div>', unsafe_allow_html=True)
    
    # Kids introduction
    kids = [
        ("yellow", "Lily", "👧"),
        ("green", "Max", "🧒"),
        ("pink", "Leo", "👦")
    ]
    
    for angle_step in range(40):
        angle = angle_step * 0.3
        
        with animation_placeholder.container():
            st.markdown('<div class="cartoon-panel">', unsafe_allow_html=True)
            st.markdown("### 🎪 Cartoon Playground 🎪")
            
            # Animated kids positions
            cols = st.columns(5)
            
            for i, (color, name, emoji) in enumerate(kids):
                pos_angle = angle + (i * 2 * math.pi / 3)
                x_pos = int(2 + 2 * math.cos(pos_angle))
                x_pos = max(0, min(4, x_pos))
                
                with cols[x_pos]:
                    # Bounce effect
                    bounce = abs(math.sin(angle_step * 0.5 + i)) * 10
                    st.markdown(f'<div style="transform: translateY(-{bounce}px);">', unsafe_allow_html=True)
                    st.image(draw_cartoon_kid(color, name, action="waving" if angle_step % 10 == 0 else "playing"), use_column_width=True)
                    st.markdown(f'<p style="text-align: center;">{emoji} {name}</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Playground equipment
            st.markdown("---")
            toys = ["🛝 Slide", "🎠 Swing", "🧸 Teddy", "🤸‍♀️ Monkey Bars", "🎪 Playhouse"]
            toy_cols = st.columns(5)
            for i, toy in enumerate(toys):
                with toy_cols[i]:
                    st.markdown(f"**{toy}**")
            
            # Random cartoon sound effect text
            effects = ["Wheee!", "Haha!", "Woo-hoo!", "Yay!", "Let's play!"]
            st.markdown(f'<p style="text-align: center; font-size: 24px;">✨ {random.choice(effects)} ✨</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        progress_bar.progress(0.66 + (angle_step / 120))
        time_placeholder.markdown(f"### ⏱️ {int(20 + angle_step * 0.25)} seconds")
        time.sleep(0.12)
    
    # GRAND FINALE - All characters together
    with animation_placeholder.container():
        st.markdown('<div class="cartoon-panel">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align: center;">🎉 HAPPY ENDING! 🎉</h1>', unsafe_allow_html=True)
        
        # Group photo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(draw_cartoon_fighter("red", expression="happy"), use_column_width=True)
            st.caption("Rex the Fighter")
        with col2:
            st.image(draw_cartoon_kid("yellow", "Lily"), use_column_width=True)
            st.image(draw_cartoon_kid("green", "Max"), use_column_width=True)
            st.image(draw_cartoon_kid("pink", "Leo"), use_column_width=True)
            st.caption("The Playful Kids!")
        with col3:
            st.image(draw_cartoon_fighter("blue", expression="happy"), use_column_width=True)
            st.caption("Blu the Fighter")
        
        st.markdown("---")
        st.markdown('<p style="text-align: center; font-size: 24px;">🌟 And they all became friends! 🌟</p>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center;">The End</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    progress_bar.progress(1.0)
    time_placeholder.markdown("### ⏱️ 30 seconds - Cartoon Complete! 🎬")
    status_placeholder.success("✅ Cartoon Animation Finished!")
    
    # Celebration effects
    st.balloons()
    st.snow()
    
    with speech_bubble.container():
        st.markdown('<div class="speech-bubble">"That was fun! Let\'s play again!" 🎉</div>', unsafe_allow_html=True)

else:
    # Preview with cartoon styling
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="cartoon-panel">', unsafe_allow_html=True)
        st.markdown("### ⚔️ ACT 1")
        st.image(draw_cartoon_fighter("red"), use_column_width=True)
        st.image(draw_cartoon_fighter("blue"), use_column_width=True)
        st.markdown("**The Epic Duel**")
        st.markdown("*0-10 seconds*")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="cartoon-panel">', unsafe_allow_html=True)
        st.markdown("### 🌅 ACT 2")
        preview_bg = draw_cartoon_background("sunset")
        st.image(preview_bg, use_column_width=True)
        st.markdown("**Peaceful Evening**")
        st.markdown("*10-20 seconds*")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="cartoon-panel">', unsafe_allow_html=True)
        st.markdown("### 👧 ACT 3")
        st.image(draw_cartoon_kid("yellow", "Lily"), use_column_width=True)
        st.image(draw_cartoon_kid("green", "Max"), use_column_width=True)
        st.image(draw_cartoon_kid("pink", "Leo"), use_column_width=True)
        st.markdown("**Playground Fun**")
        st.markdown("*20-30 seconds*")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center;">
        <h3>🎨 A Complete Cartoon Short! 🎨</h3>
        <p>Hand-drawn style • Speech bubbles • Cartoon effects • Happy ending</p>
        <p><strong>Press PLAY above to watch the 30-second cartoon!</strong></p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🎬 Cartoon Animation | 🎨 Hand-drawn Style | ⏱️ 30 Seconds | 🌟 Made with Streamlit</p>
</div>
""", unsafe_allow_html=True)
