import random

class TutorRules:
    def __init__(self):
        self.forbidden_patterns = [
            "the answer is",
            "you should write",
            "the correct answer is",
            "here's the answer",
            "the solution is",
            "you need to write",
            "you must write",
            "the final answer is",
            "the result is",
            "you should get",
            "the answer will be",
            "the answer would be",
            "the answer should be",
            "the answer must be",
            "the answer needs to be",
            "here's how to solve it",
            "the way to solve this is",
            "you need to do this",
            "the formula is",
            "the calculation is",
            "the method is",
            "the approach is",
            "you need to use",
            "the correct method is",
            "the right way is"
        ]
        
        self.required_phrases = [
            "what do you think",
            "how would you approach",
            "can you explain",
            "let's think about",
            "consider this",
            "what if",
            "suppose that",
            "imagine if",
            "let's explore",
            "how might you",
            "what's your understanding of",
            "how would you break this down",
            "what factors would you consider",
            "what's the relationship between",
            "how would you analyze this",
            "what information would you need",
            "how would you verify this",
            "what assumptions are you making",
            "how would you test this",
            "what's the first step you would take"
        ]
        
        self.response_templates = [
            "Let's think about this step by step. What would you do first?",
            "How would you approach this problem?",
            "What information do you think we need to solve this?",
            "Can you explain your reasoning so far?",
            "What's the first thing you would consider?",
            "How would you start solving this?",
            "What do you know about this concept?",
            "Let's break this down. What's the first step?",
            "What would you need to know to solve this?",
            "How would you organize your thoughts on this?",
            "What's your understanding of the key concepts here?",
            "How would you verify if your approach is correct?",
            "What assumptions are you making in your approach?",
            "How would you test your solution?",
            "What alternative approaches could you consider?"
        ]

    def validate_response(self, response):
        """Validates that the response doesn't contain direct answers"""
        response_lower = response.lower()
        
        # Check for forbidden patterns
        for pattern in self.forbidden_patterns:
            if pattern in response_lower:
                return False, "Response contains direct answer pattern"
        
        # Check for required phrases
        has_required_phrase = any(phrase in response_lower for phrase in self.required_phrases)
        if not has_required_phrase:
            return False, "Response missing required guiding phrase"
        
        return True, "Response is valid"

    def get_redirecting_response(self):
        """Returns a response that redirects the student to think for themselves"""
        return random.choice(self.response_templates)

