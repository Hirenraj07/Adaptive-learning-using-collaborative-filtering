import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
from sklearn.model_selection import GridSearchCV
import joblib
import os
from data_processor import DataProcessor

class ModelTrainer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.model = None
        self.best_params = None
        self.processor = DataProcessor(file_path)
        
    def train_model(self):
        """Train the RandomForest model with hyperparameter tuning"""
        # Get processed data
        X_train, X_test, y_train, y_test = self.processor.split_data()
        
        print("Starting model training...")
        
        # Initialize model
        rf = RandomForestClassifier(random_state=42)
        
        # Define parameter grid for GridSearch
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        # Use smaller grid for quicker results if needed
        quick_param_grid = {
            'n_estimators': [100],
            'max_depth': [10],
            'min_samples_split': [2],
            'min_samples_leaf': [1]
        }
        
        print("Performing hyperparameter tuning...")
        # Perform GridSearch with cross-validation
        grid_search = GridSearchCV(
            estimator=rf,
            param_grid=quick_param_grid,  # Use quick_param_grid for faster results
            cv=5,
            scoring='accuracy',
            n_jobs=-1
        )
        
        grid_search.fit(X_train, y_train)
        
        # Get best model and parameters
        self.model = grid_search.best_estimator_
        self.best_params = grid_search.best_params_
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        
        print("\nModel Performance:")
        print(f"Best Parameters: {self.best_params}")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Get feature importance
        feature_importance = self.get_feature_importance()
        print("\nFeature Importance:")
        print(feature_importance.head(10))
        
        # Create model directory if it doesn't exist
        model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
        os.makedirs(model_dir, exist_ok=True)
        
        # Save the model
        model_path = os.path.join(model_dir, 'performance_predictor.pkl')
        joblib.dump(self.model, model_path)
        print(f"Model saved to {model_path}")
        
        return accuracy
    
    def predict_performance(self, student_data):
        """Predict performance tier for new student data"""
        if self.model is None:
            model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                      'models', 'performance_predictor.pkl')
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
            else:
                print("Model not found. Training a new model...")
                self.train_model()
        
        # Ensure student_data has the same features as training data
        X, _ = self.processor.get_features_and_labels()
        for col in X.columns:
            if col not in student_data.columns:
                student_data[col] = 0
        
        # Keep only columns used for training
        student_data = student_data[X.columns]
        
        return self.model.predict(student_data)
    
    def get_feature_importance(self):
        """Get feature importance from the trained model"""
        if self.model is None:
            model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                      'models', 'performance_predictor.pkl')
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
            else:
                print("Model not found. Training a new model...")
                self.train_model()
        
        # Get feature names and importance values
        X, _ = self.processor.get_features_and_labels()
        feature_names = X.columns
        
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return feature_importance
    
    def generate_course_recommendation(self, student_id=None, student_data=None):
        """Generate personalized course recommendations for a student"""
        if student_data is None and student_id is not None:
            # Get student data from the processor
            processed_data = self.processor.preprocess_data()
            if student_id not in processed_data.index:
                print(f"Student ID {student_id} not found in the dataset.")
                return None
            student_data = processed_data.loc[student_id].to_dict()
        
        if student_data is None:
            print("No student data provided.")
            return None
            
        # Identify student strengths and weaknesses
        subject_cols = [col for col in student_data.keys() 
                       if col not in ['average_score', 'performance_tier', 'time_spent']]
        
        # Convert to DataFrame for easier manipulation
        if not isinstance(student_data, pd.DataFrame):
            student_df = pd.DataFrame([student_data])
        else:
            student_df = student_data
            
        # Get scores for each subject
        subject_scores = {subj: student_df[subj].values[0] 
                         for subj in subject_cols if subj in student_df.columns}
        
        # Identify weakest subjects (below 60 score)
        weak_subjects = {subj: score for subj, score in subject_scores.items() if score < 60}
        
        # Generate recommendations
        recommendations = []
        for subject, score in weak_subjects.items():
            if score < 40:
                difficulty = "Beginner"
                focus = "fundamental concepts"
            elif score < 60:
                difficulty = "Intermediate"
                focus = "problem-solving skills"
            else:
                difficulty = "Advanced"
                focus = "advanced applications"
                
            course = {
                "subject": subject,
                "current_score": score,
                "difficulty": difficulty,
                "recommended_course": f"{difficulty} {subject}",
                "focus_areas": focus,
                "duration_weeks": 4 if score < 40 else (3 if score < 60 else 2),
                "interactive_tools": ["flashcards", "quizzes", "practice problems"]
            }
            recommendations.append(course)
        
        return recommendations
    
    def get_reward_system(self, recommendations):
        """Create a reward system based on course recommendations"""
        if not recommendations:
            return {"message": "No courses to complete, no rewards available."}
        
        rewards = {
            "points_per_course": 100,
            "total_points_available": len(recommendations) * 100,
            "achievement_badges": [
                f"{course['subject']} Master" for course in recommendations
            ],
            "completion_rewards": {
                "all_courses": "Advanced Student Certificate",
                "individual_course": "Subject Mastery Badge"
            },
            "bonus_rewards": {
                "quick_completion": "Time Management Star",
                "perfect_score": "Excellence Award"
            }
        }
        
        return rewards
