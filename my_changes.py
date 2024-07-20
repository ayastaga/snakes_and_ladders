import time
import random
import sys
    
def welcome_msg():
    msg = """
    Welcome to Agastya's Snake and Ladder Game. 
    Version: The most awesome one available    
    
    Here's some ground rules:
        1. Each player takes turns rolling the die. Your pieces moves forward based on the number on the die. 
        2. If your piece lands at the bottom of a ladder, you can climb that ladder to a new square!
        3. However, if your piece lands on the head of a snake... you must go down to square where the the snake's tail ends.
        4. The first player to reach *exactly* 100 wins! 
        
    Have fun playing!
    """

    print(msg) 

def get_player_count():
    player_count = 6
    while player_count > 4 or player_count < 2:
        player_count = int(input("How many players are playing this game? (2-4): ").strip())
    return player_count

def get_players_list(player_count):
    players_list = []
    print("\nPlease enter the names of each player: \n")
    for i in range(player_count):
        player = None
        while not player:
            player = input(f"Player {i + 1}: ").strip()
        players_list.append(player)
    
    return players_list

def generate_ladders_position():
    ladders_list = {}
    used_ladders_list = []
    
    while len(ladders_list) < 15:
        ladder_start = random.randint(5, 85)
        ladder_end = random.randint(5, 85)
        
        if (ladder_end > ladder_start and 
        ladder_start not in used_ladders_list and 
        ladder_end not in used_ladders_list):
            
            ladders_list[ladder_start] = ladder_end
            used_ladders_list.append(ladder_start)
            used_ladders_list.append(ladder_end)
    
    return ladders_list

def generate_snakes_position(ladders_list):
    snakes_list = {}
    ladder_start_positions = ladders_list.keys()
    ladder_end_positions = ladders_list.values()
    used_snakes_list = []
    
    while len(snakes_list) < 10:
        snake_mouth = random.randint(20, 95)
        snake_tail = random.randint(20, 95)
        
        # in this case, the snakes are always in different position and don't overlap
        if (snake_mouth > snake_tail and 
        snake_mouth not in used_snakes_list and 
        snake_tail not in used_snakes_list and 
        snake_mouth not in ladder_end_positions):
            
            snakes_list[snake_mouth] = snake_tail
            used_snakes_list.append(snake_mouth)
            used_snakes_list.append(snake_mouth)

    return snakes_list
 
def roll_dice(current_position, player_name):
    dice_value = random.randint(1, 6)
    new_position = current_position
    print("\nRolling dice...")
    
    print(f"{player_name} rolled a {dice_value}!")
     
    if current_position + dice_value > 100:
        print(f"You need to get to 100 exactly, so you need a {100 - current_position}. Better luck next time!")
    else:
        new_position = current_position + dice_value
        print(f"{player_name} moved from {current_position} to {new_position}")

    return new_position

def check_for_ladder(current_position, ladder_list, player_name):
    if current_position in ladder_list.keys():
        new_position = current_position + 15
        print(f"{player_name} climbed a ladder and moved from {current_position} to {new_position}")
    else:
        new_position = current_position
    
    return new_position

def check_for_snake(current_position, snake_list, player_name):
    if current_position in snake_list.keys():
        new_position = current_position - 10
        print(f"{player_name} got bit by a snake and moved from {current_position} to {new_position}")
    else:
        new_position = current_position
    
    return new_position

def shortest_pathfinder(ladders_list, snakes_list):
    leaps = ladders_list | snakes_list
    squares = {0}
    counter = 0
    
    while 100 not in squares:
        counter += 1
        old_squares = squares
        squares = set() # reset squares
        
        for square in old_squares:
            for dice in range(6):
                new_square = square + dice + 1
                squares.add(leaps.get(new_square, new_square))
                
    return counter
       
if __name__ == "__main__":
    play_again = True
    while play_again:
        welcome_msg()
        
        SLEEP_TIME = 1    
        
        player_count = get_player_count()

        players_position = [0] * player_count    
        players_name = get_players_list(player_count)
        ladders_list = generate_ladders_position()
        snakes_list = generate_snakes_position(ladders_list)
        
        move_counter = 0
        
        while all(position < 99 for position in players_position):
            move_counter += 1
            for i in range(player_count):
                current_position = players_position[i]
    
                new_position = roll_dice(current_position, players_name[i])
                new_position = check_for_ladder(new_position, ladders_list, players_name[i])
                new_position = check_for_snake(new_position, snakes_list, players_name[i])
                
                players_position[i] = new_position

                if new_position > 99:
                    print(f"\nCongratulations! {players_name[i]} has won!!\n")
                    break

            if new_position > 99:
                break
        
        shortest_path = shortest_pathfinder(ladders_list, snakes_list)
        print(f"Here's some trivia:\nYour game took {move_counter} moves. The shortest game would have taken only {shortest_path} moves!\n")
        
        play_again_prompt = "None"
        while play_again_prompt.upper() not in ["Y", "N"]:
            play_again_prompt = input("Would you like to play again? (Y/N): ").strip()
        
        if play_again_prompt.upper() == "N":
            play_again = False
