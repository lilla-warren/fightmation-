import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
import random

# Page setup
st.set_page_config(page_title="30-Second Animation", layout="wide")

st.title("🎬 30-Second Animation: Fight → Peaceful Evening → Kids Playing")

# Create placeholder for animation
animation_placeholder = st.empty()
status_text = st.empty()
progress_bar = st.progress(0)

# Simple fighter function
def show_fighters(red_x, blue_x, punch_effect=False):
    fig = go.Figure()
    
    # Red fighter
    fig.add_trace(go.Scatter(
        x=[red_x], y=[0],
        mode='markers',
        marker=dict(size=40, color='red', symbol='circle'),
        name='Red Fighter'
    ))
    
    # Blue fighter
    fig.add_trace(go.Scatter(
        x=[blue_x], y=[0],
        mode='markers',
        marker=dict(size=40, color='blue', symbol='circle'),
        name='Blue Fighter'
    ))
    
    # Punch effect
    if punch_effect == "red":
        fig.add_trace(go.Scatter(
            x=[red_x + 0.5], y=[0.3],
            mode='markers',
            marker=dict(size=20, color='orange', symbol='star'),
            showlegend=False
        ))
    elif punch_effect == "blue":
        fig.add_trace(go.Scatter(
            x=[blue_x - 0.5], y=[0.3],
            mode='markers',
            marker=dict(size=20, color='orange', symbol='star'),
            showlegend=False
        ))
    
    fig.update_xaxes(range=[-5, 5], showgrid=False)
    fig.update_yaxes(range=[-1.5, 1.5], showgrid=False)
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

# Simple peaceful scene
def show_peaceful(sunset_level=0, stars=False):
    fig = go.Figure()
    
    # Sun
    sun_color = 'orange' if sunset_level < 0.5 else 'darkorange'
    fig.add_trace(go.Scatter(
        x=[0], y=[2],
        mode='markers',
        marker=dict(size=50, color=sun_color, symbol='circle'),
        showlegend=False
    ))
    
    # Ground
    fig.add_trace(go.Scatter(
        x=[-5, 5], y=[-1, -1],
        mode='lines',
        line=dict(width=3, color='darkgreen'),
        fill='tozeroy',
        fillcolor='lightgreen',
        showlegend=False
    ))
    
    # Trees
    for i in range(4):
        tree_x = -3 + i * 2
        fig.add_trace(go.Scatter(
            x=[tree_x, tree_x], y=[-1, 0.5],
            mode='lines',
            line=dict(width=8, color='brown'),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[tree_x], y=[0.5],
            mode='markers',
            marker=dict(size=30, color='green', symbol='triangle-up'),
            showlegend=False
        ))
    
    # Stars
    if stars:
        for _ in range(20):
            star_x = random.uniform(-4.5, 4.5)
            star_y = random.uniform(1, 2.5)
            fig.add_trace(go.Scatter(
                x=[star_x], y=[star_y],
                mode='markers',
                marker=dict(size=4, color='white', symbol='star'),
                showlegend=False
            ))
    
    fig.update_xaxes(range=[-5, 5], showgrid=False, showticklabels=False)
    fig.update_yaxes(range=[-1.5, 2.5], showgrid=False, showticklabels=False)
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
    return fig

# Simple kids scene
def show_kids(angle=0):
    fig = go.Figure()
    colors = ['gold', 'lightgreen', 'hotpink']
    names = ['Kid 1', 'Kid 2', 'Kid 3']
    
    for i, (color, name) in enumerate(zip(colors, names)):
        # Circular motion
        x_pos = 2.5 * np.cos(angle + i * 2 * np.pi / 3)
        y_pos = 0.5 + abs(np.sin(angle * 5 + i)) * 0.3  # Bounce
        
        fig.add_trace(go.Scatter(
            x=[x_pos], y=[y_pos],
            mode='markers',
            marker=dict(size=35, color=color, symbol='circle'),
            name=name,
            showlegend=False
        ))
        
        # Eyes
        fig.add_trace(go.Scatter(
            x=[x_pos - 0.1, x_pos + 0.1], y=[y_pos + 0.15, y_pos + 0.15],
            mode='markers',
            marker=dict(size=5, color='black', symbol='circle'),
            showlegend=False
        ))
    
    fig.update_xaxes(range=[-4, 4], showgrid=False, showticklabels=False)
    fig.update_yaxes(range=[-0.5, 2], showgrid=False, showticklabels=False)
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
    return fig

