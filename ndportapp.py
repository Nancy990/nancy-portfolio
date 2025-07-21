import streamlit as st
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
import random

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Nancy Diana | AI Strategist", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- CUSTOM CSS WITH ANIMATIONS ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Custom background */
    .stApp {
        background-color: #fbcc9c !important;
    }
    
    .main .block-container {
        background-color: #fbcc9c;
    }
    
    .main-header {
        background: linear-gradient(90deg, #ff6b35 0%, #f7931e 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .main-header:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(255, 107, 53, 0.4);
    }
    
    .skill-card {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
    }
    
    .skill-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(255, 107, 53, 0.3);
    }
    
    .project-card {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .project-card:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 30px rgba(255, 107, 53, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 0.5rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 15px 30px rgba(255, 107, 53, 0.4);
    }
    
    /* Interactive Skill Bars with Animation */
    .skill-bar-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 5px;
        margin: 10px 0;
        position: relative;
        overflow: hidden;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .skill-bar-container:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(255, 107, 53, 0.3);
    }
    
    .skill-bar {
        background: linear-gradient(90deg, #ff6b35, #f7931e, #ffb347);
        height: 30px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 15px;
        color: white;
        font-weight: bold;
        position: relative;
        overflow: hidden;
        animation: fillBar 2s ease-out;
    }
    
    .skill-bar::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes fillBar {
        from { width: 0%; }
        to { width: var(--skill-width); }
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Card-style skills */
    .skill-card-interactive {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        color: white;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .skill-card-interactive:hover {
        transform: rotateY(10deg) rotateX(10deg) scale(1.05);
        box-shadow: 0 20px 40px rgba(255, 107, 53, 0.3);
    }
    
    .skill-card-interactive::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(transparent, rgba(255,255,255,0.3), transparent);
        animation: rotate 4s linear infinite;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .skill-card-interactive:hover::before {
        opacity: 1;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .skill-level {
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .skill-name {
        font-size: 14px;
        opacity: 0.9;
    }
    
    /* Circular Progress Ring */
    .skill-circle {
        display: inline-block;
        position: relative;
        width: 120px;
        height: 120px;
        margin: 10px;
    }
    
    .skill-circle svg {
        width: 120px;
        height: 120px;
        transform: rotate(-90deg);
    }
    
    .skill-circle-bg {
        fill: none;
        stroke: rgba(255, 107, 53, 0.2);
        stroke-width: 8;
    }
    
    .skill-circle-progress {
        fill: none;
        stroke: #ff6b35;
        stroke-width: 8;
        stroke-linecap: round;
        transition: stroke-dasharray 1s ease-in-out;
    }
    
    .skill-circle-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        font-weight: bold;
        color: #ff6b35;
    }
    
    /* Hexagon skill cards */
    .hexagon-skill {
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        position: relative;
        margin: 20px auto;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .hexagon-skill:hover {
        transform: rotate(5deg) scale(1.1);
        box-shadow: 0 10px 25px rgba(255, 107, 53, 0.4);
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animated-text {
        animation: fadeInUp 1s ease-out;
    }
    
    .sidebar-content {
        background: linear-gradient(180deg, #ff6b35 0%, #f7931e 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #fbcc9c !important;
    }
    
    .css-1lcbmhc {
        background-color: #fbcc9c !important;
    }
    
    /* Custom button styles */
    .stButton > button {
        background: linear-gradient(90deg, #ff6b35 0%, #f7931e 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 53, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ---- SIDEBAR NAVIGATION ----
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.title("🚀 Navigation")
    page = st.radio("Go to:", ["Home", "Skills Dashboard", "Projects Gallery", "AI Insights", "Contact"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Fun AI Fact of the Day
    st.markdown("---")
    st.subheader("🤖 AI Fact of the Day")
    ai_facts = [
        "The first neural network was created in 1943!",
        "GPT-3 has 175 billion parameters!",
        "Computer vision can now detect emotions!",
        "AI can generate art that sells for millions!",
        "Machine learning can predict weather patterns!"
    ]
    if st.button("🎲 New Fact"):
        st.session_state.ai_fact = random.choice(ai_facts)
    
    if 'ai_fact' not in st.session_state:
        st.session_state.ai_fact = random.choice(ai_facts)
    st.info(st.session_state.ai_fact)

# ---- HOME PAGE ----
if page == "Home":
    # Animated Header
    st.markdown("""
        <div class="main-header animated-text">
            <h1>👋 Hello! I'm Nancy Diana Gudavalli</h1>
            <h3>🤖 AI Strategist | 📊 Data Scientist | 💼 Business Analyst</h3>
            <p>📍 Scottsdale, Arizona | 📧 nancydiana97@gmail.com | 🔗 <a href="https://www.linkedin.com/in/nancydianagudavalli" target="_blank" style="color: white; text-decoration: underline;">LinkedIn</a></p>
        </div>
    """, unsafe_allow_html=True)
    
    # Interactive Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>6+</h3><p>Projects</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>3</h3><p>Degrees</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>3+</h3><p>Years Experience</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>∞</h3><p>Passion for AI</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interactive About Section with Tabs
    st.header("🌟 About Me")
    tab1, tab2, tab3 = st.tabs(["💼 Professional", "🎯 Mission", "🚀 Vision"])
    
    with tab1:
        st.write("""
        I'm a business-savvy AI professional with an MBA in Finance & Marketing, 
        a Postgraduate Diploma in Business Analytics, and certifications in NLP, Computer Vision, and Deep Learning.
        
        I currently run an AI agency that helps companies transform their operations with intelligent solutions.
        """)
    
    with tab2:
        st.write("""
        My mission is to bridge the gap between complex AI technologies and practical business applications.
        I believe AI should be accessible, ethical, and genuinely helpful to organizations of all sizes.
        """)
    
    with tab3:
        st.write("""
        I envision a future where AI seamlessly integrates into business processes, 
        enhancing human capabilities rather than replacing them, and driving sustainable growth.
        """)

# ---- SKILLS DASHBOARD ----
elif page == "Skills Dashboard":
    st.title("🧠 Skills Dashboard")
    
    # Interactive skill levels with animated skill cards
    skills_data = {
        'Technical Skills': {
            'Python': 95,
            'Machine Learning': 90,
            'Deep Learning': 85,
            'Computer Vision': 88,
            'NLP': 87,
            'SQL': 92
        },
        'AI/ML Frameworks': {
            'TensorFlow': 85,
            'PyTorch': 83,
            'Hugging Face': 90,
            'OpenCV': 88,
            'LangChain': 85
        },
        'Business Skills': {
            'Strategy': 95,
            'Analytics': 92,
            'Leadership': 88,
            'Communication': 94
        }
    }
    
    def create_interactive_skill_card(skill, level):
        return f"""
        <div class="skill-card-interactive">
            <div class="skill-name">{skill}</div>
            <div class="skill-level">{level}%</div>
            <div style="font-size: 12px; margin-top: 10px;">
                {'🔥' * (level // 20)} {'⭐' if level >= 90 else ''}
            </div>
        </div>
        """
    
    def create_animated_skill_bar(skill, level):
        return f"""
        <div class="skill-bar-container">
            <div class="skill-bar" style="width: {level}%; --skill-width: {level}%;">
                <span>{skill}</span>
                <span>{level}%</span>
            </div>
        </div>
        """
    
    # Toggle between different skill views
    col1, col2 = st.columns([1, 1])
    with col1:
        view_mode = st.selectbox("🎨 Choose View Style:", ["Interactive Cards", "Animated Bars", "Both"])
    
    for category, skills in skills_data.items():
        st.subheader(f"🎯 {category}")
        
        if view_mode == "Interactive Cards":
            # Display skills as interactive 3D cards
            cols = st.columns(3)
            skill_items = list(skills.items())
            
            for i, (skill, level) in enumerate(skill_items):
                with cols[i % 3]:
                    st.markdown(create_interactive_skill_card(skill, level), unsafe_allow_html=True)
        
        elif view_mode == "Animated Bars":
            # Display as animated skill bars
            for skill, level in skills.items():
                st.markdown(create_animated_skill_bar(skill, level), unsafe_allow_html=True)
        
        else:  # Both view
            # First show cards
            cols = st.columns(3)
            skill_items = list(skills.items())
            
            for i, (skill, level) in enumerate(skill_items):
                with cols[i % 3]:
                    st.markdown(create_interactive_skill_card(skill, level), unsafe_allow_html=True)
            
            # Then show bars
            st.markdown("#### Alternative View:")
            for skill, level in skills.items():
                st.markdown(create_animated_skill_bar(skill, level), unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Interactive Skills Comparison
    st.subheader("🔥 Skills Comparison Tool")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_category = st.selectbox("Select Category:", list(skills_data.keys()))
    with col2:
        comparison_type = st.selectbox("Compare by:", ["Level", "Experience", "Proficiency"])
    
    # Create interactive comparison chart
    selected_skills = skills_data[selected_category]
    skills_df = pd.DataFrame(list(selected_skills.items()), columns=['Skill', 'Level'])
    
    fig = px.bar(skills_df, x='Skill', y='Level', 
                 title=f'{selected_category} - {comparison_type} Comparison',
                 color='Level',
                 color_continuous_scale=['#ffb347', '#ff6b35', '#f7931e'])
    
    fig.update_layout(
        paper_bgcolor='rgba(251, 204, 156, 0.8)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ff6b35',
        xaxis_title_font_color='#ff6b35',
        yaxis_title_font_color='#ff6b35'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Skills Radar Chart with Orange colors
    st.subheader("🎯 Skills Assessment Radar")
    
    categories = ['Technical', 'ML/AI', 'Business', 'Leadership', 'Communication', 'Strategy']
    values = [95, 88, 92, 88, 94, 95]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Skills',
        line_color='rgb(255, 107, 53)',
        fillcolor='rgba(255, 107, 53, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Skills Assessment Overview",
        title_font_color='#ff6b35',
        paper_bgcolor='rgba(251, 204, 156, 0.8)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ---- PROJECTS GALLERY ----
elif page == "Projects Gallery":
    st.title("🚀 Projects Gallery")
    
    projects = [
        {
            "title": "🏃 Pose Estimation & Exercise Feedback System",
            "description": "Real-time form feedback using MediaPipe and OpenCV. Calculates joint angles and flags bad posture.",
            "tech": ["Python", "OpenCV", "MediaPipe", "Machine Learning"],
            "impact": "Improved workout form accuracy by 85%",
            "status": "Completed"
        },
        {
            "title": "🛡️ Phishing Detection (CISO Global)",
            "description": "Threat detection model using GNNs + LLMs. Proposed to executives as part of strategic roadmap.",
            "tech": ["Graph Neural Networks", "LLMs", "Python", "Security"],
            "impact": "Reduced false positives by 60%",
            "status": "In Production"
        },
        {
            "title": "🤖 Interview Prep Chatbot (Clemengers)",
            "description": "AI chatbot with speech-to-text and emotion detection to simulate university interview prep.",
            "tech": ["NLP", "Speech Recognition", "Emotion AI", "Chatbot"],
            "impact": "Helped 500+ students prepare",
            "status": "Completed"
        },
        {
            "title": "👋 Gesture-Controlled Wave-to-Scroll",
            "description": "Scroll web pages with hand gestures using OpenCV contour tracking.",
            "tech": ["Computer Vision", "OpenCV", "Gesture Recognition"],
            "impact": "Novel interaction method",
            "status": "Demo Available"
        },
        {
            "title": "🛒 Product Recommendations (Mindtree)",
            "description": "K-means + DNNs to cluster regions and generate store-specific product suggestions.",
            "tech": ["K-means", "Deep Learning", "Recommendation Systems"],
            "impact": "Increased sales by 23%",
            "status": "Deployed"
        },
        {
            "title": "🤲 Sign Language & Motion Detection",
            "description": "Real-time sign language detection using PyTorch and OpenCV.",
            "tech": ["PyTorch", "Computer Vision", "Accessibility"],
            "impact": "Supporting accessibility",
            "status": "Research"
        }
    ]
    
    for i, project in enumerate(projects):
        with st.expander(f"{project['title']} - {project['status']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(project['description'])
                st.write(f"**Impact:** {project['impact']}")
                
                # Tech stack badges
                st.write("**Technologies:**")
                tech_cols = st.columns(len(project['tech']))
                for j, tech in enumerate(project['tech']):
                    with tech_cols[j]:
                        st.markdown(f'<span style="background-color: #ff6b35; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;">{tech}</span>', unsafe_allow_html=True)
            
            with col2:
                # Project metrics visualization
                if project['status'] == "Completed":
                    st.success("✅ Completed")
                elif project['status'] == "In Production":
                    st.info("🚀 In Production")
                elif project['status'] == "Deployed":
                    st.success("📈 Deployed")
                else:
                    st.warning(f"🔬 {project['status']}")

# ---- AI INSIGHTS ----
elif page == "AI Insights":
    st.title("🧠 AI Insights & Thought Leadership")
    
    # AI Trend Visualization
    st.subheader("📈 AI Industry Trends")
    
    # Sample trend data
    trend_data = pd.DataFrame({
        'Year': [2020, 2021, 2022, 2023, 2024, 2025],
        'LLMs Adoption (%)': [5, 15, 35, 65, 85, 95],
        'Computer Vision (%)': [20, 30, 45, 60, 75, 85],
        'Business AI Investment ($B)': [10, 25, 50, 85, 125, 175]
    })
    
    fig = px.line(trend_data, x='Year', y=['LLMs Adoption (%)', 'Computer Vision (%)'], 
                  title='AI Technology Adoption Trends',
                  color_discrete_map={'LLMs Adoption (%)': '#ff6b35', 'Computer Vision (%)': '#f7931e'})
    
    fig.update_layout(
        paper_bgcolor='rgba(251, 204, 156, 0.8)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#ff6b35'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # AI Insights Cards
    st.subheader("💡 Weekly AI Insights")
    
    insights = [
        {
            "title": "🤖 The Future of Multi-Agent Systems",
            "content": "Multi-agent AI systems are revolutionizing how we approach complex problem-solving in enterprise environments.",
            "date": "July 15, 2025"
        },
        {
            "title": "🛡️ AI Safety in Production",
            "content": "Implementing robust safety measures and alignment strategies is crucial for responsible AI deployment.",
            "date": "July 10, 2025"
        },
        {
            "title": "🔄 RAG Systems Evolution",
            "content": "Retrieval-Augmented Generation is becoming more sophisticated with graph-based knowledge integration.",
            "date": "July 5, 2025"
        }
    ]
    
    for insight in insights:
        st.markdown(f"""
            <div class="project-card">
                <h4>{insight['title']}</h4>
                <p>{insight['content']}</p>
                <small>📅 {insight['date']}</small>
            </div>
        """, unsafe_allow_html=True)

# ---- CONTACT PAGE ----
elif page == "Contact":
    st.title("📬 Let's Connect!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Send me a message")
        
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Your Name", placeholder="Enter your full name")
            email = st.text_input("Your Email", placeholder="your.email@domain.com")
            company = st.text_input("Company (Optional)", placeholder="Your organization")
            
            message_type = st.selectbox(
                "What's this about?",
                ["General Inquiry", "Project Collaboration", "AI Consultation", "Speaking Opportunity", "Other"]
            )
            
            message = st.text_area("Message", placeholder="Tell me about your project or inquiry...", height=150)
            
            submitted = st.form_submit_button("🚀 Send Message")
            
            if submitted:
                if name and email and message:
                    # Simulate sending (in real app, you'd integrate with email service)
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    st.success("✅ Message sent successfully! I'll get back to you within 24 hours.")
                    st.balloons()
                else:
                    st.error("Please fill in all required fields.")
    
    with col2:
        st.subheader("Other ways to reach me")
        
        st.markdown("""
        📧 **Email:** nancydiana97@gmail.com
        
        🔗 **LinkedIn:** [Connect with me](https://www.linkedin.com/in/nancydianagudavalli)
        
        📍 **Location:** Scottsdale, Arizona
        
        ⏰ **Response Time:** Within 24 hours
        
        🌟 **Best for:** AI strategy discussions, collaboration opportunities, and technical consultations
        """)
        
        # Download Resume Button
        st.markdown("---")
        if st.button("📄 Download My Resume", key="resume_download"):
            st.info("Resume download would start here (add your PDF file to make this functional)")

# ---- FOOTER ----
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>© 2025 Nancy Diana Gudavalli | AI-Powered Solutions for Real-World Impact</p>
        <p> #AIINN Built using Streamlit and creativity</p>
    </div>
""", unsafe_allow_html=True)