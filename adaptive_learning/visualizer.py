import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from data_processor import DataProcessor

class Visualizer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.processor = DataProcessor(file_path)
        self.df = self.processor.load_data()
        self.processed_data = self.processor.preprocess_data()
        
        # Create visualizations directory if it doesn't exist
        self.vis_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'visualizations')
        os.makedirs(self.vis_dir, exist_ok=True)
        
    def plot_performance_distribution(self):
        """Plot distribution of performance tiers"""
        plt.figure(figsize=(12, 6))
        
        # Count students in each performance tier
        tier_counts = self.processed_data['performance_tier'].value_counts().sort_index()
        
        # Create bar chart with custom colors
        ax = sns.barplot(x=tier_counts.index, y=tier_counts.values, 
                        palette=['#FF5733', '#FFC300', '#36A2EB', '#4BC0C0', '#9966FF'])
        
        # Add count labels on top of bars
        for i, count in enumerate(tier_counts.values):
            ax.text(i, count + 5, str(count), ha='center', fontweight='bold')
        
        plt.title('Distribution of Students Across Performance Tiers', fontsize=16)
        plt.xlabel('Performance Tier', fontsize=14)
        plt.ylabel('Number of Students', fontsize=14)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save figure
        plt.savefig(os.path.join(self.vis_dir, 'performance_distribution.png'), dpi=300)
        plt.close()
        print(f"Performance distribution plot saved to {self.vis_dir}")
    
    def plot_subject_performance(self):
        """Plot average performance across subjects"""
        plt.figure(figsize=(14, 8))
        
        # Get subject columns
        subject_cols = [col for col in self.processed_data.columns 
                       if col not in ['average_score', 'performance_tier', 'time_spent']]
        
        # Calculate average scores per subject
        subject_scores = self.processed_data[subject_cols].mean().sort_values(ascending=False)
        
        # Create bar chart with gradient colors
        palette = sns.color_palette("viridis", len(subject_scores))
        ax = sns.barplot(x=subject_scores.index, y=subject_scores.values, palette=palette)
        
        # Add score labels on top of bars
        for i, score in enumerate(subject_scores.values):
            ax.text(i, score + 1, f"{score:.1f}", ha='center', fontweight='bold')
        
        plt.title('Average Performance by Subject', fontsize=16)
        plt.xlabel('Subject', fontsize=14)
        plt.ylabel('Average Score', fontsize=14)
        plt.ylim(0, 100)  # Set y-axis limit for consistency
        plt.axhline(y=60, color='r', linestyle='--', alpha=0.7, label='Passing Score (60)')
        plt.legend()
        plt.tight_layout()
        
        # Save figure
        plt.savefig(os.path.join(self.vis_dir, 'subject_performance.png'), dpi=300)
        plt.close()
        print(f"Subject performance plot saved to {self.vis_dir}")
    
    def plot_time_vs_performance(self):
        """Plot correlation between time spent and performance"""
        plt.figure(figsize=(12, 8))
        
        # Create scatter plot
        scatter = plt.scatter(
            self.processed_data['time_spent'], 
            self.processed_data['average_score'],
            c=self.processed_data['performance_tier'].astype('category').cat.codes,
            cmap='viridis',
            alpha=0.7,
            s=100
        )
        
        # Add trend line
        z = np.polyfit(self.processed_data['time_spent'], self.processed_data['average_score'], 1)
        p = np.poly1d(z)
        plt.plot(
            sorted(self.processed_data['time_spent']),
            p(sorted(self.processed_data['time_spent'])),
            "r--", 
            linewidth=2,
            label=f"Trend line (y={z[0]:.2f}x + {z[1]:.2f})"
        )
        
        # Add legend and labels
        plt.legend(handles=scatter.legend_elements()[0], 
                   labels=['Below 40', '40-50', '50-70', '70-80', 'Above 80'], 
                   title="Performance Tier")
        
        plt.title('Correlation: Time Spent vs. Performance', fontsize=16)
        plt.xlabel('Time Spent (Proxy Metric)', fontsize=14)
        plt.ylabel('Average Score', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save figure
        plt.savefig(os.path.join(self.vis_dir, 'time_vs_performance.png'), dpi=300)
        plt.close()
        print(f"Time vs performance plot saved to {self.vis_dir}")
    
    def plot_adaptive_complexity(self):
        """Visualize how course complexity adapts based on performance"""
        plt.figure(figsize=(14, 8))
        
        # Get unique performance tiers for categorical x-axis
        tiers = ['Below 40', '40-50', '50-70', '70-80', 'Above 80']
        
        # Define complexity levels for each tier (decreasing complexity as performance improves)
        complexity_levels = {
            'Below 40': 90,
            '40-50': 75,
            '50-70': 60,
            '70-80': 45,
            'Above 80': 30
        }
        
        # Create bar chart for complexity
        complexity_values = [complexity_levels[tier] for tier in tiers]
        plt.bar(tiers, complexity_values, color='#3498db', alpha=0.7, label='Course Complexity')
        
        # Add challenge level (gradually increasing)
        challenge_levels = {
            'Below 40': 20,
            '40-50': 40,
            '50-70': 60,
            '70-80': 80,
            'Above 80': 90
        }
        
        # Add challenge level line
        challenge_values = [challenge_levels[tier] for tier in tiers]
        plt.plot(tiers, challenge_values, 'ro-', linewidth=3, label='Challenge Level')
        
        # Add engagement level (balanced)
        engagement_levels = {
            'Below 40': 60,
            '40-50': 75,
            '50-70': 85,
            '70-80': 75,
            'Above 80': 65
        }
        
        # Add engagement level line
        engagement_values = [engagement_levels[tier] for tier in tiers]
        plt.plot(tiers, engagement_values, 'g^-', linewidth=3, label='Engagement Design')
        
        plt.title('Adaptive Learning: Course Parameters by Performance Tier', fontsize=16)
        plt.xlabel('Performance Tier', fontsize=14)
        plt.ylabel('Level (0-100)', fontsize=14)
        plt.ylim(0, 100)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save figure
        plt.savefig(os.path.join(self.vis_dir, 'adaptive_complexity.png'), dpi=300)
        plt.close()
        print(f"Adaptive complexity plot saved to {self.vis_dir}")
    
    def plot_subject_strengths_weaknesses(self):
        """Visualize student strengths and weaknesses by subject"""
        plt.figure(figsize=(15, 10))
        
        # Get subject columns
        subject_cols = [col for col in self.processed_data.columns 
                       if col not in ['average_score', 'performance_tier', 'time_spent']]
        
        # Create boxplot for each subject
        ax = sns.boxplot(data=self.processed_data[subject_cols], palette="Set3")
        
        # Add swarmplot to show individual data points
        sns.swarmplot(data=self.processed_data[subject_cols], color=".25", size=3, alpha=0.5)
        
        # Add a horizontal line at score 60 (passing threshold)
        plt.axhline(y=60, color='r', linestyle='--', alpha=0.7, label='Passing Score (60)')
        
        plt.title('Subject Performance Distribution (Strengths & Weaknesses)', fontsize=16)
        plt.xlabel('Subject', fontsize=14)
        plt.ylabel('Score', fontsize=14)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        
        # Save figure
        plt.savefig(os.path.join(self.vis_dir, 'subject_strengths_weaknesses.png'), dpi=300)
        plt.close()
        print(f"Subject strengths and weaknesses plot saved to {self.vis_dir}")
    
    def create_all_visualizations(self):
        """Create all visualizations"""
        print("Generating visualizations...")
        
        try:
            self.plot_performance_distribution()
            self.plot_subject_performance()
            self.plot_time_vs_performance()
            self.plot_adaptive_complexity()
            self.plot_subject_strengths_weaknesses()
            
            print("All visualizations have been created in the 'visualizations' directory.")
        except Exception as e:
            print(f"Error creating visualizations: {str(e)}")
            import traceback
            traceback.print_exc()