# Main animation button
if st.button("▶️ PLAY 30-SECOND ANIMATION", type="primary", use_container_width=True):
    
    # ========== PART 1: FIGHT (0-10 seconds) ==========
    status_text.markdown("### 🥊 PART 1: Fighters battling (0-10 seconds)")
    
    # Walk toward each other (2 seconds)
    for step in range(20):
        t = step / 20  # 0 to 1
        red_x = -3 + (2 * t)  # -3 to -1
        blue_x = 3 - (2 * t)   # 3 to 1
        fig = show_fighters(red_x, blue_x)
        animation_placeholder.plotly_chart(fig, use_container_width=True)
        progress_bar.progress(step * 0.5)  # 0-10%
        time.sleep(0.1)
    
    # Fighting punches (8 seconds)
    for punch in range(16):
        if punch % 2 == 0:
            fig = show_fighters(-1, 1, punch_effect="red")
            status_text.markdown("### 🥊 RED PUNCHES! 🥊")
        else:
            fig = show_fighters(-1, 1, punch_effect="blue")
            status_text.markdown("### 🥊 BLUE PUNCHES! 🥊")
        
        animation_placeholder.plotly_chart(fig, use_container_width=True)
        progress_bar.progress(10 + punch * 1.25)  # 10-30%
        time.sleep(0.5)
    
    # Fight ends - both fall
    for fall in range(10):
        red_y = -fall * 0.1
        blue_y = -fall * 0.1
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[-1], y=[red_y],
            mode='markers',
            marker=dict(size=40, color='red', symbol='circle'),
            name='Red Fighter'
        ))
        fig.add_trace(go.Scatter(
            x=[1], y=[blue_y],
            mode='markers',
            marker=dict(size=40, color='blue', symbol='circle'),
            name='Blue Fighter'
        ))
        fig.update_xaxes(range=[-5, 5])
        fig.update_yaxes(range=[-1.5, 1.5])
        fig.update_layout(height=400)
        animation_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.05)
    
    time.sleep(1)
    
    # ========== PART 2: PEACEFUL EVENING (10-20 seconds) ==========
    status_text.markdown("### 🌅 PART 2: Peaceful evening (10-20 seconds)")
    
    # Sunset transition
    for i in range(20):
        sunset = i / 20
        fig = show_peaceful(sunset_level=sunset)
        animation_placeholder.plotly_chart(fig, use_container_width=True)
        progress_bar.progress(30 + i * 0.5)  # 30-40%
        time.sleep(0.1)
    
    # Evening scene with stars
    for i in range(20):
        stars = i > 10
        fig = show_peaceful(stars=stars)
        if stars:
            fig.update_layout(paper_bgcolor='rgba(20, 20, 60, 0.9)')
        animation_placeholder.plotly_chart(fig, use_container_width=True)
        progress_bar.progress(40 + i * 0.5)  # 40-50%
        time.sleep(0.15)
    
    time.sleep(1)
    
    # ========== PART 3: KIDS PLAYING (20-30 seconds) ==========
    status_text.markdown("### 👧🧒👦 PART 3: Kids playing (20-30 seconds)")
    
    # Kids running in circle
    for angle_step in range(40):
        angle = angle_step * 0.3
        fig = show_kids(angle)
        animation_placeholder.plotly_chart(fig, use_container_width=True)
        progress_bar.progress(50 + angle_step * 1.25)  # 50-100%
        time.sleep(0.1)
    
    # Final celebration
    status_text.markdown("### 🎉 ANIMATION COMPLETE! 🎉")
    
    fig = show_kids(0)
    fig.update_layout(
        title=dict(text="🎉 THE END - Happy Kids! 🎉", x=0.5, xanchor='center')
    )
    animation_placeholder.plotly_chart(fig, use_container_width=True)
    progress_bar.progress(100)
    
    st.balloons()
    st.success("✅ 30-second animation completed successfully!")
    
else:
    # Show preview
    st.info("👆 **Click the PLAY button above** to watch the 30-second animation!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🥊 0-10 seconds")
        st.markdown("**Fight Scene**")
        st.markdown("- Red vs Blue fighters")
        st.markdown("- Punching action")
        st.markdown("- Both fall down")
    
    with col2:
        st.markdown("### 🌅 10-20 seconds")
        st.markdown("**Peaceful Evening**")
        st.markdown("- Sunset colors")
        st.markdown("- Trees and ground")
        st.markdown("- Stars appear")
    
    with col3:
        st.markdown("### 👧 20-30 seconds")
        st.markdown("**Kids Playing**")
        st.markdown("- Three kids")
        st.markdown("- Running in circles")
        st.markdown("- Happy ending")
    
    st.markdown("---")
    st.caption("⏱️ Total duration: 30 seconds | Made with Streamlit")

# Instructions
with st.expander("🚀 How to Deploy This on Streamlit Cloud"):
    st.markdown("""
    ### Step-by-step:
    
    1. **Create these 2 files in a folder:**
       - `app.py` (copy the code above)
       - `requirements.txt` (with the 3 lines below)
    
    2. **Push to GitHub**
    
    3. **Go to** https://share.streamlit.io
    
    4. **Click "New app"**
    
    5. **Select your repository**
    
    6. **Main file path:** `app.py`
    
    7. **Click Deploy!**
    
    ### requirements.txt content:
