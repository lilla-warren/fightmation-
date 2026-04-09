import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
from PIL import Image, ImageDraw
import random

# Page setup
st.set_page_config(page_title="Fighter Animation", layout="wide")
st.title("🎬 30-Second Animation: Fight → Peaceful Evening → Kids Playing")

# Create placeholder for animation
animation_placeholder = st.empty()
status_text = st.empty()

# Function to create fighter (red or blue)
def create_fighter(color, x_pos, y_pos=0):
    fig = go.Figure()
    
    # Body (circle)
    fig.add_trace(go.Scatter(
        x=[x_pos], y=[y_pos],
        mode='markers',
        marker=dict(size=50, color=color, symbol='circle'),
        name=f'{color} Fighter',
        showlegend=False
    ))
    
    # Sword (line)
    fig.add_trace(go.Scatter(
        x=[x_pos + 0.3, x_pos + 0.6],
        y=[y_pos, y_pos + 0.3],
        mode='lines',
        line=dict(width=5, color='gray'),
        showlegend=False
    ))
    
    fig.update_xaxes(range=[-5, 5])
    fig.update_yaxes(range=[-2, 3])
    fig.update_layout(height=400, width=800, showlegend=False)
    
    return fig

# Function to create peaceful scene
def create_peaceful_scene():
    fig = go.Figure()
    
    # Sun
    fig.add_trace(go.Scatter(
        x=[0], y=[2],
        mode='markers',
        marker=dict(size=60, color='orange', symbol='circle'),
        showlegend=False
    ))
    
    # Trees
    for i in range(5):
        x = random.uniform(-4, 4)
        fig.add_trace(go.Scatter(
            x=[x], y=[-1],
            mode='markers',
            marker=dict(size=40, color='green', symbol='triangle-up'),
            showlegend=False
        ))
    
    fig.update_xaxes(range=[-5, 5])
    fig.update_yaxes(range=[-2, 3])
    fig.update_layout(height=400, width=800, showlegend=False)
    
    return fig

# Function to create kids
def create_kids():
    fig = go.Figure()
    colors = ['yellow', 'lightgreen', 'pink']
    positions = [-2, 0, 2]
    
    for i, (color, x_pos) in enumerate(zip(colors, positions)):
        # Kid body
        fig.add_trace(go.Scatter(
            x=[x_pos], y=[0],
            mode='markers',
            marker=dict(size=30, color=color, symbol='circle'),
            showlegend=False
        ))
        
        # Head
        fig.add_trace(go.Scatter(
            x=[x_pos], y=[0.5],
            mode='markers',
            marker=dict(size=20, color=color, symbol='circle'),
            showlegend=False
        ))
    
    fig.update_xaxes(range=[-5, 5])
    fig.update_yaxes(range=[-2, 3])
    fig.update_layout(height=400, width=800, showlegend=False)
    
    return fig

# Progress bar
progress_bar = st.progress(0)

