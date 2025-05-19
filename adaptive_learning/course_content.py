"""
Course content database for the adaptive learning platform.
Contains detailed course information and structure for various subjects.
"""

# Dictionary containing detailed course information by subject
COURSE_DATABASE = {
    "Coding": {
        "title": "Introduction to Coding",
        "description": "This course is designed to introduce students to the fundamentals of programming. We'll start with the very basics and progressively build up to more complex concepts. By the end of this course, students will have a solid foundation in coding using Python, including writing simple programs, understanding data structures, and applying problem-solving skills.",
        "modules": [
            {
                "title": "Programming Fundamentals",
                "learning_objectives": [
                    "Understand what programming is and why it is essential.",
                    "Learn basic programming terminology and concepts.",
                    "Set up a development environment for coding."
                ],
                "content": {
                    "sections": [
                        {
                            "title": "What Is Programming?",
                            "description": "Programming is the process of creating instructions for computers to perform specific tasks. It is important for automating tasks, solving complex problems, and building interactive applications."
                        },
                        {
                            "title": "Key Terminology",
                            "description": "Algorithm: A step-by-step procedure for solving a problem. Variable: A storage location for data. Syntax: The set of rules that defines combinations of symbols considered as correctly structured code."
                        },
                        {
                            "title": "Setting Up Your Environment",
                            "description": "Installing Python and using an IDE (Integrated Development Environment) such as VS Code or PyCharm. Basic command line usage."
                        }
                    ],
                    "examples": ["Write a simple 'Hello, World!' program."],
                    "exercises": ["Identify and explain the components of the 'Hello, World!' code."]
                }
            },
            {
                "title": "Python Basics",
                "learning_objectives": [
                    "Get familiar with Python's syntax and basic structures.",
                    "Write simple programs using variables, loops, and conditional statements."
                ],
                "content": {
                    "sections": [
                        {
                            "title": "Variables and Data Types",
                            "description": "Explanation of numbers, strings, booleans, and how to assign values. Example: age = 15, name = 'Alice'."
                        },
                        {
                            "title": "Operators and Expressions",
                            "description": "Arithmetic, comparison, and logical operators. Practice simple calculations."
                        },
                        {
                            "title": "Control Structures",
                            "description": "Conditional Statements: if, elif, and else. Loops: For and while loops."
                        },
                        {
                            "title": "Functions",
                            "description": "What are functions and why they are useful. Writing a simple function that returns the sum of two numbers."
                        }
                    ],
                    "examples": ["Print numbers 1 to 10 using a loop."],
                    "exercises": [
                        "Code a function to check if a number is even or odd.",
                        "Modify a loop to iterate through a list of names and print a greeting for each."
                    ]
                }
            },
            {
                "title": "Intermediate Programming Concepts",
                "learning_objectives": [
                    "Learn to work with data structures and handle exceptions.",
                    "Understand how to read from and write to files."
                ],
                "content": {
                    "sections": [
                        {
                            "title": "Data Structures in Python",
                            "description": "Lists, Tuples, and Dictionaries: How to create and use them. When to use a list vs. a tuple vs. a dictionary."
                        },
                        {
                            "title": "Error Handling",
                            "description": "Importance of handling errors to make programs robust. Using try/except blocks."
                        },
                        {
                            "title": "File I/O",
                            "description": "How to open, read, and write files. Example: Reading a text file and printing its content."
                        }
                    ],
                    "examples": ["Read a file containing a list of numbers and print the sum."],
                    "exercises": ["Build a small contact book using dictionaries and lists."]
                }
            },
            {
                "title": "Introduction to Object-Oriented Programming (OOP)",
                "learning_objectives": [
                    "Understand the principles of OOP.",
                    "Learn how to create and use classes and objects in Python."
                ],
                "content": {
                    "sections": [
                        {
                            "title": "What is OOP?",
                            "description": "Definition and benefits of object-oriented programming. Key concepts: classes, objects, inheritance, and encapsulation."
                        },
                        {
                            "title": "Creating Classes and Objects",
                            "description": "How to define a class and create instances. Example: Creating a simple Student class."
                        },
                        {
                            "title": "Inheritance",
                            "description": "How to create a subclass that inherits properties from a parent class. Example: Define a GraduateStudent class that extends Student."
                        }
                    ],
                    "examples": ["Create a simple Student class with name and age attributes."],
                    "exercises": [
                        "Develop a class hierarchy for a school system (e.g., Person, Student, Teacher).",
                        "Write a program that creates multiple student objects and prints a personalized greeting for each."
                    ]
                }
            }
        ]
    },
    "Math": {
        "title": "Mathematics Fundamentals",
        "description": "This course covers essential mathematical concepts from basic arithmetic to introductory calculus. It is designed to strengthen students' numerical understanding, problem-solving skills, and their ability to apply math in real-world scenarios.",
        "modules": [
            {
                "title": "Arithmetic and Number Sense",
                "learning_objectives": [
                    "Master basic arithmetic operations.",
                    "Develop strong number sense with fractions, decimals, and percentages."
                ],
                "content": {
                    "sections": [
                        {
                            "title": "Basic Operations",
                            "description": "Addition, subtraction, multiplication, and division. Examples and step-by-step explanations."
                        },
                        {
                            "title": "Fractions and Decimals",
                            "description": "Converting between fractions and decimals. Simplifying fractions."
                        },
                        {
                            "title": "Percentages",
                            "description": "Calculating percentages. Real-life examples like discounts and interest rates."
                        }
                    ],
                    "examples": ["Convert fractions like 3/4 into decimals."],
                    "exercises": ["Practice calculating 25% of various numbers."]
                }
            },
            {
                "title": "Algebra Fundamentals",
                "learning_objectives": [
                    "Understand and manipulate algebraic expressions.",
                    "Solve basic linear equations and inequalities."
                ],
                "content": {
                    "sections": [
                        {
                            "title": "Algebraic Expressions",
                            "description": "Introduction to variables and constants. Simplifying expressions."
                        },
                        {
                            "title": "Equations and Inequalities",
                            "description": "Solving linear equations with one variable. Understanding and graphing simple inequalities."
                        },
                        {
                            "title": "Word Problems",
                            "description": "Translating real-world problems into algebraic equations."
                        }
                    ],
                    "examples": ["Solve 3x + 5 = 20 and interpret the solution."],
                    "exercises": [
                        "Solve and check equations like 2x - 4 = 10.",
                        "Create your own word problem and solve it step by step."
                    ]
                }
            },
            {
                "title": "Geometry and Measurement",
                "learning_objectives": [
                    "Learn the properties of basic geometric shapes.",
                    "Calculate perimeter, area, and volume."
                ],
                "content": {
                    "sections": [
                        {
                            "title": "Basic Shapes",
                            "description": "Properties of triangles, rectangles, circles, and polygons. Real-world applications."
                        },
                        {
                            "title": "Perimeter and Area",
                            "description": "Formulas for calculating the perimeter and area of various shapes."
                        },
                        {
                            "title": "Volume and Surface Area",
                            "description": "Formulas for cubes, cylinders, and spheres. Understanding the concepts with practical examples."
                        }
                    ],
                    "examples": ["Calculate the area of a rectangle with given dimensions."],
                    "exercises": [
                        "Calculate the circumference of a circle and the area of a rectangle.",
                        "Use the Pythagorean theorem to find missing sides in triangles."
                    ]
                }
            },
            {
                "title": "Introduction to Calculus and Data Analysis",
                "learning_objectives": [
                    "Grasp the basic ideas behind calculus.",
                    "Learn to interpret simple graphs and trends."
                ],
                "content": {
                    "sections": [
                        {
                            "title": "Limits and Derivatives",
                            "description": "Basic definition of a limit. Concept of a derivative as the rate of change."
                        },
                        {
                            "title": "Integrals",
                            "description": "Introduction to integration as the area under a curve."
                        },
                        {
                            "title": "Graphing and Data Analysis",
                            "description": "Interpreting line graphs, bar charts, and histograms. Basic statistics: mean, median, mode."
                        }
                    ],
                    "examples": ["What is the derivative of x²?"],
                    "exercises": [
                        "Graph a simple linear function and calculate its slope.",
                        "Interpret a sample data set by calculating the mean and plotting the data."
                    ]
                }
            }
        ]
    },
    "Social Studies": {
        "title": "Social Studies and World Civics",
        "description": "This course introduces students to the fundamentals of social studies. It covers history, geography, civics, and cultural studies to help students understand the development of societies and their interconnectedness in the modern world.",
        "modules": [
            {
                "title": "Foundations of Social Studies",
                "learning_objectives": [
                    "Understand the scope and importance of social studies.",
                    "Recognize the roles of history, geography, civics, and culture in society."
                ],
                "content": {
                    "sections": [
                        {
                            "title": "Introduction to Social Studies",
                            "description": "Definition and importance. How social studies helps us understand our world."
                        },
                        {
                            "title": "Key Disciplines",
                            "description": "History: Chronological study of past events. Geography: Study of places and physical relationships. Civics: Understanding government and citizen responsibilities. Culture: Exploration of traditions, customs, and beliefs."
                        }
                    ],
                    "examples": [],
                    "exercises": [
                        "Discussion: Why is it important to study history?",
                        "Activity: Map out a timeline of major historical events."
                    ]
                }
            },
            {
                "title": "World History and Geography",
                "learning_objectives": [
                    "Explore the major civilizations and historical events that shaped our world.",
                    "Understand basic geographical concepts and their influence on society."
                ],
                "content": {
                    "sections": [
                        {
                            "title": "Ancient Civilizations",
                            "description": "Overview of civilizations like Egypt, Mesopotamia, Greece, and Rome. Their contributions in art, science, governance, and culture."
                        },
                        {
                            "title": "Geographical Concepts",
                            "description": "Understanding maps, regions, and climate. The impact of physical geography on the development of civilizations."
                        },
                        {
                            "title": "Modern Historical Events",
                            "description": "Key events in modern history such as the Renaissance, Industrial Revolution, and World Wars."
                        }
                    ],
                    "examples": [],
                    "exercises": [
                        "Compare contributions of two ancient civilizations.",
                        "Use a world map to identify regions and discuss how geography influenced historical trade routes."
                    ]
                }
            },
            {
                "title": "Civics and Government",
                "learning_objectives": [
                    "Understand the structure of government and the roles of citizens.",
                    "Learn how laws are made and why civic participation matters."
                ],
                "content": {
                    "sections": [
                        {
                            "title": "Foundations of Government",
                            "description": "Types of government systems: Democracy, monarchy, dictatorship. Separation of powers: Executive, Legislative, Judicial branches."
                        },
                        {
                            "title": "Citizen's Role",
                            "description": "Civic duties, rights, and responsibilities. How citizens participate in government through voting, activism, and community service."
                        },
                        {
                            "title": "Law Making Process",
                            "description": "Steps involved in passing legislation. Importance of checks and balances in government."
                        }
                    ],
                    "examples": [],
                    "exercises": [
                        "Discussion: How do different branches of government work together?",
                        "Exercise: Simulate a simple legislative process where students propose and debate a new rule for a classroom."
                    ]
                }
            },
            {
                "title": "Culture, Society, and Globalization",
                "learning_objectives": [
                    "Appreciate cultural diversity and its role in society.",
                    "Analyze the impact of globalization on local and global communities."
                ],
                "content": {
                    "sections": [
                        {
                            "title": "Cultural Studies",
                            "description": "Defining culture and examining cultural norms. Case studies of cultural festivals and traditions."
                        },
                        {
                            "title": "Social Institutions",
                            "description": "What are social institutions (e.g., family, education, religion)? Their roles in shaping societal behavior and values."
                        },
                        {
                            "title": "Globalization",
                            "description": "Definition and historical context. How globalization connects nations and influences local cultures. Discussion on the benefits and challenges of globalization."
                        }
                    ],
                    "examples": [],
                    "exercises": [
                        "Activity: Research and present a cultural tradition from another country.",
                        "Discussion: How has globalization changed the way we interact with other cultures?"
                    ]
                }
            }
        ]
    }
}

