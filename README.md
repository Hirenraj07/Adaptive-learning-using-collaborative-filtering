# Adaptive-learning-using-collaborative-filtering
Personalized course recommendation system using collaborative filtering and machine learning.

This project is a complete Adaptive Learning recommendation system built using **Python**, **Machine Learning**, and **Streamlit**. It analyzes high school student performance data and dynamically suggests personalized learning content.

---

## 🚀 Objectives

- Predict student performance using collaborative filtering techniques  
- Recommend customized course paths (beginner/intermediate) based on predicted proficiency  
- Visualize strengths, weaknesses, and trends in subject-level understanding  
- Provide an interactive frontend dashboard for course suggestions and insights  

---

## 🧠 Features

### 1. Machine Learning & Collaborative Filtering  
- Uses student performance data to train a collaborative filtering model  
- Predicts likely outcomes in unattempted subjects  
- Saves trained models as `.pkl` files for fast re-use  

### 2. Course Recommendation Engine  
- Dynamically selects suitable course JSON files from the `courses/` directory  
- Tailors recommendations based on subject strengths and weaknesses  

### 3. Visual Insights  
- Generates visualizations such as:  
  - Subject-wise performance  
  - Time spent vs outcomes  
  - Weakest and strongest subject areas  

### 4. Interactive Frontend (Streamlit)  
- Deployable using `streamlit run frontend/app.py`  
- Allows students to interactively receive personalized course suggestions  

---

## 📊 Visualizations

| Performance Trends | Strength vs Weakness |  
| ------------------ | -------------------- |  
| ![Performance Trends](https://drive.google.com/uc?id=1AG6LdCa37pE7IXjLhpNrOb32tNI4TWN9) | ![Strength vs Weakness](https://drive.google.com/uc?id=1fkmtmn3_lrTYoBriUThZ1kS0L965CGFO) |  

![Strength Areas](https://drive.google.com/uc?id=1soxiy1njTPP0HkCEpCJ9TIlzKA9QKnFK)  

*Images are loaded directly from Google Drive links for easy access.*

---

## 🛠️ Tech Stack

- Python  
- Pandas, NumPy  
- Scikit-learn  
- Streamlit  
- Matplotlib, Seaborn  
- DAX (Power BI) – used in a separate BI project  

---

## 📁 Run Locally

```bash
git clone https://github.com/Hirenraj07/adaptive_learning.git
cd adaptive_learning
pip install -r requirements.txt
streamlit run frontend/app.py