class AccountingFinanceTutor:
    def __init__(self):
        self.hints_given = 0
        self.max_hints = 3
        self.student_progress = {}
        self.rules = TutorRules()
        self.current_topic = None
        self.current_question_index = 0
        self.conversation_state = "initial"  # initial, topic_selected, in_discussion, practice
        self.learning_path = {
            "accounting_equation": [
                "Understanding the basic equation",
                "Analyzing transactions",
                "Impact on financial statements",
                "Real-world applications"
            ],
            "financial_ratios": [
                "Types of ratios",
                "Calculation methods",
                "Interpretation",
                "Industry comparisons"
            ],
            "financial_statements": [
                "Statement components",
                "Interrelationships",
                "Analysis techniques",
                "Practical applications"
            ],
            "time_value_money": [
                "Basic concepts",
                "Present value calculations",
                "Future value calculations",
                "Annuities and perpetuities"
            ]
        }
        
        # Common encouraging phrases
        self.encouragement_phrases = [
            "You're on the right track!",
            "That's a good start. Let's think about this further.",
            "You're getting closer!",
            "Good effort! Let's break this down step by step.",
            "Almost there! Consider one more aspect...",
            "That's an interesting perspective. Let's explore it further.",
            "You're making good progress. Let's refine your understanding.",
            "That's a thoughtful approach. Let's build on it.",
            "You're asking good questions. Let's explore them together.",
            "You're developing good analytical skills. Let's apply them here."
        ]
        
        # Topic-specific guidance templates
        self.topic_hints = {
            "accounting_equation": [
                "Remember the basic accounting equation: Assets = Liabilities + Equity",
                "Think about what changes on each side of the equation when a transaction occurs",
                "Consider how this transaction affects the company's assets and liabilities",
                "Remember that every transaction must maintain the equation's balance",
                "What's the impact on the company's financial position?",
                "How would this transaction be recorded in the accounting system?",
                "What's the relationship between this transaction and the company's equity?"
            ],
            "financial_ratios": [
                "Start by identifying which financial statements you need",
                "Consider what this ratio is trying to measure",
                "Think about the relationship between the numerator and denominator",
                "What does this ratio tell us about the company's performance?",
                "How would you interpret this ratio in context?",
                "What industry standards should you consider?",
                "How might this ratio change over time?"
            ],
            "financial_statements": [
                "Which statement would show this information?",
                "What's the relationship between these statements?",
                "Consider the timing of when transactions are recorded",
                "Think about the accrual vs. cash basis of accounting",
                "How do these statements work together?",
                "What's the purpose of each statement?",
                "How would you analyze trends in these statements?"
            ],
            "time_value_money": [
                "What is the relationship between present and future value?",
                "Consider the impact of interest rates and time periods",
                "Think about whether this is a single payment or an annuity",
                "How does compounding frequency affect the calculation?",
                "What assumptions are you making about interest rates?",
                "How would inflation impact your calculations?",
                "What's the difference between nominal and real rates?"
            ]
        }
        
        # Topic keywords for identification
        self.topic_keywords = {
            "accounting_equation": ["equation", "assets", "liabilities", "equity", "balance", "transaction", "accounting"],
            "financial_ratios": ["ratio", "calculate", "divide", "percentage", "profitability", "liquidity", "leverage"],
            "financial_statements": ["statement", "balance sheet", "income", "cash flow", "financial", "report"],
            "time_value_money": ["time value", "present value", "future value", "interest", "annuity", "discounting"]
        }

    def greet_student(self):
        """Initial greeting and session setup"""
        welcome_message = """
        Hello! I'm your Accounting & Finance Tutor. I'm here to help you understand 
        concepts and work through problems. Remember, I won't give you direct answers, 
        but I'll guide you to find them yourself.
        
        I can help you with:
        - Accounting Equation
        - Financial Ratios
        - Financial Statements
        - Time Value of Money
        
        What would you like to work on today?
        """
        return welcome_message

    def identify_topic(self, user_input):
        """Identifies the topic from user input"""
        user_input_lower = user_input.lower()
        
        for topic, keywords in self.topic_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return topic
        return None

    def evaluate_response(self, user_input, current_topic=None):
        """Evaluates response and determines next question or guidance needed"""
        user_input_lower = user_input.lower()
        
        # Handle exit command
        if user_input_lower == "exit":
            return "Thank you for studying with me! Keep up the good work!"
        
        # Handle initial state
        if self.conversation_state == "initial":
            identified_topic = self.identify_topic(user_input)
            if identified_topic:
                self.current_topic = identified_topic
                self.conversation_state = "topic_selected"
                return self.start_topic_discussion(identified_topic)
            else:
                return ("I can help you with Accounting Equation, Financial Ratios, "
                       "Financial Statements, or Time Value of Money. Which topic would you like to work on?")
        
        # Handle topic selected state
        elif self.conversation_state == "topic_selected":
            if "practice" in user_input_lower:
                self.conversation_state = "practice"
                difficulty = "medium"  # default difficulty
                if "easy" in user_input_lower:
                    difficulty = "easy"
                elif "hard" in user_input_lower:
                    difficulty = "hard"
                return self.create_practice_problem(self.current_topic, difficulty)
            else:
                self.conversation_state = "in_discussion"
                return self._handle_discussion(user_input)
        
        # Handle in discussion state
        elif self.conversation_state == "in_discussion":
            return self._handle_discussion(user_input)
        
        # Handle practice state
        elif self.conversation_state == "practice":
            if "hint" in user_input_lower:
                return self._provide_guided_hint()
            else:
                return self._handle_practice_response(user_input)
        
        return "I'm not sure I understand. Could you rephrase that?"

    def _handle_discussion(self, user_input):
        """Handles responses during topic discussion"""
        response_quality = self._assess_response(user_input)
        
        if response_quality == "good":
            self.current_question_index += 1
            if self.current_question_index < len(self.learning_path[self.current_topic]):
                next_response = (f"{random.choice(self.encouragement_phrases)} "
                               f"Let's move on to {self.learning_path[self.current_topic][self.current_question_index]}. "
                               f"What's your understanding of this aspect?")
                is_valid, _ = self.rules.validate_response(next_response)
                if not is_valid:
                    next_response = self.rules.get_redirecting_response()
                return next_response
            else:
                return ("Excellent! You've shown good understanding of this topic. "
                       "Would you like to try a practice problem to test your knowledge?")
        else:
            return self._provide_guided_hint()

    def _handle_practice_response(self, user_input):
        """Handles responses during practice problems"""
        response_quality = self._assess_response(user_input)
        
        if response_quality == "good":
            return ("That's a good approach! Let's think about it further. "
                   "What assumptions are you making in your solution? "
                   "How would you verify if your answer is correct?")
        else:
            return self._provide_guided_hint()

    def _assess_response(self, response):
        """Assess the quality of student response"""
        if not self.current_topic:
            return "needs_guidance"
            
        relevant_keywords = self.topic_keywords.get(self.current_topic, [])
        matches = sum(keyword in response.lower() for keyword in relevant_keywords)
        
        # Check for critical thinking indicators
        critical_thinking_indicators = [
            "because",
            "therefore",
            "thus",
            "since",
            "if",
            "then",
            "assume",
            "consider",
            "analyze",
            "evaluate"
        ]
        
        critical_thinking_matches = sum(indicator in response.lower() for indicator in critical_thinking_indicators)
        
        # Consider both keyword matches and critical thinking indicators
        total_score = matches + critical_thinking_matches
        
        return "good" if total_score >= 3 else "needs_guidance"

    def _provide_guided_hint(self):
        """Provides a structured hint based on current topic and progress"""
        if self.hints_given >= self.max_hints:
            return ("I've given you several hints. Let's take a step back. "
                   "What's your current understanding of the problem? "
                   "What specific part is challenging you?")
            
        if self.current_topic and self.current_question_index < len(self.topic_hints[self.current_topic]):
            self.hints_given += 1
            hint = f"Let's think about this differently. {self.topic_hints[self.current_topic][self.current_question_index]}"
            is_valid, _ = self.rules.validate_response(hint)
            if not is_valid:
                hint = self.rules.get_redirecting_response()
            return hint
        return "Could you explain your thinking process to me? What's challenging you about this problem?"

    def create_practice_problem(self, topic, difficulty):
        """Generates a practice problem based on topic and difficulty"""
        practice_problems = {
            "accounting_equation": {
                "easy": "A company purchases $1,000 of inventory on credit. How does this affect the accounting equation?",
                "medium": "A company issues $5,000 in common stock and purchases equipment worth $3,000 cash. Show the impact on the accounting equation.",
                "hard": "A company takes out a $10,000 loan, purchases inventory for $7,000, and pays $2,000 in dividends. What's the net effect on the accounting equation?"
            },
            "financial_ratios": {
                "easy": "Calculate the current ratio if current assets are $50,000 and current liabilities are $25,000.",
                "medium": "A company has current assets of $75,000, inventory of $25,000, and current liabilities of $30,000. Calculate the quick ratio.",
                "hard": "Calculate the return on equity if net income is $60,000, total assets are $400,000, and total liabilities are $200,000."
            }
        }
        
        problem = practice_problems.get(topic, {}).get(difficulty, "No problem available for this topic and difficulty level.")
        return f"{problem}\n\nHow would you approach solving this problem?"

def main():
    tutor = AccountingFinanceTutor()
    print(tutor.greet_student())
    
    while True:
        user_input = input("\nStudent: ").lower()
        print("Tutor:", tutor.evaluate_response(user_input))

if __name__ == "__main__":
    main()
