""")

st.markdown("</div>", unsafe_allow_html=True)

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
        st.markdown(f"<div style='margin-top: -{bounce}px;'>🎈</div>", unsafe_allow_html=True)

# Playground equipment
st.markdown("---")
st.markdown("🛝  🧸  🎠  🤸  🎪")

progress_bar.progress(50 + angle_step * 1.25)
time.sleep(0.1)

# Final celebration
with animation_placeholder.container():
st.balloons()
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

st.success("✅ 30-second animation completed successfully!")
st.balloons()

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
st.caption("⏱️ Total duration: 30 seconds | Made with Streamlit | No external packages needed!")

# Simple instructions
with st.expander("🚀 How to Deploy (100% Working Method)"):
st.markdown("""
### ✅ This version uses ONLY Streamlit (no Plotly, no NumPy!)

**Step 1:** Create a folder with these 2 files:

**`app.py`** - Copy the code above

**`requirements.txt`** - Create this file with ONE line:
