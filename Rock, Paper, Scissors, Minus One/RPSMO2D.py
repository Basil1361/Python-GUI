import random

def RPS(n): 
    player_choices = []
    for i in range(n):
        while True:
            x = str(input(f"Choice {i+1} - Type r, p or s: "))
            # Check length first
            if len(x) > 1:
                print("Type only r, p or s!")
                continue
                
            if not x.isalpha():
                print("String Only")
                continue
                
            if x.lower() not in ['r', 'p', 's']:
                print("Only r, p, or s allowed!")
                continue
            player_choices.append(x.lower())
            break
    
    print(f"Your choices: {player_choices}")
    return player_choices
    
def Computer(n):
    computer_choices = []
    for _ in range(n):
        x = random.randint(1,3)
        computer_choices.append(int(x))
    conversion = {1: 'r', 2: 'p', 3: 's'}
    computer_letters = []
    for choice in computer_choices:
        computer_letters.append(conversion[choice])
    print(f"Computer choices: {computer_letters}")
    return computer_letters

def player_choice_2():
    player_choice = RPS(2)
    computer_letters = Computer(2)
    
    # Player selects one choice to keep
    while True:
        x = str(input("Now, select one to keep: "))
        if x in player_choice:
            print(f"Your final pick is {x}")
            break
        else:
            print(f"There is no {x} within {player_choice}")
            print("Please try again!")
    
    # Computer randomly selects one choice to keep
    y = random.randint(0, 1)  # Use 0,1 for list indexing
    computer_final = computer_letters[y]
    print(f"Computer kept: {computer_final}")
    
    return x, computer_final
        
def final_decision(): 
    x, computer_final = player_choice_2() 
    print(f"\nFINAL BATTLE:")
    if x == computer_final:
        print("It's a TIE!")
        result = "tie"
    elif (x == 'r' and computer_final == 's') or \
         (x == 'p' and computer_final == 'r') or \
         (x == 's' and computer_final == 'p'):
        print("YOU WIN!")
        result = "win"
    else:
        print("YOU LOSE!")
        result = "lose"
    return result
final_decision()

