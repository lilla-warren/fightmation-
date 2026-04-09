import streamlit as st
import time
import random
import math

# Page setup
st.set_page_config(page_title="30-Second Animation", layout="wide")

st.title("🎬 30-Second Animation: Fight → Peaceful Evening → Kids Playing")

# Create placeholder for animation
animation_placeholder = st.empty()
status_text = st.empty()
progress_bar = st.progress(0)

# ========== MAIN ANIMATION ==========
if st.button("▶️ PLAY 30-SECOND ANIMATION", type="primary", use_container_width=True):
    
    # ========== PART 1: FIGHT (0-10 seconds) ==========
    status_text.markdown("### 🥊 PART 1: FIGHTERS BATTLE (0-10 seconds)")
    
    # Walk toward each other (2 seconds)
    for step in range(20):
        with animation_placeholder.container():
            cols = st.columns(3)
            
            with cols[0]:
                st.markdown("## 🔴")
                st.caption("Red Fighter")
            
            with cols[1]:
                st.markdown("VS")
            
            with cols[2]:
                st.markdown("## 🔵")
                st.caption("Blue Fighter")
        
        progress_bar.progress(step * 0.5)
        time.sleep(0.1)
    
    # Fighting (8 seconds)
    for punch in range(16):
        with animation_placeholder.container():
            if punch % 2 == 0:
                st.markdown("## 🔴  VS  🔵")
                st.markdown("### 💥 RED PUNCHES! 💥")
                st.markdown("###     👊")
                status_text.markdown("### 🥊 RED ATTACKS! 🥊")
            else:
                st.markdown("## 🔴  VS  🔵")
                st.markdown("### 💥 BLUE KICKS! 💥")
                st.markdown("###     🦶")
                status_text.markdown("### 🥋 BLUE STRIKES! 🥋")
        
        progress_bar.progress(10 + punch * 1.25)
        time.sleep(0.5)
    
    # Both fall
    for fall in range(10):
        with animation_placeholder.container():
            st.markdown("## 😫  😫")
            st.markdown("### Both fighters are down!")
            st.markdown("💨 💨 💨")
        time.sleep(0.1)
    
    time.sleep(1)
    
    # ========== PART 2: PEACEFUL EVENING (10-20 seconds) ==========
    status_text.markdown("### 🌅 PART 2: PEACEFUL EVENING (10-20 seconds)")
    
    # Sunset
    for step in range(20):
        with animation_placeholder.container():
            st.markdown("### 🌅 Peaceful Evening")
            
            # Sun position
            sun_x = "🌞" + " " * (20 - step) + "☁️"
            st.markdown(f"{sun_x}")
            
            # Trees
            st.markdown("🌲              🌳              🌲")
            st.markdown("🌲 🌲           🌳 🌳           🌲 🌲")
        
        progress_bar.progress(30 + step * 0.5)
        time.sleep(0.15)
    
    # Night with stars
    for step in range(20):
        with animation_placeholder.container():
            st.markdown("### 🌙 Starry Night")
            
            # Stars appearing
            stars = "⭐ " * (step + 5)
            st.markdown(f"{stars}")
            
            # Trees
            st.markdown("🌲              🌳              🌲")
            st.markdown("🌲 🌲           🌳 🌳           🌲 🌲")
        
        progress_bar.progress(40 + step * 0.5)
        time.sleep(0.15)
    
    time.sleep(1)
    
    # ========== PART 3: KIDS PLAYING (20-30 seconds) ==========
    status_text.markdown("### 👧🧒👦 PART 3: KIDS PLAYING (20-30 seconds)")
    
    # Kids running in circle
    for angle_step in range(40):
        angle = angle_step * 0.3
        
        with animation_placeholder.container():
            st.markdown("### 🎪 Playground Time! 🎪")
            
            # Create circular motion with emojis
            cols = st.columns(7)
            
            # Position 3 kids in a circle
            for i in range(3):
                pos_angle = angle + (i * 2 * 3.14159 / 3)
                x_pos = int(3 + 3 * math.cos(pos_angle))
                
                if x_pos < 0:
                    x_pos = 0
                if x_pos > 6:
                    x_pos = 6
                
                if i == 0:
                    kid = "👧"
                    color = "🟡"
                elif i == 1:
                    kid = "🧒"
                    color = "🟢"
                else:
                    kid = "👦"
                    color = "🩷"
                
                with cols[x_pos]:
                    bounce = abs(math.sin(angle * 5 + i)) * 20
                    st.markdown(f"### {color} {kid}")
                    st.markdown(f"🎈")
            
            # Playground equipment
            st.markdown("---")
            st.markdown("🛝  🧸  🎠  🤸  🎪")
        
        progress_bar.progress(50 + angle_step * 1.25)
        time.sleep(0.1)
    
    # Final celebration
    with animation_placeholder.container():
        st.markdown("# 🎉🎉🎉")
        st.markdown("## THE END - Happy Kids!")
        st.markdown("### 👧 🧒 👦")
        st.markdown("### 🎈 🎈 🎈")
        
        # Final group pose
        cols = st.columns(3)
        with cols[0]:
            st.markdown("### 🟡 👧")
        with cols[1]:
            st.markdown("### 🟢 🧒")
        with cols[2]:
            st.markdown("### 🩷 👦")
    
    progress_bar.progress(100)
    status_text.markdown("### 🎉 ANIMATION COMPLETE! 🎉")
    
    st.balloons()
    st.success("✅ 30-second animation completed successfully!")

else:
    # Show preview
    st.info("👆 **Click the PLAY button above** to watch the 30-second animation!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🥊 0-10 seconds")
        st.markdown("**Fight Scene**")
        st.markdown("🔴 vs 🔵")
        st.markdown("Punching and kicking")
        st.markdown("Both fighters fall")
    
    with col2:
        st.markdown("### 🌅 10-20 seconds")
        st.markdown("**Peaceful Evening**")
        st.markdown("🌞 Sunset")
        st.markdown("🌲 Trees appear")
        st.markdown("⭐ Stars come out")
    
    with col3:
        st.markdown("### 👧 20-30 seconds")
        st.markdown("**Kids Playing**")
        st.markdown("Three kids")
        st.markdown("Running in circles")
        st.markdown("Happy ending!")
    
    st.markdown("---")
    st.caption("⏱️ Total duration: 30 seconds | Made with Streamlit")

# Simple instructions
with st.expander("🚀 How to Deploy"):
    st.markdown("""
    **Step 1:** Create a folder with these 2 files:
    - app.py (copy the code above)
    - requirements.txt (with one line: streamlit)
    
    **Step 2:** Push to GitHub
    
    **Step 3:** Deploy on share.streamlit.io
    
    **Step 4:** Select app.py as main file
    
    **Step 5:** Click Deploy
    """)
