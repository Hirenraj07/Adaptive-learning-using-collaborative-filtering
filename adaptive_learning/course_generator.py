import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

class NumpyEncoder(json.JSONEncoder):
    """Custom encoder to handle NumPy data types"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32, np.float16)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

class CourseGenerator:
    """
    Generates personalized course content for students based on their performance data.
    Specifically targets students with poor performance in specific subjects.
    """
    
    def __init__(self):
        # Import detailed course content
        from course_content import COURSE_DATABASE, LEARNING_TOOLS, PRACTICE_PROBLEMS
        
        # Store course database
        self.course_database = COURSE_DATABASE
        self.learning_tools = LEARNING_TOOLS
        self.practice_problems = PRACTICE_PROBLEMS
        
        # Define difficulty levels
        self.difficulty_levels = {
            "beginner": {
                "complexity": 1,
                "prerequisites": [],
                "estimated_duration_weeks": 4,
                "session_length_minutes": 30
            },
            "intermediate": {
                "complexity": 2,
                "prerequisites": ["beginner"],
                "estimated_duration_weeks": 3,
                "session_length_minutes": 45
            },
            "advanced": {
                "complexity": 3,
                "prerequisites": ["beginner", "intermediate"],
                "estimated_duration_weeks": 2,
                "session_length_minutes": 60
            }
        }
        
        # Define subject templates with core concepts
        self.subject_templates = {
            "Math": {
                "core_concepts": [
                    "Number Systems", "Algebra", "Geometry", "Trigonometry", 
                    "Statistics", "Calculus"
                ],
                "practical_applications": [
                    "Financial Calculations", "Data Analysis", "Engineering Problems",
                    "Scientific Modeling"
                ],
                "learning_resources": [
                    "Interactive Exercises", "Video Tutorials", "Problem Sets",
                    "Virtual Math Lab"
                ]
            },
            "Science": {
                "core_concepts": [
                    "Scientific Method", "Physics Principles", "Chemistry Fundamentals", 
                    "Biology Basics", "Earth Sciences"
                ],
                "practical_applications": [
                    "Laboratory Experiments", "Environmental Analysis", "Technology Applications",
                    "Medical Sciences"
                ],
                "learning_resources": [
                    "Virtual Labs", "Science Simulations", "Field Work Projects",
                    "Research Exercises"
                ]
            },
            "English": {
                "core_concepts": [
                    "Grammar Rules", "Vocabulary Building", "Reading Comprehension", 
                    "Writing Techniques", "Literary Analysis"
                ],
                "practical_applications": [
                    "Essay Writing", "Communication Skills", "Critical Analysis",
                    "Creative Writing"
                ],
                "learning_resources": [
                    "Reading Materials", "Writing Workshops", "Language Games",
                    "Literature Studies"
                ]
            },
            "History": {
                "core_concepts": [
                    "Ancient Civilizations", "Medieval Period", "Modern Era", 
                    "World Wars", "Historical Research Methods"
                ],
                "practical_applications": [
                    "Document Analysis", "Historical Debates", "Timeline Creation",
                    "Cultural Studies"
                ],
                "learning_resources": [
                    "Primary Sources", "Historical Documentaries", "Museum Virtual Tours",
                    "Timeline Projects"
                ]
            },
            "Coding": {
                "core_concepts": [
                    "Programming Fundamentals", "Data Structures", "Algorithms", 
                    "Web Development", "Software Engineering"
                ],
                "practical_applications": [
                    "App Development", "Website Creation", "Game Design",
                    "Data Analysis Projects"
                ],
                "learning_resources": [
                    "Coding Challenges", "Code Editors", "Project-Based Learning",
                    "Pair Programming Exercises"
                ]
            },
            "Art": {
                "core_concepts": [
                    "Color Theory", "Composition", "Drawing Techniques", 
                    "Art History", "Digital Arts"
                ],
                "practical_applications": [
                    "Portfolio Development", "Exhibition Planning", "Design Projects",
                    "Mixed Media Work"
                ],
                "learning_resources": [
                    "Virtual Studio", "Technique Tutorials", "Art Analysis",
                    "Museum Studies"
                ]
            },
            "Music": {
                "core_concepts": [
                    "Music Theory", "Rhythm & Tempo", "Melody & Harmony", 
                    "Instrumentation", "Music History"
                ],
                "practical_applications": [
                    "Performance Skills", "Composition", "Music Production",
                    "Critical Listening"
                ],
                "learning_resources": [
                    "Instrument Practice", "Composition Software", "Listening Exercises",
                    "Performance Workshops"
                ]
            },
            "Physical Education": {
                "core_concepts": [
                    "Fitness Fundamentals", "Sports Rules", "Health & Nutrition", 
                    "Body Systems", "Movement Science"
                ],
                "practical_applications": [
                    "Fitness Planning", "Sports Practice", "Health Analysis",
                    "Team Activities"
                ],
                "learning_resources": [
                    "Training Programs", "Skill Drills", "Team Challenges",
                    "Sports Analytics"
                ]
            }
        }
    
    def generate_course(self, subject, current_score, student_id=None):
        """
        Generate a complete course for a student with poor performance in a specific subject.
        
        Args:
            subject (str): The subject to generate a course for
            current_score (float): The student's current score in the subject
            student_id (str, optional): Student ID for personalization
            
        Returns:
            dict: Complete course structure with lessons, exercises, assessments
        """
        # Determine appropriate difficulty level based on current score
        if current_score < 40:
            difficulty = "beginner"
        elif current_score < 60:
            difficulty = "intermediate"
        else:
            difficulty = "advanced"
        
        # Check if we have detailed course content for this subject
        if subject in self.course_database:
            # Use the detailed course information from our database
            detailed_course = self.course_database[subject]
            
            # Create personalized course structure based on the detailed content
            course = {
                "course_title": f"{difficulty.title()} {detailed_course['title']}",
                "subject": subject,
                "difficulty": difficulty.title(),
                "current_score": current_score,
                "target_score": min(current_score + 20, 100),
                "generated_date": datetime.now().strftime("%Y-%m-%d"),
                "duration": self.difficulty_levels[difficulty]["estimated_duration_weeks"],
                "session_length_minutes": self.difficulty_levels[difficulty]["session_length_minutes"],
                "sessions_per_week": 3,
                "prerequisites": self.difficulty_levels[difficulty]["prerequisites"],
                "description": detailed_course["description"],
                "modules": []
            }
            
            # Generate modules based on the detailed content
            for module in detailed_course["modules"]:
                # Adjust module complexity based on student's current level
                module_content = {
                    "title": module["title"],
                    "learning_objectives": module["learning_objectives"],
                    "focus": ", ".join(module["learning_objectives"]),
                    "duration": max(1, int(self.difficulty_levels[difficulty]["estimated_duration_weeks"]/len(detailed_course["modules"]))),
                    "lessons": []
                }
                
                # Generate lessons for this module
                sections = module["content"]["sections"]
                for i, section in enumerate(sections):
                    # Skip advanced sections for beginners
                    if difficulty == "beginner" and i >= min(3, len(sections)):
                        continue
                    
                    # Create lesson
                    lesson = {
                        "title": section["title"],
                        "focus": section["description"].split('.')[0],  # First sentence as focus
                        "learning_outcomes": module["learning_objectives"],
                        "activities": [
                            {
                                "type": "lecture",
                                "description": section["description"]
                            }
                        ]
                    }
                    
                    # Add examples if available
                    if i < len(module["content"].get("examples", [])):
                        lesson["activities"].append({
                            "type": "example",
                            "description": module["content"]["examples"][i]
                        })
                    
                    # Add exercises if available
                    for j, exercise in enumerate(module["content"].get("exercises", [])):
                        if j % len(sections) == i:  # Distribute exercises among lessons
                            lesson["activities"].append({
                                "type": "exercise",
                                "description": exercise
                            })
                    
                    module_content["lessons"].append(lesson)
                
                course["modules"].append(module_content)
            
            # Add learning tools from the global settings
            course["learning_activities"] = [
                {
                    "activity_type": "Flashcards & Quizzes",
                    "description": self.learning_tools["all_courses"]["flashcards_quizzes"]["description"],
                    "benefits": "Reinforces key concepts and provides immediate feedback on understanding",
                    "frequency": "Weekly"
                },
                {
                    "activity_type": "Practical Project",
                    "description": self.learning_tools["all_courses"]["practical_projects"].get(subject, "Apply concepts in a real-world project"),
                    "benefits": "Builds problem-solving skills and demonstrates practical application of knowledge",
                    "frequency": "At the end of each module"
                },
                {
                    "activity_type": "Discussion Forum",
                    "description": self.learning_tools["all_courses"]["discussion_forums"]["description"],
                    "benefits": "Encourages peer learning and develops communication skills",
                    "frequency": "Ongoing"
                }
            ]
            
            # Add assessment methods
            course["assessment_methods"] = [
                {
                    "method": "Module Quizzes",
                    "description": "Short assessments at the end of each module to test understanding",
                    "weight": 30
                },
                {
                    "method": "Practical Assignments",
                    "description": "Hands-on tasks that demonstrate application of concepts",
                    "weight": 40
                },
                {
                    "method": "Final Project",
                    "description": "Comprehensive project integrating all learned concepts",
                    "weight": 30
                }
            ]
            
            # Add completion requirements
            course["completion_requirements"] = [
                f"Complete all {len(course['modules'])} modules with a minimum score of 70%",
                "Submit all practical assignments",
                "Complete the final project with a minimum score of 70%",
                "Participate in at least 5 forum discussions"
            ]
            
            return course
        
        # Fall back to the original method if we don't have detailed content
        # Check if subject template exists
        if subject not in self.subject_templates:
            # Default to a generic template if subject not found
            subject_data = {
                "core_concepts": [
                    "Fundamentals", "Intermediate Concepts", "Advanced Applications"
                ],
                "practical_applications": [
                    "Basic Applications", "Problem Solving", "Advanced Projects"
                ],
                "learning_resources": [
                    "Textbook Materials", "Practice Exercises", "Project Work"
                ]
            }
        else:
            subject_data = self.subject_templates[subject]
        
        # Create course structure
        course = {
            "title": f"{difficulty.title()} {subject} Course",
            "subject": subject,
            "difficulty": difficulty,
            "current_score": current_score,
            "target_score": min(current_score + 20, 100),
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "duration_weeks": self.difficulty_levels[difficulty]["estimated_duration_weeks"],
            "session_length_minutes": self.difficulty_levels[difficulty]["session_length_minutes"],
            "sessions_per_week": 3,
            "overview": f"This personalized course is designed to improve your {subject} skills from a current score of {current_score} to a target of {min(current_score + 20, 100)}. The {difficulty} level curriculum focuses on building a solid foundation with gradual progression.",
            "modules": []
        }
        
        # Generate modules based on core concepts
        for i, concept in enumerate(subject_data["core_concepts"]):
            # Determine how many concepts to include based on difficulty
            if difficulty == "beginner" and i >= 3:
                continue  # Only include first 3 concepts for beginners
            elif difficulty == "intermediate" and i >= 4:
                continue  # Include first 4 concepts for intermediate
            
            module = {
                "module_id": i + 1,
                "title": concept,
                "description": f"Learn the essential components of {concept} with a focus on building a solid foundation.",
                "duration_days": 7,
                "lessons": []
            }
            
            # Generate 3-5 lessons per module
            num_lessons = 3 if difficulty == "beginner" else (4 if difficulty == "intermediate" else 5)
            
            for j in range(num_lessons):
                lesson = {
                    "lesson_id": j + 1,
                    "title": f"Lesson {j+1}: {self._generate_lesson_title(concept, j)}",
                    "duration_minutes": self.difficulty_levels[difficulty]["session_length_minutes"],
                    "content_summary": f"This lesson covers key aspects of {concept} with focus on {self._generate_lesson_focus(concept, j)}.",
                    "activities": [
                        {
                            "type": "video_tutorial",
                            "title": f"Understanding {self._generate_lesson_focus(concept, j)}",
                            "duration_minutes": 10
                        },
                        {
                            "type": "interactive_exercise",
                            "title": f"Practice with {self._generate_lesson_focus(concept, j)}",
                            "problems": 5 + (j * 2),
                            "difficulty": difficulty
                        },
                        {
                            "type": "quiz",
                            "title": f"Quick Check: {concept} Basics",
                            "questions": 5,
                            "passing_score": 60
                        }
                    ],
                    "resources": [
                        {
                            "type": "reading",
                            "title": f"{concept} Fundamentals",
                            "format": "PDF"
                        },
                        {
                            "type": "practice",
                            "title": f"{concept} Extra Practice",
                            "difficulty": difficulty
                        }
                    ]
                }
                
                # Add practical application for higher difficulty levels
                if difficulty != "beginner" or j == num_lessons - 1:
                    practical_app = subject_data["practical_applications"][min(i, len(subject_data["practical_applications"])-1)]
                    lesson["activities"].append({
                        "type": "practical_application",
                        "title": f"Apply Your Knowledge: {practical_app}",
                        "description": f"Complete a real-world application using {concept}.",
                        "duration_minutes": 15
                    })
                
                module["lessons"].append(lesson)
            
            # Add module assessment
            module["assessment"] = {
                "title": f"{concept} Mastery Assessment",
                "passing_score": 70,
                "question_count": 10 + (5 * self.difficulty_levels[difficulty]["complexity"]),
                "time_limit_minutes": 30 + (15 * self.difficulty_levels[difficulty]["complexity"]),
                "retake_allowed": True,
                "formats": ["multiple_choice", "short_answer", "problem_solving"]
            }
            
            course["modules"].append(module)
        
        # Add final course project
        course["final_project"] = {
            "title": f"{subject} Synthesis Project",
            "description": f"Demonstrate your mastery of {subject} concepts through a comprehensive project that integrates all the modules you've studied.",
            "duration_days": 7,
            "deliverables": [
                "Written report",
                "Visual presentation",
                "Applied demonstration"
            ],
            "evaluation_criteria": [
                "Comprehension of core concepts",
                "Application of techniques",
                "Creativity and originality",
                "Presentation quality"
            ],
            "passing_score": 70
        }
        
        # Add completion and certification
        course["completion"] = {
            "certification": f"{subject} Proficiency Certificate",
            "requirements": [
                "Complete all module assessments with a minimum score of 70%",
                "Submit and pass the final project with a minimum score of 70%",
                "Attend at least 80% of the scheduled sessions"
            ],
            "rewards": [
                "Digital certificate",
                "Performance tier upgrade",
                "100 achievement points",
                f"{subject} Specialist badge"
            ]
        }
        
        return course
    
    def _generate_lesson_title(self, concept, lesson_index):
        """Generate appropriate lesson titles based on concept and index"""
        if lesson_index == 0:
            return f"Introduction to {concept}"
        elif lesson_index == 1:
            return f"Core Principles of {concept}"
        elif lesson_index == 2:
            return f"Applying {concept}"
        elif lesson_index == 3:
            return f"Advanced Topics in {concept}"
        else:
            return f"Mastering {concept}"
    
    def _generate_lesson_focus(self, concept, lesson_index):
        """Generate appropriate focus areas based on concept and lesson index"""
        if lesson_index == 0:
            return f"fundamental definitions and basic principles"
        elif lesson_index == 1:
            return f"key methodologies and standard approaches"
        elif lesson_index == 2:
            return f"practical applications and problem-solving techniques"
        elif lesson_index == 3:
            return f"advanced strategies and specialized scenarios"
        else:
            return f"synthesis of complex ideas and creative applications"
    
    def save_course(self, course, output_dir="courses"):
        """Save generated course to a JSON file"""
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create filename from course title
        filename = f"{course['subject']}_{course['difficulty']}_course.json"
        filepath = os.path.join(output_dir, filename)
        
        # Save to JSON file using the custom encoder for NumPy types
        with open(filepath, 'w') as f:
            json.dump(course, f, indent=4, cls=NumpyEncoder)
        
        return filepath
    
    def get_practice_problems(self, subject, difficulty, topic, count=5):
        """
        Generate practice problems for a specific subject, difficulty, and topic.
        
        Args:
            subject (str): The subject to generate problems for
            difficulty (str): Difficulty level (beginner, intermediate, advanced)
            topic (str): Topic or concept to focus on
            count (int): Number of problems to generate
            
        Returns:
            list: List of practice problems with solutions
        """
        # First check if we have pre-defined practice problems in our database
        if subject in self.practice_problems and difficulty.lower() in self.practice_problems[subject]:
            # Get all available problems for this subject and difficulty
            available_problems = self.practice_problems[subject][difficulty.lower()]
            
            # Return requested number of problems (or all if fewer available)
            return available_problems[:min(count, len(available_problems))]
        
        # If no predefined problems, generate simple ones
        problems = []
        
        for i in range(count):
            problem = {
                "question": f"Practice Problem {i+1} for {subject} ({topic})",
                "solution": f"This is a sample solution for problem {i+1}."
            }
            
            # Add sample code for coding problems
            if subject == "Coding":
                problem["code_solution"] = 'print("Hello, World!")'
                
            problems.append(problem)
        
        return problems

# Testing function
def main():
    generator = CourseGenerator()
    
    # Generate a sample course
    course = generator.generate_course("Math", 35, "student123")
    
    # Save course to file
    filepath = generator.save_course(course)
    print(f"Course saved to {filepath}")
    
    # Get practice problems
    problems = generator.get_practice_problems("Math", "beginner", "Algebra", 3)
    for i, problem in enumerate(problems):
        print(f"\nProblem {i+1}: {problem['question']}")
        print(f"Answer: {problem['solution']}")

if __name__ == "__main__":
    main()
