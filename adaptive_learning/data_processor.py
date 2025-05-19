import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import os

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.processed_data = None
        
    def load_data(self):
        """Load and preprocess the dataset"""
        print(f"Loading data from {self.file_path}")
        self.df = pd.read_csv(self.file_path)
        
        # Remove average rows for initial analysis
        self.df_clean = self.df[~self.df['test_number'].astype(str).str.contains('Average')]
        # Convert numeric columns
        self.df_clean['score'] = pd.to_numeric(self.df_clean['score'], errors='coerce')
        self.df_clean['test_number'] = pd.to_numeric(self.df_clean['test_number'], errors='coerce')
        # Drop rows with NaN values
        self.df_clean = self.df_clean.dropna()
        
        print(f"Data loaded successfully with {len(self.df_clean)} records")
        return self.df_clean
    
    def preprocess_data(self):
        """Preprocess data for model training"""
        if self.df is None:
            self.load_data()
        
        # Calculate average scores per student per subject
        student_subjects = self.df_clean.groupby(['student_id', 'subject'])['score'].mean().reset_index()
        
        # Pivot to get subjects as columns
        student_matrix = student_subjects.pivot(index='student_id', columns='subject', values='score')
        
        # Fill NaN values with 0
        student_matrix = student_matrix.fillna(0)
        
        # Calculate average score across all subjects for each student
        student_matrix['average_score'] = student_matrix.mean(axis=1)
        
        # Categorize students into performance tiers
        student_matrix['performance_tier'] = pd.cut(
            student_matrix['average_score'], 
            bins=[0, 40, 50, 70, 80, 100],
            labels=['Below 40', '40-50', '50-70', '70-80', 'Above 80']
        )
        
        # Track time spent (using test numbers as proxy)
        time_spent = self.df_clean.groupby('student_id')['test_number'].sum().reset_index()
        time_spent.columns = ['student_id', 'time_spent']
        
        # Merge time spent with student matrix
        student_matrix_reset = student_matrix.reset_index()
        final_data = pd.merge(student_matrix_reset, time_spent, on='student_id')
        
        # Set student_id as index again
        final_data = final_data.set_index('student_id')
        
        # Store processed data
        self.processed_data = final_data
        print(f"Data preprocessing complete. Final shape: {self.processed_data.shape}")
        
        return self.processed_data
    
    def identify_strengths_weaknesses(self):
        """Identify student strengths and weaknesses"""
        if self.processed_data is None:
            self.preprocess_data()
        
        # Get subject columns (excluding non-subject columns)
        subject_cols = [col for col in self.processed_data.columns 
                       if col not in ['average_score', 'performance_tier', 'time_spent']]
        
        # For each student, identify best and worst subjects
        strengths_weaknesses = {}
        
        for student_id in self.processed_data.index:
            student_data = self.processed_data.loc[student_id]
            subject_scores = student_data[subject_cols]
            
            best_subject = subject_scores.idxmax()
            worst_subject = subject_scores.idxmin()
            
            strengths_weaknesses[student_id] = {
                'best_subject': best_subject,
                'best_score': student_data[best_subject],
                'worst_subject': worst_subject,
                'worst_score': student_data[worst_subject],
                'average_score': student_data['average_score'],
                'performance_tier': student_data['performance_tier']
            }
        
        return strengths_weaknesses
    
    def get_features_and_labels(self):
        """Split data into features and labels"""
        if self.processed_data is None:
            self.preprocess_data()
        
        # Features: all columns except performance_tier
        X = self.processed_data.drop('performance_tier', axis=1)
        # Label: performance_tier
        y = self.processed_data['performance_tier']
        
        return X, y
    
    def split_data(self, test_size=0.2, random_state=42):
        """Split data into training and test sets"""
        X, y = self.get_features_and_labels()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")
        return X_train, X_test, y_train, y_test