# ANIMATION STARTS HERE
if st.button("🎬 Play 30-Second Animation"):
    
    # ========== PART 1: FIGHT (0-10 seconds) ==========
    status_text.text("🥊 Part 1: Fighters battling... (0-10s)")
    
    # Animate fighters moving toward each other
    for t in np.linspace(-3, -1, 30):
        fig = go.Figure()
        
        # Red fighter (moving right)
        fig.add_trace(go.Scatter(
            x=[t], y=[0],
            mode='markers',
            marker=dict(size=50, color='red', symbol='circle'),
            name='Red Fighter'
        ))
        
        # Blue fighter (moving left)
        fig.add_trace(go.Scatter(
            x=[-t], y=[0],
            mode='markers',
            marker=dict(size=50, color='blue', symbol='circle'),
            name='Blue Fighter'
        ))
        
        fig.update_xaxes(range=[-4, 4])
        fig.update_yaxes(range=[-2, 2])
        fig.update_layout(title="⚔️ FIGHT! ⚔️", height=450, width=800)
        animation_placeholder.plotly_chart(fig, use_container_width=True)
        progress_bar.progress(t * 2 + 6)  # Update progress (0-10%)
        time.sleep(0.1)
    
    # Fighting animation (punches)
    for punch in range(8):
        # Red punches
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[-1, -0.5], y=[0, 0.5],
            mode='markers+lines',
            marker=dict(size=[50, 30], color=['red', 'red']),
            line=dict(width=3, color='red')
        ))
        fig.add_trace(go.Scatter(
            x=[1], y=[0],
            mode='markers',
            marker=dict(size=50, color='blue')
        ))
        fig.update_xaxes(range=[-4, 4])
        fig.update_yaxes(range=[-2, 2])
        fig.update_layout(title="💥 RED PUNCHES! 💥", height=450, width=800)
        animation_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.3)
        
        # Blue punches back
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[1, 0.5], y=[0, 0.5],
            mode='markers+lines',
            marker=dict(size=[50, 30], color=['blue', 'blue']),
            line=dict(width=3, color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=[-1], y=[0],
            mode='markers',
            marker=dict(size=50, color='red')
        ))
        fig.update_xaxes(range=[-4, 4])
        fig.update_yaxes(range=[-2, 2])
        fig.update_layout(title="💥 BLUE PUNCHES! 💥", height=450, width=800)
        animation_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.3)
        
        progress_bar.progress(10 + punch * 2)  # Progress 10-30%
    
    # ========== PART 2: PEACEFUL EVENING (10-20 seconds) ==========
    status_text.text("🌅 Part 2: Peaceful evening... (10-20s)")
    
    # Sunset effect
    for brightness in np.linspace(1, 0.3, 20):
        fig = create_peaceful_scene()
        fig.update_layout(
            title="🌅 Peaceful Evening Sunset 🌅",
            paper_bgcolor=f'rgba(255, {int(150*brightness)}, {int(100*brightness)}, 1)',
            plot_bgcolor=f'rgba(255, {int(150*brightness)}, {int(100*brightness)}, 1)',
            height=450,
            width=800
        )
        animation_placeholder.plotly_chart(fig, use_container_width=True)
        progress_bar.progress(30 + brightness * 10)
        time.sleep(0.1)
    
    # Add stars
    for star_count in range(10, 50, 5):
        fig = create_peaceful_scene()
        
        # Add stars
        for _ in range(star_count):
            star_x = random.uniform(-4, 4)
            star_y = random.uniform(1, 2.5)
            fig.add_trace(go.Scatter(
                x=[star_x], y=[star_y],
                mode='markers',
                marker=dict(size=5, color='white', symbol='star'),
                showlegend=False
            ))
        
        fig.update_layout(
            title="✨ Peaceful Evening with Stars ✨",
            paper_bgcolor='rgba(10, 10, 50, 1)',
            plot_bgcolor='rgba(10, 10, 50, 1)',
            height=450,
            width=800
        )
        animation_placeholder.plotly_chart(fig, use_container_width=True)
        progress_bar.progress(40 + star_count // 2)
        time.sleep(0.1)
    
    # ========== PART 3: KIDS PLAYING (20-30 seconds) ==========
    status_text.text("👧🧒👦 Part 3: Kids playing... (20-30s)")
    
    # Animate kids running in circle
    for angle in np.linspace(0, 4 * np.pi, 40):
        fig = go.Figure()
        colors = ['yellow', 'lightgreen', 'pink']
        
        for i, color in enumerate(colors):
            # Calculate circular motion
            x_pos = 2 * np.cos(angle + i * 2 * np.pi / 3)
            z_pos = 2 * np.sin(angle + i * 2 * np.pi / 3)
            
            # Kid body
            fig.add_trace(go.Scatter(
                x=[x_pos], y=[0],
                mode='markers',
                marker=dict(size=30, color=color, symbol='circle'),
                showlegend=False
            ))
            
            # Kid head
            fig.add_trace(go.Scatter(
                x=[x_pos], y=[0.5],
                mode='markers',
                marker=dict(size=20, color=color, symbol='circle'),
                showlegend=False
            ))
            
            # Bounce effect
            bounce = abs(np.sin(angle * 5 + i)) * 0.2
            fig.add_trace(go.Scatter(
                x=[x_pos], y=[0 + bounce],
                mode='markers',
                marker=dict(size=25, color=color, symbol='circle'),
                showlegend=False
            ))
        
        fig.update_xaxes(range=[-4, 4])
        fig.update_yaxes(range=[-1, 3])
        fig.update_layout(
            title="🎠 Kids Playing! 🎠",
            height=450,
            width=800
        )
        animation_placeholder.plotly_chart(fig, use_container_width=True)
        progress_bar.progress(60 + angle * 10)
        time.sleep(0.1)
    
    # Kids gather together at the end
    status_text.text("🎉 Animation Complete! 🎉")
    
    # Final scene - all kids together
    fig = go.Figure()
    final_positions = [-1, 0, 1]
    colors = ['yellow', 'lightgreen', 'pink']
    
    for i, (color, x_pos) in enumerate(zip(colors, final_positions)):
        fig.add_trace(go.Scatter(
            x=[x_pos], y=[0],
            mode='markers',
            marker=dict(size=35, color=color, symbol='circle'),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[x_pos], y=[0.5],
            mode='markers',
            marker=dict(size=25, color=color, symbol='circle'),
            showlegend=False
        ))
    
    fig.update_xaxes(range=[-4, 4])
    fig.update_yaxes(range=[-1, 3])
    fig.update_layout(
        title="🎉 THE END - Happy Kids! 🎉",
        height=450,
        width=800
    )
    animation_placeholder.plotly_chart(fig, use_container_width=True)
    progress_bar.progress(100)
    
    st.balloons()  # Celebration!
    st.success("✅ 30-second animation completed successfully!")

else:
    # Show preview before playing
    st.info("👆 Click the button above to play the 30-second animation!")
    
    # Preview image
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🥊 Part 1: Fight**")
        st.markdown("0-10 seconds")
        st.code("""
        🔴 vs 🔵
        Punch! Punch!
        """)
    
    with col2:
        st.markdown("**🌅 Part 2: Peaceful**")
        st.markdown("10-20 seconds")
        st.code("""
        🌞 Sunset
        🌲 Trees
        ⭐ Stars
        """)
    
    with col3:
        st.markdown("**👧 Part 3: Kids**")
        st.markdown("20-30 seconds")
        st.code("""
        🟡 🟢 🩷
        Running
        Playing
        """)

# Instructions
with st.expander("📖 How to deploy this on Streamlit Cloud"):
    st.markdown("""
    1. **Push this code to GitHub**
    2. **Go to** share.streamlit.io
    3. **Sign in with GitHub**
    4. **Click "New app"**
    5. **Select your repository** (fighter-animation)
    6. **Main file path:** app.py
    7. **Click Deploy!**
    
    Your animation will be live at: `https://your-name-fighter-animation.streamlit.app`
    """)