# Additional interactive elements and reinforcement strategies
LEARNING_TOOLS = {
    "all_courses": {
        "flashcards_quizzes": {
            "description": "Flashcards for key terms and concepts to reinforce learning. Periodic quizzes that offer immediate feedback."
        },
        "practical_projects": {
            "Coding": "Build a small application that incorporates learned concepts.",
            "Math": "Solve real-world problems through projects, such as budgeting or statistical analysis.",
            "Social Studies": "Create a multimedia presentation on a historical event or cultural phenomenon."
        },
        "discussion_forums": {
            "description": "Forums for students to discuss topics, ask questions, and share insights in a moderated environment."
        },
        "gamification": {
            "description": "Award badges or points for completing modules, quizzes, and projects to keep students motivated."
        }
    }
}

# Sample practice problems by subject and difficulty
PRACTICE_PROBLEMS = {
    "Coding": {
        "beginner": [
            {
                "question": "Write a program that prints the numbers from 1 to 10.",
                "code_solution": """
for i in range(1, 11):
    print(i)
"""
            },
            {
                "question": "Create a function that returns True if a number is even and False if it's odd.",
                "code_solution": """
def is_even(number):
    return number % 2 == 0
    
# Test the function
print(is_even(4))  # True
print(is_even(7))  # False
"""
            },
            {
                "question": "Write a program that asks the user for their name and greets them.",
                "code_solution": """
name = input("What is your name? ")
print(f"Hello, {name}! Nice to meet you.")
"""
            }
        ],
        "intermediate": [
            {
                "question": "Create a function that takes a list of numbers and returns the sum of all even numbers in the list.",
                "code_solution": """
def sum_even_numbers(numbers):
    total = 0
    for num in numbers:
        if num % 2 == 0:
            total += num
    return total
    
# Test the function
print(sum_even_numbers([1, 2, 3, 4, 5, 6]))  # 12 (2+4+6)
"""
            },
            {
                "question": "Write a program that reads a file named 'data.txt' and counts the number of words in it.",
                "code_solution": """
def count_words(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            words = content.split()
            return len(words)
    except FileNotFoundError:
        return "File not found."
        
print(count_words('data.txt'))
"""
            }
        ],
        "advanced": [
            {
                "question": "Create a class called 'BankAccount' that has methods for deposit, withdraw, and checking the balance.",
                "code_solution": """
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited ${amount}. New balance: ${self.balance}"
        return "Amount must be positive."
        
    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds."
        if amount > 0:
            self.balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        return "Amount must be positive."
        
    def get_balance(self):
        return f"Balance for {self.owner}: ${self.balance}"

# Test the class
account = BankAccount("John Smith", 100)
print(account.deposit(50))  # Deposited $50. New balance: $150
print(account.withdraw(25))  # Withdrew $25. New balance: $125
print(account.get_balance())  # Balance for John Smith: $125
"""
            }
        ]
    },
    "Math": {
        "beginner": [
            {
                "question": "Calculate 15% of 80.",
                "solution": "To find 15% of 80, multiply 80 by 0.15: 80 × 0.15 = 12"
            },
            {
                "question": "Convert the fraction 3/8 to a decimal.",
                "solution": "To convert 3/8 to a decimal, divide 3 by 8: 3 ÷ 8 = 0.375"
            },
            {
                "question": "If a rectangle has a length of 10 cm and a width of 5 cm, what is its area?",
                "solution": "The area of a rectangle is length × width. So, 10 cm × 5 cm = 50 square cm"
            }
        ],
        "intermediate": [
            {
                "question": "Solve the equation: 3x + 5 = 20",
                "solution": """
Step 1: Subtract 5 from both sides: 3x + 5 - 5 = 20 - 5
Step 2: Simplify: 3x = 15
Step 3: Divide both sides by 3: 3x/3 = 15/3
Step 4: Simplify: x = 5
"""
            },
            {
                "question": "A triangle has sides of lengths 3, 4, and 5. What is its area?",
                "solution": """
This is a right triangle (3-4-5 triangle).
Using the formula Area = (1/2) × base × height:
Area = (1/2) × 3 × 4 = 6 square units
"""
            }
        ],
        "advanced": [
            {
                "question": "Find the derivative of f(x) = x² + 3x + 2",
                "solution": """
Using the power rule and the sum rule:
f'(x) = 2x + 3
"""
            },
            {
                "question": "Calculate the integral of g(x) = 2x + 5 from x = 1 to x = 3",
                "solution": """
Step 1: Find the indefinite integral: G(x) = x² + 5x + C
Step 2: Calculate the definite integral: G(3) - G(1)
        = ((3)² + 5(3)) - ((1)² + 5(1))
        = (9 + 15) - (1 + 5)
        = 24 - 6
        = 18
"""
            }
        ]
    },
    "Social Studies": {
        "beginner": [
            {
                "question": "Name three ancient civilizations and one contribution each made to modern society.",
                "solution": """
1. Ancient Egypt: Hieroglyphic writing system, architectural innovations (pyramids), and medical knowledge
2. Ancient Greece: Democracy, philosophy, and Olympic Games
3. Ancient Rome: Legal system, architectural innovations (roads, aqueducts), and government structure
"""
            },
            {
                "question": "What are the three branches of government in a democracy?",
                "solution": """
The three branches of government in a democracy are:
1. Executive Branch: Responsible for implementing and enforcing laws
2. Legislative Branch: Responsible for making laws
3. Judicial Branch: Responsible for interpreting laws and administering justice
"""
            }
        ],
        "intermediate": [
            {
                "question": "Explain how geography influenced the development of ancient civilizations.",
                "solution": """
Geography influenced ancient civilizations in several ways:
1. River valleys (Nile, Tigris-Euphrates, Indus, Yellow) provided fertile soil for agriculture, allowing settlements to grow
2. Natural barriers like mountains and seas offered protection from invasions
3. Access to water bodies facilitated trade and cultural exchange
4. Climate affected what crops could be grown and the types of livestock that could be raised
5. Natural resources determined technological development and trade goods
"""
            },
            {
                "question": "Compare and contrast democracy and monarchy as forms of government.",
                "solution": """
Democracy:
- Power rests with the citizens who vote to elect representatives
- Often has separation of powers and checks and balances
- Leaders serve for limited terms
- Laws can be changed through established processes
- Examples: United States, France, India

Monarchy:
- Power rests with a monarch (king/queen) who typically inherits the position
- Authority may be absolute or limited (constitutional monarchy)
- Ruler often serves for life
- In absolute monarchies, the monarch can change laws at will
- Examples: Saudi Arabia (absolute), United Kingdom (constitutional)

Similarities:
- Both can have written laws and constitutions
- Both can provide stability and national identity
- Both require some form of administration to function
"""
            }
        ],
        "advanced": [
            {
                "question": "Analyze the impact of globalization on cultural identity and sovereignty.",
                "solution": """
Impact of Globalization on Cultural Identity and Sovereignty:

Cultural Identity:
- Positive effects: Increased exposure to diverse cultures, preservation of endangered traditions through global recognition
- Negative effects: Homogenization of culture ("McDonaldization"), dilution of local traditions, dominance of Western cultural products

Sovereignty:
- Economic sovereignty: Nations become economically interdependent, multinational corporations gain influence, international trade agreements may limit national economic policies
- Political sovereignty: International organizations and agreements (UN, EU, etc.) require nations to adhere to certain standards, creating tension between global cooperation and national autonomy
- Digital sovereignty: Control over data, privacy laws, and internet governance becomes increasingly complex in a borderless digital world

Balance:
- "Glocalization": Adapting global influences to local contexts
- Revival movements: Cultural preservation efforts in response to globalization
- International governance frameworks that respect diversity while addressing global challenges
"""
            }
        ]
    }
}

def get_course_content(subject):
    """
    Retrieve full course content for a specific subject.
    
    Args:
        subject (str): The subject to get course content for
        
    Returns:
        dict: Complete course content or None if not found
    """
    return COURSE_DATABASE.get(subject)

def get_module_content(subject, module_title):
    """
    Retrieve module content for a specific subject and module.
    
    Args:
        subject (str): The subject to get module content for
        module_title (str): The title of the module to retrieve
        
    Returns:
        dict: Module content or None if not found
    """
    course = COURSE_DATABASE.get(subject)
    if not course:
        return None
    
    for module in course["modules"]:
        if module["title"] == module_title:
            return module
    
    return None
