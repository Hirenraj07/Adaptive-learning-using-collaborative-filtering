import os
import sys
import pandas as pd
import numpy as np
from data_processor import DataProcessor
from model_trainer import ModelTrainer
from visualizer import Visualizer

def main():
    # Define paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(current_dir, "highschool_subject_performance_dataset.csv")
    
    # Create directories if they don't exist
    os.makedirs(os.path.join(current_dir, 'models'), exist_ok=True)
    os.makedirs(os.path.join(current_dir, 'visualizations'), exist_ok=True)
    
    # Check if dataset exists
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        return
    
    try:
        print("\nStarting Data Processing...")
        processor = DataProcessor(dataset_path)
        df = processor.load_data()
        print(f"Loaded {len(df)} records from dataset")
        processed_data = processor.preprocess_data()
        print(f"Processed data shape: {processed_data.shape}")
        
        print("\nStarting Model Training...")
        trainer = ModelTrainer(dataset_path)
        trainer.train_model()
        
        print("\nCreating Visualizations...")
        visualizer = Visualizer(dataset_path)
        visualizer.create_all_visualizations()
        
        print("\nPipeline completed successfully!")
        print("1. Trained model saved to 'models/performance_predictor.pkl'")
        print("2. Visualizations saved to 'visualizations/' directory")
        print("3. Run the Streamlit app using: streamlit run frontend/app.py")
    except Exception as e:
        print(f"Error during execution: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
