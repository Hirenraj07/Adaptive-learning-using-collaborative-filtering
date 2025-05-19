import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import json

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_processor import DataProcessor
from model_trainer import ModelTrainer
from course_generator import CourseGenerator

def load_images(image_path):
    """Load and return image if it exists, otherwise return None"""
    try:
        return Image.open(image_path)
    except:
        return None

# Add verification checks at startup
if 'verified' not in st.session_state:
    st.session_state.verified = False
    st.session_state.credit_balance = 100  # Initial credits

# Add verification decorator
def verify_operation(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            st.session_state.credit_balance += 10  # Reward successful operation
            return result
        except Exception as e:
            st.session_state.credit_balance -= 5  # Deduct for errors
            st.error(f"Verification failed: {str(e)}")
            st.stop()
    return wrapper

@verify_operation
def load_model_safely():
    model_path = os.path.join('models', 'performance_predictor.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model not found - training new model")
    return joblib.load(model_path)

@verify_operation
def predict_performance_safely(model, data):
    return model.predict(data)

def main():
    """Main function to configure and run the Streamlit app."""
    
    # Set page config
    st.set_page_config(
        page_title="Adaptive Learning Platform",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state variables consistently
    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    
    if 'student_data' not in st.session_state:
        st.session_state.student_data = {}
    
    if 'prediction_results' not in st.session_state:
        st.session_state.prediction_results = None
    
    # Initialize credits system
    if 'credits' not in st.session_state:
        st.session_state.credits = 0
    
    # Initialize enrolled courses
    if 'enrolled_courses' not in st.session_state:
        st.session_state.enrolled_courses = []
    
    # Initialize completed_lessons tracking
    if 'completed_lessons' not in st.session_state:
        st.session_state.completed_lessons = {}
    
    # Define navigation functions
    def navigate_to(page):
        st.session_state.page = page
        st.rerun()
    
    # Apply custom CSS
    with open("frontend/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Navigation bar
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 20px; padding: 10px; background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
        <div style="flex: 1; text-align: center;">
            <h2 style="margin: 0; color: #333;">Adaptive Learning Platform</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu with horizontal buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Home", key="nav_home", use_container_width=True):
            navigate_to("Home")
    
    with col2:
        if st.button("Student Analysis", key="nav_student_analysis", use_container_width=True):
            navigate_to("Student Analysis")
    
    with col3:
        if st.button("Course Recommendations", key="nav_course_recommendations", use_container_width=True):
            navigate_to("Course Recommendations")
    
    with col4:
        if st.button("Data Insights", key="nav_data_insights", use_container_width=True):
            navigate_to("Data Insights")
    
    # Display persistent sidebar information
    st.sidebar.markdown("### 🎓 Learning Dashboard")
    st.sidebar.metric("Credits", st.session_state.credits)
    
    if st.session_state.enrolled_courses:
        st.sidebar.markdown("### 📚 My Courses")
        for course in st.session_state.enrolled_courses:
            if st.sidebar.button(f"Continue {course}", key=f"continue_{course}_sidebar"):
                st.session_state.active_course = course
                st.session_state.page = "Active Course"
                st.rerun()
    
    # Set app mode based on session state
    app_mode = st.session_state.page
    
    # Home page
    if app_mode == "Home":
        # Modern header
        st.markdown("""
        <div class="hero">
            <h1>Welcome to Your Adaptive Learning Platform</h1>
            <p>Personalized education tailored to your learning style</p>
        </div>
        """, unsafe_allow_html=True)
        
        # DEBUG MARKER: HOME PAGE CONTENT START
        st.write("DEBUG: Home page content is being rendered")
        
        # Get Started button (using Streamlit button)
        if st.button("Get Started", key="get_started_button", use_container_width=True):
            st.session_state.page = "Student Analysis"
            st.rerun()
        
        # Only show detailed course content if there are weak subjects in the student data
        has_weak_subjects = False
        if 'student_data' in st.session_state and st.session_state.student_data:
            # Check if any subject has a score below 60
            coding_score = st.session_state.student_data.get('Coding', 0)
            math_score = st.session_state.student_data.get('Math', 0)
            social_studies_score = st.session_state.student_data.get('Social Studies', 0)
            
            if coding_score < 60 or math_score < 60 or social_studies_score < 60:
                has_weak_subjects = True
                
                # Display message about remedial courses
                st.markdown("""
                <div class="card animated fadeIn">
                    <div class="widget-header">
                        <span>Recommended Remedial Courses</span>
                    </div>
                    <p>Based on your performance analysis, we've identified some areas where you could benefit from additional support. 
                    Here are detailed course materials tailored to help you improve in your weaker subjects.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Import course database
                from course_content import COURSE_DATABASE
                
                # Only show subjects where the student is weak
                weak_subjects = []
                if coding_score < 60:
                    weak_subjects.append("Coding")
                if math_score < 60:
                    weak_subjects.append("Mathematics")
                if social_studies_score < 60:
                    weak_subjects.append("Social Studies")
                
                # Create tabs for weak subjects only
                if weak_subjects:
                    subject_tabs = st.tabs(weak_subjects)
                    
                    for i, (subject, tab) in enumerate(zip(weak_subjects, subject_tabs)):
                        with tab:
                            # Get the corresponding subject from the database
                            db_subject = subject if subject in COURSE_DATABASE else "Coding" if subject == "Coding" else "Mathematics" if subject == "Math" else "Social Studies"
                            
                            if db_subject in COURSE_DATABASE:
                                course = COURSE_DATABASE[db_subject]
                                
                                # Course header
                                st.markdown(f"""
                                <div class="card animated fadeInUp" style="background: linear-gradient(135deg, #1E88E5 0%, #6A1B9A 100%); color: white; margin-bottom: 20px;">
                                    <h2>{course['title']}</h2>
                                    <p>{course['description'][:150]}...</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Display modules in a grid
                                cols = st.columns(min(2, len(course['modules'])))
                                
                                for j, module in enumerate(course['modules']):
                                    with cols[j % len(cols)]:
                                        st.markdown(f"""
                                        <div class="course-card animated fadeIn" style="animation-delay: {j*0.2}s">
                                            <div class="course-card-header" style="background-color: {'#4CAF50' if j % 3 == 0 else '#FF9800' if j % 3 == 1 else '#1E88E5'};">
                                                <h3 class="course-card-title">Module {j+1}: {module['title']}</h3>
                                            </div>
                                            <div class="course-card-body">
                                                <p><strong>Learning Objectives:</strong></p>
                                                <ul style="padding-left: 20px;">
                                                    {"".join([f'<li>{obj}</li>' for obj in module['learning_objectives'][:2]])}
                                                    {"<li>...and more</li>" if len(module['learning_objectives']) > 2 else ""}
                                                </ul>
                                                <p><strong>Topics:</strong> {len(module['content']['sections'])} sections</p>
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                        # Add a streamlit button for each module
                                        if st.button(f"Preview Module {j+1}", key=f"preview_module_{subject}_{j}"):
                                            st.session_state.selected_module = module
                                            st.rerun()
                
                    # Add example flashcards for interactive learning
                    st.markdown("""
                    <div class="card animated fadeInUp">
                        <div class="widget-header">
                            <span>Interactive Learning Tools</span>
                        </div>
                        <p>Try out these interactive flashcards to reinforce your learning.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Flashcard 1
                    flashcard1_front = st.expander("What is a variable in programming?", expanded=False)
                    with flashcard1_front:
                        st.write("A variable is a named storage location in a computer's memory that holds a value that can be changed during program execution.")
                    
                    # Flashcard 2
                    flashcard2_front = st.expander("What is the quadratic formula?", expanded=False)
                    with flashcard2_front:
                        st.write("x = (-b ± √(b² - 4ac)) / 2a")
                        st.write("Used to solve quadratic equations of the form ax² + bx + c = 0")
                    
                    # Flashcard 3
                    flashcard3_front = st.expander("What are the three branches of government?", expanded=False)
                    with flashcard3_front:
                        st.write("1. Legislative Branch (makes laws)")
                        st.write("2. Executive Branch (enforces laws)")
                        st.write("3. Judicial Branch (interprets laws)")
                    
                    # Practice Quiz using Streamlit components
                    st.subheader("Practice Quiz")
                    st.write("Which of these is NOT a programming language?")
                    
                    quiz_cols = st.columns(4)
                    
                    answer_provided = False
                    correct_answer = False
                    
                    with quiz_cols[0]:
                        if st.button("HTML", key="quiz_html"):
                            answer_provided = True
                            correct_answer = False
                    
                    with quiz_cols[1]:
                        if st.button("Python", key="quiz_python"):
                            answer_provided = True
                            correct_answer = False
                    
                    with quiz_cols[2]:
                        if st.button("Photoshop", key="quiz_photoshop"):
                            answer_provided = True
                            correct_answer = True
                    
                    with quiz_cols[3]:
                        if st.button("JavaScript", key="quiz_javascript"):
                            answer_provided = True
                            correct_answer = False
                    
                    if answer_provided:
                        if correct_answer:
                            st.success("✓ Correct! Photoshop is a graphics editing software, not a programming language.")
                            
                            # Show achievement
                            st.balloons()
                        else:
                            st.error("✗ Incorrect. The correct answer is Photoshop, which is a graphics editing software, not a programming language.")
                    
                    # Module completion button
                    if st.button("Complete Sample Module", key="complete_module"):
                        st.balloons()
                        st.success("🏆 Achievement Unlocked! Congratulations on completing the module!")
        
        # If no weak subjects or no student data, show normal home page content
        if not has_weak_subjects:
            # Overview of features
            st.markdown("""
            <div class="hero-container">
                <h1 class="hero-title">Welcome to Adaptive Learning</h1>
                <p class="hero-subtitle">A personalized learning experience that adapts to your unique strengths and learning style</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Get Started with Your Analysis", key="get_started_analysis"):
                st.session_state.page = "Student Analysis"
                st.rerun()
            
            # Feature highlights
            st.markdown("<h2>Key Features</h2>", unsafe_allow_html=True)
            
            feature_col1, feature_col2 = st.columns(2)
            
            with feature_col1:
                st.markdown("""
                <div class="card animated fadeIn">
                    <h3>🧠 Adaptive Learning</h3>
                    <p>Our AI-powered system adapts to your learning pace and style, identifying areas where you need more support and recommending personalized courses.</p>
                </div>
                
                <div class="card animated fadeIn" style="animation-delay: 0.2s">
                    <h3>📊 Performance Analytics</h3>
                    <p>Get detailed insights into your academic performance with interactive charts and visualizations that track your progress over time.</p>
                </div>
                """, unsafe_allow_html=True)
                
            with feature_col2:
                st.markdown("""
                <div class="card animated fadeIn" style="animation-delay: 0.4s">
                    <h3>🏆 Gamified Learning</h3>
                    <p>Earn points, badges, and rewards as you complete courses and improve your scores, making learning more engaging and motivating.</p>
                </div>
                
                <div class="card animated fadeIn" style="animation-delay: 0.6s">
                    <h3>📱 Responsive Design</h3>
                    <p>Access your personalized learning platform from any device with our responsive design that works seamlessly on desktops, tablets, and smartphones.</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Call to action
            st.markdown("""
            <div style="text-align: center; margin: 40px 0;">
                <p style="font-size: 1.2rem; margin-bottom: 20px;">Ready to start your personalized learning journey?</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Analyze Your Performance", key="analyze_performance_btn"):
                st.session_state.page = "Student Analysis"
                st.rerun()
                
        # ===== FLASHCARDS SECTION =====
        st.markdown("---")
        st.subheader("📝 Interactive Study Flashcards")
        st.info("DEBUG: Flashcard section should be visible below")
        
        # Create tabs for flashcard subjects
        flashcard_subjects = ["Coding", "Mathematics", "Social Studies"]
        flashcard_tabs = st.tabs(flashcard_subjects)
        
        # Sample flashcard data
        sample_flashcards = {
            "Coding": [
                {"question": "What does HTML stand for?", "answer": "HyperText Markup Language"},
                {"question": "What is a variable?", "answer": "A named storage location in memory"},
                {"question": "What is the difference between '==' and '==='?", "answer": "'==' compares values, '===' compares values and types"}
            ],
            "Mathematics": [
                {"question": "What is the Pythagorean theorem?", "answer": "a² + b² = c²"},
                {"question": "What is a prime number?", "answer": "A number divisible only by 1 and itself"},
                {"question": "What is the derivative of f(x) = x²?", "answer": "f'(x) = 2x"}
            ],
            "Social Studies": [
                {"question": "What is democracy?", "answer": "A system of government by the whole population or eligible members"},
                {"question": "What was the Renaissance?", "answer": "A period of European cultural, artistic, political and scientific 'rebirth'"},
                {"question": "What is economics?", "answer": "The study of how societies use scarce resources to produce and distribute goods"}
            ]
        }
        
        # Display flashcards in each tab
        for i, tab in enumerate(flashcard_tabs):
            with tab:
                subject = flashcard_subjects[i]
                
                # Make sure we have valid flashcards for this subject
                if subject in sample_flashcards:
                    flashcards = sample_flashcards[subject]
                    
                    # Display count of flashcards
                    st.write(f"DEBUG: {len(flashcards)} flashcards found for {subject}")
                    
                    # Initialize session state for this subject if not exists
                    if f"{subject}_card_index" not in st.session_state:
                        st.session_state[f"{subject}_card_index"] = 0
                    
                    # Get current card index
                    card_idx = st.session_state[f"{subject}_card_index"]
                    
                    # Ensure index is valid
                    if card_idx >= len(flashcards):
                        card_idx = 0
                        st.session_state[f"{subject}_card_index"] = 0
                    
                    # Current flashcard
                    current_card = flashcards[card_idx]
                    
                    # Show card info
                    st.write(f"Card {card_idx + 1} of {len(flashcards)}")
                    
                    # Display card in a container
                    with st.container():
                        st.markdown("### Question")
                        st.info(current_card["question"])
                        
                        # Toggle for showing/hiding answer
                        answer_key = f"show_answer_{subject}_home"
                        if answer_key not in st.session_state:
                            st.session_state[answer_key] = False
                        
                        # Toggle button
                        toggle_label = "Hide Answer" if st.session_state[answer_key] else "Show Answer"
                        if st.button(toggle_label, key=f"toggle_{subject}_home_{card_idx}"):
                            st.session_state[answer_key] = not st.session_state[answer_key]
                            st.rerun()
                        
                        # Display answer if toggled
                        if st.session_state[answer_key]:
                            st.markdown("### Answer")
                            st.success(current_card["answer"])
                    
                    # Navigation controls
                    cols = st.columns(2)
                    with cols[0]:
                        prev_disabled = card_idx <= 0
                        if st.button("⬅️ Previous", key=f"prev_{subject}_home_{card_idx}", disabled=prev_disabled):
                            st.session_state[f"{subject}_card_index"] = max(0, card_idx - 1)
                            # Reset answer visibility
                            st.session_state[answer_key] = False
                            st.rerun()
                    
                    with cols[1]:
                        next_disabled = card_idx >= len(flashcards) - 1
                        if st.button("Next ➡️", key=f"next_{subject}_home_{card_idx}", disabled=next_disabled):
                            st.session_state[f"{subject}_card_index"] = min(len(flashcards) - 1, card_idx + 1)
                            # Reset answer visibility
                            st.session_state[answer_key] = False
                            st.rerun()
                else:
                    st.warning(f"No flashcards available for {subject}")
    
    # Student Analysis page
    elif app_mode == "Student Analysis":
        # Modern header with progress tracking
        st.markdown("""
        <div class="card" style="background: linear-gradient(135deg, #1E88E5 0%, #4CAF50 100%); color: white; margin-bottom: 20px;">
            <h1>📊 Student Performance Analysis</h1>
            <p>Enter your scores to get personalized AI insights into your academic performance</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Direct approach - no tabs
        # Modern data input form
        st.markdown("""
        <div class="card">
            <div class="widget-header">
                <span>Student Information</span>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            student_id = st.text_input("Student ID", value="S-"+str(np.random.randint(1000, 9999)))
            coding_score = st.slider("Coding Score", 0, 100, 70)
            time_spent = st.slider("Weekly Study Hours", 1, 40, 15)
            
        with col2:
            student_name = st.text_input("Name (Optional)", value="")
            math_score = st.slider("Math Score", 0, 100, 75)
            social_studies_score = st.slider("Social Studies Score", 0, 100, 65)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Add Load Student Data option
        st.markdown("""
        <div class="card" style="margin-top: 20px;">
            <div class="widget-header">
                <span>Sample Data</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a dropdown for sample student profiles
        sample_profiles = {
            "Select a profile": {"Coding": 70, "Math": 75, "Social Studies": 65, "Time Spent": 15},
            "Struggling Student": {"Coding": 45, "Math": 55, "Social Studies": 50, "Time Spent": 10},
            "Average Student": {"Coding": 70, "Math": 68, "Social Studies": 72, "Time Spent": 15},
            "Advanced Student": {"Coding": 90, "Math": 88, "Social Studies": 85, "Time Spent": 20}
        }
        
        selected_profile = st.selectbox("Load Sample Student Profile", options=list(sample_profiles.keys()))
        
        if st.button("Load Selected Profile") and selected_profile != "Select a profile":
            profile_data = sample_profiles[selected_profile]
            # Update the session state values
            coding_score = profile_data["Coding"]
            math_score = profile_data["Math"]
            social_studies_score = profile_data["Social Studies"]
            time_spent = profile_data["Time Spent"]
            # Force a rerun to update the UI
            st.session_state.temp_profile = {
                "Coding": coding_score,
                "Math": math_score,
                "Social Studies": social_studies_score,
                "time_spent": time_spent
            }
            st.rerun()
        
        # Create a nice styled submit button
        st.markdown("""
        <style>
        div.stButton > button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            height: 3em;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Simplified analysis function - direct approach
        if st.button("Analyze Performance"):
            # Save student data to session state
            st.session_state.student_data = {
                'Student ID': student_id,
                'Name': student_name,
                'Coding': coding_score,
                'Math': math_score,
                'Social Studies': social_studies_score,
                'time_spent': time_spent,
                'average_score': (coding_score + math_score + social_studies_score) / 3
            }
            
            # FIXED APPROACH: Use direct prediction values
            avg_score = (coding_score + math_score + social_studies_score) / 3
            # Simple prediction model: adjust scores based on study time
            predicted_score = min(100, avg_score * (1 + (time_spent - 15) / 100))
            
            # Display immediate results
            st.markdown("""
            <div class="card">
                <div class="widget-header">
                    <span>Academic Performance Prediction</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                performance_level = "Excellent" if predicted_score >= 85.0 else "Good" if predicted_score >= 70.0 else "Needs Improvement"
                performance_color = "#4CAF50" if predicted_score >= 85.0 else "#FF9800" if predicted_score >= 70.0 else "#F44336"
                
                st.markdown(f"""
                <div class="card">
                    <h2 style="text-align: center; color: {performance_color}; font-size: 3rem;">{predicted_score:.1f}%</h2>
                    <p style="text-align: center;">Predicted Score</p>
                    <div style="height: 10px; background-color: #f0f0f0; border-radius: 5px; margin: 15px 0;">
                        <div style="height: 10px; width: {predicted_score}%; background-color: {performance_color}; border-radius: 5px;"></div>
                    </div>
                    <p style="text-align: center; font-weight: bold; color: {performance_color};">Performance Level: {performance_level}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Display improvement metrics
                improvement = predicted_score - avg_score
                improvement_text = f"↑ +{improvement:.1f}%" if improvement > 0 else f"↓ {improvement:.1f}%"
                improvement_color = "#4CAF50" if improvement > 0 else "#F44336"
                
                st.markdown(f"""
                <div class="card">
                    <h3 style="text-align: center;">Score Improvement</h3>
                    <h2 style="text-align: center; color: {improvement_color}; font-size: 2.5rem;">{improvement_text}</h2>
                    <div style="display: flex; align-items: center; justify-content: center; margin-top: 15px;">
                        <div style="text-align: center; flex: 1;">
                            <p>Current Average</p>
                            <h3>{avg_score:.1f}%</h3>
                        </div>
                        <div style="font-size: 1.5rem; margin: 0 15px;">→</div>
                        <div style="text-align: center; flex: 1;">
                            <p>Predicted Score</p>
                            <h3>{predicted_score:.1f}%</h3>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Subject-specific insights
            st.subheader("Subject-Specific Insights")
            
            subject_insights = {
                "Coding": {
                    "score": coding_score,
                    "description": "Strong programming fundamentals" if coding_score >= 80 else 
                                 "Good coding skills" if coding_score >= 60 else
                                 "Needs improvement in coding concepts",
                    "recommendation": "Advanced algorithms & data structures" if coding_score >= 80 else
                                    "Practice intermediate programming problems" if coding_score >= 60 else
                                    "Review basic programming concepts",
                    "icon": "💻" if coding_score >= 80 else "📱" if coding_score >= 60 else "🔍"
                },
                "Math": {
                    "score": math_score,
                    "description": "Excellent mathematical ability" if math_score >= 80 else 
                                 "Good math foundation" if math_score >= 60 else
                                 "Requires more practice in math",
                    "recommendation": "Explore advanced calculus and statistics" if math_score >= 80 else
                                    "Practice more problem-solving in algebra" if math_score >= 60 else
                                    "Focus on strengthening core math concepts",
                    "icon": "🧮" if math_score >= 80 else "📊" if math_score >= 60 else "📏"
                },
                "Social Studies": {
                    "score": social_studies_score,
                    "description": "Outstanding social science knowledge" if social_studies_score >= 80 else 
                                 "Good understanding of social concepts" if social_studies_score >= 60 else
                                 "Needs improvement in social studies",
                    "recommendation": "Explore specialized social science topics" if social_studies_score >= 80 else
                                    "Read more about world history and cultures" if social_studies_score >= 60 else
                                    "Review fundamental social studies concepts",
                    "icon": "🌍" if social_studies_score >= 80 else "📚" if social_studies_score >= 60 else "🗿"
                }
            }
            
            for subject, insight in subject_insights.items():
                score_color = "#4CAF50" if insight["score"] >= 80 else "#FF9800" if insight["score"] >= 60 else "#F44336"
                
                st.markdown(f"""
                <div class="card" style="margin-bottom: 15px; border-left: 4px solid {score_color};">
                    <div style="display: flex; align-items: center;">
                        <div style="font-size: 2rem; margin-right: 15px;">{insight["icon"]}</div>
                        <div>
                            <h3>{subject}: {insight["score"]}%</h3>
                            <p><strong>{insight["description"]}</strong></p>
                            <p>Recommendation: {insight["recommendation"]}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Add a button to view detailed course recommendations
            if st.button("View Recommended Courses"):
                st.session_state.page = "Course Recommendations"
                st.rerun()
    
    # Course Recommendations page
    elif app_mode == "Course Recommendations":
        # Check if analysis has been performed
        if 'student_data' not in st.session_state:
            st.warning("Please analyze your performance first in the Student Analysis page.")
            if st.button("Go to Student Analysis"):
                st.session_state.page = "Student Analysis"
                st.rerun()
        else:
            # Modern header
            st.markdown("""
            <div class="card" style="background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%); color: white; margin-bottom: 20px;">
                <h1>📚 Personalized Course Recommendations</h1>
                <p>Custom learning path based on your academic performance</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get student data from session state
            student_data = st.session_state.student_data
            
            # Display student overview
            st.markdown(f"""
            <div class="card">
                <div class="widget-header">
                    <span>Student Overview</span>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 2.5rem; margin-right: 20px;">👨‍🎓</div>
                    <div>
                        <h3>{student_data.get('Name', 'Student')} ({student_data.get('Student ID', 'Unknown')})</h3>
                        <p>Average Score: <strong>{student_data.get('average_score', 0):.1f}%</strong></p>
                        <p>Weekly Study Hours: <strong>{student_data.get('time_spent', 0)} hours</strong></p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate course recommendations based on performance
            st.markdown("""
            <div class="card">
                <div class="widget-header">
                    <span>Recommended Courses</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate simple course recommendations
            subject_scores = {
                "Coding": student_data.get('Coding', 0),
                "Math": student_data.get('Math', 0),
                "Social Studies": student_data.get('Social Studies', 0)
            }
            
            # Sort subjects by scores (ascending, focus on weakest first)
            sorted_subjects = sorted(subject_scores.items(), key=lambda x: x[1])
            
            # Display recommendations with animations
            for i, (subject, score) in enumerate(sorted_subjects):
                priority = "High" if i == 0 else "Medium" if i == 1 else "Low"
                priority_color = "#F44336" if i == 0 else "#FF9800" if i == 1 else "#4CAF50"
                
                if score < 60:
                    level = "Beginner"
                    icon = "🔰"
                elif score < 80:
                    level = "Intermediate"
                    icon = "🏅"
                else:
                    level = "Advanced"
                    icon = "🏆"
                
                course_info = {
                    "Coding": {
                        "Beginner": "Introduction to Programming Concepts",
                        "Intermediate": "Data Structures and Algorithms",
                        "Advanced": "Advanced Software Engineering and Architecture"
                    },
                    "Math": {
                        "Beginner": "Fundamentals of Mathematics",
                        "Intermediate": "Advanced Algebra and Calculus",
                        "Advanced": "Advanced Statistics and Number Theory"
                    },
                    "Social Studies": {
                        "Beginner": "Introduction to World History and Geography",
                        "Intermediate": "Cultural Studies and Current Events",
                        "Advanced": "Political Science and Global Economics"
                    }
                }
                
                # Choose the appropriate course based on subject and level
                course_name = course_info[subject][level]
                
                # Set animation delay
                animation_delay = 0.3 * (i + 1)
                
                st.markdown(f"""
                <div class="card course-card" style="border-left: 5px solid {priority_color}; animation-delay: {animation_delay}s;">
                    <div style="display: flex; align-items: center;">
                        <div style="font-size: 2.5rem; margin-right: 20px;">{icon}</div>
                        <div style="flex-grow: 1;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h3>{course_name}</h3>
                                <span style="background-color: {priority_color}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem;">{priority} Priority</span>
                            </div>
                            <p><strong>Subject:</strong> {subject} (Current Score: {score}%)</p>
                            <p><strong>Level:</strong> {level}</p>
                            <div class="progress-bar-container">
                                <div class="progress-bar" style="width: {score}%; background-color: {priority_color};"></div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Actual working buttons using Streamlit
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"View Syllabus", key=f"syllabus_{subject}_{i}"):
                        if 'active_syllabus' not in st.session_state:
                            st.session_state.active_syllabus = {}
                        
                        # Toggle the active syllabus state
                        current = st.session_state.active_syllabus.get(subject, False)
                        st.session_state.active_syllabus[subject] = not current
                        st.rerun()
                
                with col2:
                    if st.button(f"Enroll Now", key=f"enroll_{subject}_{i}"):
                        # Check if already enrolled to avoid duplicates
                        if subject not in st.session_state.enrolled_courses:
                            st.session_state.enrolled_courses.append(subject)
                            st.session_state.credits += 100
                            st.success(f"Successfully enrolled in {course_name}! +100 credits added.")
                        else:
                            st.info(f"You are already enrolled in {course_name}.")
                        st.rerun()
                
                # Show syllabus if active
                if 'active_syllabus' in st.session_state and st.session_state.active_syllabus.get(subject, False):
                    st.markdown("""
                    <div class="card" style="background-color: #f9f9f9; margin-top: 10px; margin-bottom: 20px;">
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"### 📚 {course_name} - Syllabus")
                    st.markdown(f"**Duration:** 12 weeks")
                    st.markdown(f"**Prerequisites:** None")
                    
                    st.markdown("#### Course Modules:")
                    st.markdown("""
                    1. **Introduction to {subject}**  
                       Basic concepts and foundations
                    
                    2. **Core Principles and Methods**  
                       Understanding key frameworks and approaches
                    
                    3. **Advanced Topics in {subject}**  
                       Specialized knowledge and techniques
                    
                    4. **Practical Applications**  
                       Real-world problem solving and projects
                    """.format(subject=subject))
                    
                    st.markdown("#### Assessment Methods:")
                    st.markdown("""
                    - Weekly quizzes (30%)
                    - Mid-term examination (30%)
                    - Final project (40%)
                    """)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Add button to start the course
                    start_key = f"start_{subject}_{i}"
                    if st.button(f"Start Course", key=start_key):
                        st.session_state.active_course = subject
                        st.session_state.page = "Active Course"
                        # Debug logging
                        st.info(f"Starting course: {subject}. Changing page to Active Course.")
                        st.rerun()
                
                # Learning path visualization
                st.markdown("""
                <div class="card">
                    <div class="widget-header">
                        <span>Learning Path Visualization</span>
                    </div>
                    <div class="learning-path">
                        <div class="path-node current">
                            <div class="node-icon">📋</div>
                            <div class="node-label">Assessment</div>
                        </div>
                        <div class="path-connector"></div>
                        <div class="path-node">
                            <div class="node-icon">📚</div>
                            <div class="node-label">Core Courses</div>
                        </div>
                        <div class="path-connector"></div>
                        <div class="path-node">
                            <div class="node-icon">🔬</div>
                            <div class="node-label">Specialized Study</div>
                        </div>
                        <div class="path-connector"></div>
                        <div class="path-node">
                            <div class="node-icon">🎯</div>
                            <div class="node-label">Final Project</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display credits if enrolled
                if 'enrolled_courses' in st.session_state and subject in st.session_state.enrolled_courses:
                    st.success(f"✓ Enrolled in {subject} course")
            
            # Add a flashcard section to the end of the Course Recommendations page
            st.markdown("---")
            st.subheader("📝 Study Flashcards")
            st.write("Practice with these flashcards to enhance your learning")
            
            # Create tabs for flashcard subjects
            flashcard_tabs_rec = st.tabs(["Coding", "Mathematics", "Social Studies"])
            
            # Sample flashcard data
            sample_flashcards = {
                "Coding": [
                    {"question": "What does HTML stand for?", "answer": "HyperText Markup Language"},
                    {"question": "What is a variable?", "answer": "A named storage location in memory"},
                    {"question": "What is the difference between '==' and '==='?", "answer": "'==' compares values, '===' compares values and types"}
                ],
                "Mathematics": [
                    {"question": "What is the Pythagorean theorem?", "answer": "a² + b² = c²"},
                    {"question": "What is a prime number?", "answer": "A number divisible only by 1 and itself"},
                    {"question": "What is the derivative of f(x) = x²?", "answer": "f'(x) = 2x"}
                ],
                "Social Studies": [
                    {"question": "What is democracy?", "answer": "A system of government by the whole population or eligible members"},
                    {"question": "What was the Renaissance?", "answer": "A period of European cultural, artistic, political and scientific 'rebirth'"},
                    {"question": "What is economics?", "answer": "The study of how societies use scarce resources to produce and distribute goods"}
                ]
            }
            
            # Display flashcards in each tab
            for i, tab in enumerate(flashcard_tabs_rec):
                with tab:
                    subject = ["Coding", "Mathematics", "Social Studies"][i]
                    
                    # Make sure we have valid flashcards for this subject
                    if subject in sample_flashcards:
                        flashcards = sample_flashcards[subject]
                        
                        # Initialize session state for this subject if not exists
                        if f"{subject}_rec_index" not in st.session_state:
                            st.session_state[f"{subject}_rec_index"] = 0
                        
                        # Get current card index
                        card_idx = st.session_state[f"{subject}_rec_index"]
                        
                        # Ensure index is valid
                        if card_idx >= len(flashcards):
                            card_idx = 0
                            st.session_state[f"{subject}_rec_index"] = 0
                        
                        # Current flashcard
                        current_card = flashcards[card_idx]
                        
                        # Show card info
                        st.write(f"Card {card_idx + 1} of {len(flashcards)}")
                        
                        # Display card in a container
                        with st.container():
                            st.markdown("### Question")
                            st.info(current_card["question"])
                            
                            # Toggle for showing/hiding answer
                            answer_key = f"show_answer_{subject}_rec"
                            if answer_key not in st.session_state:
                                st.session_state[answer_key] = False
                            
                            # Toggle button
                            toggle_label = "Hide Answer" if st.session_state[answer_key] else "Show Answer"
                            if st.button(toggle_label, key=f"toggle_{subject}_rec_{card_idx}"):
                                st.session_state[answer_key] = not st.session_state[answer_key]
                                st.rerun()
                            
                            # Display answer if toggled
                            if st.session_state[answer_key]:
                                st.markdown("### Answer")
                                st.success(current_card["answer"])
                        
                        # Navigation controls
                        cols = st.columns(2)
                        with cols[0]:
                            prev_disabled = card_idx <= 0
                            if st.button("⬅️ Previous", key=f"prev_{subject}_rec_{card_idx}", disabled=prev_disabled):
                                st.session_state[f"{subject}_rec_index"] = max(0, card_idx - 1)
                                # Reset answer visibility
                                st.session_state[answer_key] = False
                                st.rerun()
                        
                        with cols[1]:
                            next_disabled = card_idx >= len(flashcards) - 1
                            if st.button("Next ➡️", key=f"next_{subject}_rec_{card_idx}", disabled=next_disabled):
                                st.session_state[f"{subject}_rec_index"] = min(len(flashcards) - 1, card_idx + 1)
                                # Reset answer visibility
                                st.session_state[answer_key] = False
                                st.rerun()
                    else:
                        st.warning(f"No flashcards available for {subject}")
    
    # Data Insights page
    elif app_mode == "Data Insights":
        st.header("📊 Data Insights")
        
        # Check if visualizations exist
        vis_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'visualizations')
        
        # Create tabs for different visualizations
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Performance Distribution", 
            "Subject Performance", 
            "Time vs. Performance",
            "Adaptive Complexity",
            "Strengths & Weaknesses"
        ])
        
        with tab1:
            img = load_images(os.path.join(vis_dir, 'performance_distribution.png'))
            if img:
                st.image(img, caption="Distribution of Students Across Performance Tiers", use_column_width=True)
            else:
                st.warning("Visualization not available. Please run the pipeline script first.")
                st.code("python run_pipeline.py", language="bash")
        
        with tab2:
            img = load_images(os.path.join(vis_dir, 'subject_performance.png'))
            if img:
                st.image(img, caption="Average Performance by Subject", use_column_width=True)
            else:
                st.warning("Visualization not available. Please run the pipeline script first.")
        
        with tab3:
            img = load_images(os.path.join(vis_dir, 'time_vs_performance.png'))
            if img:
                st.image(img, caption="Correlation: Time Spent vs. Performance", use_column_width=True)
            else:
                st.warning("Visualization not available. Please run the pipeline script first.")
        
        with tab4:
            img = load_images(os.path.join(vis_dir, 'adaptive_complexity.png'))
            if img:
                st.image(img, caption="Adaptive Learning: Course Parameters by Performance Tier", use_column_width=True)
            else:
                st.warning("Visualization not available. Please run the pipeline script first.")
        
        with tab5:
            img = load_images(os.path.join(vis_dir, 'subject_strengths_weaknesses.png'))
            if img:
                st.image(img, caption="Subject Performance Distribution (Strengths & Weaknesses)", use_column_width=True)
            else:
                st.warning("Visualization not available. Please run the pipeline script first.")
    
    # Active Course page
    elif app_mode == "Active Course":
        if 'active_course' in st.session_state:
            subject = st.session_state.active_course
            st.title(f"{subject} Course")
            
            # Course progress tracking
            if f'{subject}_progress' not in st.session_state:
                st.session_state[f'{subject}_progress'] = 0
            
            progress = st.session_state[f'{subject}_progress']
            
            # Display course modules
            st.header("Course Modules")
            
            # Module data based on the subject
            modules = [
                {"title": f"Introduction to {subject}", "lessons": 4, "completed": min(progress, 4)},
                {"title": f"Core Principles of {subject}", "lessons": 5, "completed": max(0, min(progress - 4, 5))},
                {"title": f"Advanced Topics in {subject}", "lessons": 6, "completed": max(0, min(progress - 9, 6))},
                {"title": f"Practical Applications of {subject}", "lessons": 5, "completed": max(0, min(progress - 15, 5))}
            ]
            
            # Display course progress
            total_lessons = sum(m["lessons"] for m in modules)
            st.progress(progress / total_lessons)
            st.caption(f"Progress: {progress}/{total_lessons} lessons completed ({int(progress/total_lessons*100)}%)")
            
            # Display each module
            for i, module in enumerate(modules):
                with st.expander(f"Module {i+1}: {module['title']} ({module['completed']}/{module['lessons']} lessons)", 
                               expanded=i == progress // 5):
                    st.markdown(f"**Description:** This module covers the essential concepts of {module['title'].lower()}.")
                    
                    # Show lessons within the module
                    for j in range(module["lessons"]):
                        lesson_num = j + 1
                        lesson_overall = sum(m["lessons"] for m in modules[:i]) + j
                        
                        # Check if the lesson is completed
                        lesson_completed = lesson_overall < progress
                        
                        # Current lesson
                        is_current = lesson_overall == progress
                        
                        # Create a style based on status
                        if lesson_completed:
                            icon = "✅"
                            button_text = "Review Lesson"
                        elif is_current:
                            icon = "📝"
                            button_text = "Start Lesson"
                        else:
                            icon = "🔒"
                            button_text = "Locked"
                        
                        st.markdown(f"{icon} **Lesson {lesson_num}:** Core concept {lesson_num}")
                        
                        # Add button for lesson
                        if lesson_completed or is_current:
                            if st.button(button_text, key=f"lesson_{subject}_{i}_{j}"):
                                st.session_state[f'active_lesson_{subject}'] = lesson_overall
                                st.session_state[f'lesson_view_{subject}'] = True
                                st.rerun()
            
            # Display active lesson if there is one
            if f'lesson_view_{subject}' in st.session_state and st.session_state[f'lesson_view_{subject}']:
                lesson_index = st.session_state[f'active_lesson_{subject}']
                
                st.markdown("---")
                st.header(f"Lesson {lesson_index + 1}")
                
                # Determine which module this lesson belongs to
                module_index = 0
                module_lesson_index = lesson_index
                for i, module in enumerate(modules):
                    if module_lesson_index >= module["lessons"]:
                        module_lesson_index -= module["lessons"]
                        module_index += 1
                    else:
                        break
                
                st.subheader(f"From Module {module_index + 1}: {modules[module_index]['title']}")
                
                # Lesson content - this would come from your course content system
                st.markdown(f"""
                ### Lesson Objectives
                
                By the end of this lesson, you will be able to:
                - Understand the key concepts of this topic
                - Apply the principles to solve problems
                - Analyze real-world scenarios
                
                ### Lesson Content
                
                This is the main content of lesson {lesson_index + 1} in the {subject} course.
                It includes important principles, examples, and practice problems.
                
                ### Practice Exercise
                """)
                
                # Simple quiz to complete the lesson
                st.radio("What is the most important concept in this lesson?", 
                         ["Concept A", "Concept B", "Concept C", "All of the above"],
                         index=3,
                         key=f"quiz_{subject}_{lesson_index}")
                
                complete_key = f"complete_{subject}_{lesson_index}"
                if st.button("Complete Lesson", key=complete_key):
                    # Mark the lesson as completed if it's the current one
                    if lesson_index == progress:
                        # Update progress
                        st.session_state[f'{subject}_progress'] = progress + 1
                        
                        # Add credits for lesson completion
                        st.session_state.credits = st.session_state.get('credits', 0) + 25
                        
                        # Store lesson completion in completed_lessons
                        lesson_id = f"{subject}_lesson_{lesson_index}"
                        st.session_state.completed_lessons[lesson_id] = True
                        
                        st.success(f"Lesson completed successfully! +25 credits earned. Your total: {st.session_state.credits} credits")
                    else:
                        st.info("Lesson reviewed.")
                    
                    st.session_state[f'lesson_view_{subject}'] = False
                    st.rerun()
                
                if st.button("Back to Course"):
                    st.session_state[f'lesson_view_{subject}'] = False
                    st.rerun()
            
            # Button to return to main menu
            if st.button("← Back to Dashboard"):
                st.session_state.page = "Home"
                st.rerun()
        else:
            st.error("No active course selected")
            if st.button("Return to Dashboard"):
                st.session_state.page = "Home"
                st.rerun()
    
    # About page
    elif app_mode == "About":
        st.header("ℹ️ About the Adaptive Learning System")
        
        st.markdown("""
        ### System Overview
        
        The Adaptive Learning System is an AI-powered educational tool designed to provide personalized learning
        experiences for students. By analyzing performance data across various subjects, the system identifies
        strengths and weaknesses, categorizes students into performance tiers, and generates targeted courses
        to address areas needing improvement.
        
        ### Key Components
        
        1. **Data Processing Module**: Loads and preprocesses student performance data, calculating average scores
           and categorizing students into performance tiers.
           
        2. **AI Model**: Uses Random Forest classification to predict student performance tiers based on
           subject scores and engagement metrics.
           
        3. **Course Recommendation Engine**: Generates personalized course recommendations based on identified
           weak subjects, adjusting difficulty and focus areas according to performance levels.
           
        4. **Visualization System**: Creates visual representations of student performance distributions,
           subject-specific strengths and weaknesses, and the relationship between time spent and performance.
           
        5. **Reward System**: Motivates students through achievement badges, points, and special rewards upon
           course completion.
           
        ### Technical Implementation
        
        - **Backend**: Python, scikit-learn, pandas, numpy
        - **Frontend**: Streamlit
        - **Visualization**: Matplotlib, Seaborn
        - **Data Storage**: CSV files (can be extended to databases)
        
        ### Future Enhancements
        
        - Integration with real-time learning management systems
        - Incorporation of natural language processing for text-based assessments
        - Expanded interactive learning tools including simulations and quizzes
        - Mobile app version for on-the-go learning
        - Collaborative learning features and peer comparison analytics
        """)
        
    # Apply custom styling
    st.markdown("""
    <style>
        /* Global styles */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
        }
        
        /* Hero section */
        .hero-unit {
            background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
            padding: 40px;
            border-radius: 10px;
            color: white;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .hero-content h1 {
            font-size: 2.5rem;
            margin-bottom: 15px;
        }
        
        /* Card styles */
        .card {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .widget-header {
            border-bottom: 1px solid #f0f0f0;
            margin-bottom: 15px;
            padding-bottom: 10px;
            font-size: 1.2rem;
            font-weight: 600;
            color: #333;
        }
        
        /* Course cards */
        .course-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
            height: 100%;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .course-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        
        .course-card-header {
            padding: 15px;
            color: white;
        }
        
        .course-card-title {
            margin: 0;
            font-size: 1.1rem;
            font-weight: 600;
        }
        
        .course-card-body {
            padding: 15px;
            flex-grow: 1;
        }
        
        /* Subject cards */
        .subject-card {
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .subject-card:hover {
            transform: translateX(5px);
        }
        
        /* Flashcard animations */
        .flashcard {
            perspective: 1000px;
            height: 200px;
            margin-bottom: 20px;
            cursor: pointer;
        }
        
        .flashcard-inner {
            position: relative;
            width: 100%;
            height: 100%;
            transition: transform 0.6s;
            transform-style: preserve-3d;
        }
        
        .flashcard.flipped .flashcard-inner {
            transform: rotateY(180deg);
        }
        
        .flashcard-front, .flashcard-back {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 8px;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        .flashcard-front {
            background-color: #1E88E5;
            color: white;
        }
        
        .flashcard-back {
            background-color: #4CAF50;
            color: white;
            transform: rotateY(180deg);
        }
        
        /* Animation classes */
        .animated {
            animation-duration: 1s;
            animation-fill-mode: both;
        }
        
        .fadeIn {
            animation-name: fadeIn;
        }
        
        .fadeInUp {
            animation-name: fadeInUp;
        }
        
        .bounceIn {
            animation-name: bounceIn;
        }
        
        .pulse {
            animation-name: pulse;
            animation-duration: 2s;
            animation-iteration-count: infinite;
        }
        
        .slideInRight {
            animation-name: slideInRight;
        }
        
        /* Animation keyframes */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeInUp {
            from { 
                opacity: 0;
                transform: translate3d(0, 40px, 0);
            }
            to { 
                opacity: 1;
                transform: translate3d(0, 0, 0);
            }
        }
        
        @keyframes bounceIn {
            from, 20%, 40%, 60%, 80%, to {
                animation-timing-function: cubic-bezier(0.215, 0.610, 0.355, 1.000);
            }
            0% {
                opacity: 0;
                transform: scale3d(0.3, 0.3, 0.3);
            }
            20% {
                transform: scale3d(1.1, 1.1, 1.1);
            }
            40% {
                transform: scale3d(0.9, 0.9, 0.9);
            }
            60% {
                opacity: 1;
                transform: scale3d(1.03, 1.03, 1.03);
            }
            80% {
                transform: scale3d(0.97, 0.97, 0.97);
            }
            to {
                opacity: 1;
                transform: scale3d(1, 1, 1);
            }
        }
        
        @keyframes pulse {
            from {
                transform: scale3d(1, 1, 1);
            }
            50% {
                transform: scale3d(1.05, 1.05, 1.05);
            }
            to {
                transform: scale3d(1, 1, 1);
            }
        }
        
        @keyframes slideInRight {
            from {
                transform: translate3d(100%, 0, 0);
                visibility: visible;
            }
            to {
                transform: translate3d(0, 0, 0);
            }
        }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
