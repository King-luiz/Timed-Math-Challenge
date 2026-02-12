import random
import time

# Game configuration
DIFFICULTY_LEVELS = {
    "1": {"name": "Easy", "min": 2, "max": 10, "operators": ["+", "-"]},
    "2": {"name": "Medium", "min": 3, "max": 12, "operators": ["+", "-", "*"]},
    "3": {"name": "Hard", "min": 5, "max": 20, "operators": ["+", "-", "*", "//"]}
}

TOTAL_PROBLEMS = 10
HIGH_SCORE_FILE = "math_game_scores.txt"


def display_welcome():
    """Display welcome message and instructions"""
    print("=" * 50)
    print("🧮 WELCOME TO THE MENTAL MATH TRAINER! 🧮".center(50))
    print("=" * 50)
    print("\nHow it works:")
    print("• You'll get", TOTAL_PROBLEMS, "math problems")
    print("• Each wrong attempt costs you 1 point")
    print("• Try to finish as fast as you can!")
    print("• Division problems use integer division (//)")
    print("\nLet's test your mental math skills!\n")


def select_difficulty():
    """Let user select difficulty level"""
    print("Select Difficulty:")
    for key, level in DIFFICULTY_LEVELS.items():
        print(f"{key}. {level['name']} - {level['min']} to {level['max']}, ops: {', '.join(level['operators'])}")
    
    while True:
        choice = input("Enter difficulty (1/2/3): ")
        if choice in DIFFICULTY_LEVELS:
            return DIFFICULTY_LEVELS[choice]
        print("Invalid choice. Please enter 1, 2, or 3.")


def generate_problem(difficulty):
    """Generate a random math problem based on difficulty"""
    left = random.randint(difficulty["min"], difficulty["max"])
    right = random.randint(difficulty["min"], difficulty["max"])
    operator = random.choice(difficulty["operators"])
    
    # Ensure division problems have clean answers
    if operator == "//":
        # Make left number a multiple of right for clean division
        left = right * random.randint(difficulty["min"], difficulty["max"] // 2)
    
    expr = f"{left} {operator} {right}"
    answer = eval(expr)
    return expr, answer


def save_high_score(name, score, time_taken, difficulty, wrong_attempts):
    """Save player's score to file"""
    try:
        with open(HIGH_SCORE_FILE, "a") as f:
            f.write(f"{name}|{score}|{time_taken}|{difficulty}|{wrong_attempts}|{time.strftime('%Y-%m-%d %H:%M')}\n")
    except:
        print("Could not save high score.")


def display_high_scores():
    """Display top 10 high scores"""
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            scores = f.readlines()
        
        if scores:
            print("\n🏆 HIGH SCORES 🏆".center(50))
            print("-" * 50)
            
            # Parse and sort scores
            score_list = []
            for line in scores:
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    score_list.append({
                        "name": parts[0],
                        "score": int(parts[1]),
                        "time": float(parts[2]),
                        "difficulty": parts[3],
                        "date": parts[5]
                    })
            
            # Sort by score (higher is better), then by time (lower is better)
            score_list.sort(key=lambda x: (-x["score"], x["time"]))
            
            # Display top 10
            print(f"{'Rank':<6} {'Name':<15} {'Score':<8} {'Time':<8} {'Difficulty':<10} {'Date':<12}")
            print("-" * 65)
            for i, score in enumerate(score_list[:10], 1):
                print(f"{i:<6} {score['name'][:15]:<15} {score['score']:<8} {score['time']:<8.1f} {score['difficulty']:<10} {score['date']:<12}")
        else:
            print("\nNo high scores yet. Be the first!")
    except FileNotFoundError:
        print("\nNo high scores yet. Be the first!")
    except Exception as e:
        print(f"\nCould not load high scores: {e}")


def play_game():
    """Main game function"""
    display_welcome()
    display_high_scores()
    
    # Get player name
    player_name = input("\nEnter your name: ").strip() or "Anonymous"
    
    # Select difficulty
    difficulty = select_difficulty()
    print(f"\nStarting {difficulty['name']} mode!")
    
    # Game variables
    wrong = 0
    wrong_attempts = []  # Track which problems were answered wrong
    problem_history = []  # Track all problems and answers
    
    input("\nPress Enter to start!")
    print("----------------------")
    
    start_time = time.time()
    
    # Main game loop
    for i in range(TOTAL_PROBLEMS):
        expr, answer = generate_problem(difficulty)
        attempts = 0
        
        print(f"\nProblem #{i + 1}:")
        
        while True:
            guess = input(f"{expr} = ")
            
            try:
                # Handle integer answers
                if guess.strip() == "":
                    print("Please enter an answer!")
                    continue
                    
                if int(guess) == answer:
                    print("✓ Correct!")
                    break
                else:
                    wrong += 1
                    attempts += 1
                    print(f"✗ Incorrect. Try again! (Attempts: {attempts})")
            except ValueError:
                print("Please enter a valid number!")
        
        # Track wrong attempts for this problem
        if attempts > 0:
            wrong_attempts.append({
                "problem": expr,
                "answer": answer,
                "attempts": attempts
            })
        
        # Store problem history
        problem_history.append({
            "problem": expr,
            "answer": answer,
            "attempts": attempts + 1  # +1 for the correct attempt
        })
    
    end_time = time.time()
    total_time = round(end_time - start_time, 2)
    
    # Calculate score
    max_score = TOTAL_PROBLEMS * 10  # 10 points per problem
    score = max(max_score - (wrong * 2), 0)  # 2 points penalty per wrong attempt
    
    # Display results
    print("\n" + "=" * 50)
    print("📊 GAME RESULTS 📊".center(50))
    print("=" * 50)
    print(f"\nPlayer: {player_name}")
    print(f"Difficulty: {difficulty['name']}")
    print(f"Time: {total_time} seconds")
    print(f"Wrong attempts: {wrong}")
    print(f"Your score: {score} / {max_score}")
    
    # Performance rating
    if wrong == 0:
        print("🌟 PERFECT! Flawless victory! 🌟")
    elif wrong < 3:
        print("👍 Great job! Very few mistakes!")
    elif wrong < 7:
        print("👌 Good effort! Keep practicing!")
    else:
        print("💪 Keep practicing! You'll improve!")
    
    # Show problems with multiple attempts
    if wrong_attempts:
        print("\n📝 Problems you struggled with:")
        for item in wrong_attempts:
            print(f"  • {item['problem']} = {item['answer']} ({item['attempts']} wrong attempts)")
    
    # Save score
    save_high_score(player_name, score, total_time, difficulty['name'], wrong)
    
    # Ask for rematch
    print("\n" + "=" * 50)
    play_again = input("Play again? (y/n): ").lower()
    if play_again == 'y':
        play_game()
    else:
        print("\nThanks for playing! Come back soon to beat your high score! 🎮")


def main():
    """Entry point of the game"""
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. See you next time!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please restart the game.")


if __name__ == "__main__":
    main()