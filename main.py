from tkinter import *
from tkinter import messagebox
import random
import time
from tkinter import ttk

# Constants
BOARD_SIZE = 600
GRID_SIZE = 10
CELL_SIZE = BOARD_SIZE // GRID_SIZE
HAS_WON = False
player_index = 0
players = []
COLORS = ['blue', 'red', 'green', 'yellow']
# Set to 5 for cleaner look -> can adjust to follow requirement
NUM_OF_SNAKES = 5
NUM_OF_LADDERS = 5

def start_game():
    home_frame.forget()
    game()

def exit_game():
    confirmation = messagebox.askquestion(title="Form", message="Are you sure you would like to exit the game?")
    if confirmation == "yes":
        root.destroy()

def populate_nums():
    n = 1
    for i in range(GRID_SIZE):
        if i % 2 == 0: 
            # count forwards
            for j in range(GRID_SIZE):
                x_coordinate = CELL_SIZE * j + CELL_SIZE // 2
                y_coordinate = (GRID_SIZE - i - 1) * CELL_SIZE + CELL_SIZE // 2
                canvas.create_text(x_coordinate, y_coordinate, text=str(n), font=('DM Sans 14pt', 14))
                n += 1
        else:
            # count backwards
            for j in range(GRID_SIZE - 1, -1, -1):
                x_coordinate = CELL_SIZE * j + CELL_SIZE // 2
                y_coordinate = (GRID_SIZE - i - 1) * CELL_SIZE + CELL_SIZE // 2
                canvas.create_text(x_coordinate, y_coordinate, text=str(n), font=('DM Sans 14pt', 14))
                n += 1

def create_canvas():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            top_left_x = j * CELL_SIZE
            bottom_right_x = i * CELL_SIZE
            top_left_y = top_left_x + CELL_SIZE
            bottom_right_y = bottom_right_x + CELL_SIZE
            canvas.create_rectangle(
                top_left_x, bottom_right_x, top_left_y, bottom_right_y, outline="black", fill="white")
    
    populate_nums()
    
    for i in range(player_count.get()):
        player = canvas.create_oval(5, BOARD_SIZE - CELL_SIZE + 5, CELL_SIZE - 5, BOARD_SIZE - 5, fill=COLORS[i])
        players.append(player)
        positions.append(1)

    draw_ladders()
    
    draw_snakes(ladders_list)

# Since ladder and snake positions are randomized, unable to use icons
def generate_ladders_position():
    ladders_list = {}
    used_ladders_list = []
    
    while len(ladders_list) < NUM_OF_LADDERS:
        ladder_start = random.randint(5, 85)
        ladder_end = random.randint(5, 85)
        
        if (ladder_end > ladder_start and
            ladder_end - ladder_start > 10 and 
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
    
    while len(snakes_list) < NUM_OF_SNAKES:
        snake_mouth = random.randint(20, 95)
        snake_tail = random.randint(20, 95)
        
        # in this case, the snakes are always in different position and don't overlap
        if (snake_mouth > snake_tail and
        snake_mouth - snake_tail > 10 and 
        snake_mouth not in used_snakes_list and 
        snake_tail not in used_snakes_list and 
        snake_mouth not in ladder_end_positions and
        snake_mouth not in ladder_start_positions):
            
            snakes_list[snake_mouth] = snake_tail
            used_snakes_list.append(snake_mouth)
            used_snakes_list.append(snake_mouth)

    return snakes_list

def get_coordinates(position):
    row = (position - 1) // GRID_SIZE
    col = (position - 1) % GRID_SIZE
    
    if row % 2 == 1:  # Adjust column for Boustrophedon pattern
        col = GRID_SIZE - 1 - col
    
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = (GRID_SIZE - 1 - row) * CELL_SIZE + CELL_SIZE // 2
    return x, y

def draw_snakes(ladders_list):    
    for mouth, tail in snakes_list.items():
        mouth_x, mouth_y = get_coordinates(mouth)
        tail_x, tail_y = get_coordinates(tail)
        canvas.create_line(mouth_x, mouth_y, tail_x, tail_y, fill="#6CBB3C", width=5, arrow=LAST)
        BUTT

def draw_ladders():    
    for bottom, top in ladders_list.items():
        bottom_x, bottom_y = get_coordinates(bottom)
        top_x, top_y = get_coordinates(top)
        canvas.create_line(bottom_x, bottom_y, top_x, top_y, fill="#964B00", width=5, arrow=LAST)

def move_player(player_index, new_position, regular_move):
    if regular_move == True:
        roll_btn['state'] = "disabled"
        for i in range(positions[player_index] + 1, new_position + 1):
            x, y = get_coordinates(i)
            canvas.coords(players[player_index], x - CELL_SIZE // 2 + 5, y - CELL_SIZE // 2 + 5, x + CELL_SIZE // 2 - 5, y + CELL_SIZE // 2 - 5)
            root.update()
            time.sleep(0.1)
        roll_btn['state'] = "active"
    else:
        x, y = get_coordinates(new_position)
        canvas.coords(players[player_index], x - CELL_SIZE // 2 + 5, y - CELL_SIZE // 2 + 5, x + CELL_SIZE // 2 - 5, y + CELL_SIZE // 2 - 5)

def message_delay():
    roll_btn['state'] = 'disabled'
    message_lbl.config(text=f"Rolling the dice...")
    root.after(0, roll_dice)

def roll_dice():
    global player_index
    global HAS_WON
    if HAS_WON == False:
        roll_btn['state'] = 'active'

    if player_index > player_count.get() - 1:
        player_index = 0
    
    dice_value = random.randint(1, 6)
    message_lbl.config(text=f"Player {player_index + 1}, rolled a {dice_value}", font=('Londrina Solid', 30))
    
    new_position = positions[player_index] + dice_value + 1

    if new_position > 100:
        message_lbl.config(text=f"Player {player_index + 1}, rolled a {dice_value}.\n{100 - positions[player_index]} is needed to reach 100", font=('Londrina Solid', 20))
        new_position -= dice_value - 1
        player_index += 1
        return
    elif new_position == 100:
        HAS_WON = True
        move_player(player_index, new_position, True)
        roll_btn['state'] = "disabled"
        message_lbl.config(text=f"Player {player_index + 1}, has won the game!!", font=('Londrina Solid', 30))
        return

    move_player(player_index, new_position, True)
    
    if new_position in snakes_list:
        new_position = snakes_list[new_position]
        move_player(player_index, new_position, False)
        message_lbl.config(text=f"Player {player_index + 1}, was biten by a snake\nand moved from {positions[player_index]} to {new_position}", font=('Londrina Solid', 20))
    
    if new_position in ladders_list:
        new_position = ladders_list[new_position]
        move_player(player_index, new_position, False)
        message_lbl.config(text=f"Player {player_index + 1}, climbed a ladder\nand moved from {positions[player_index]} to {new_position}", font=('Londrina Solid', 20))
        
    positions[player_index] = new_position
        
    player_index += 1

def game():
    root.resizable(True, True)
    root.geometry("700x750")
    root.resizable(False, False)
    
    game_frame.pack()
    canvas.pack(fill="both", expand=1)

    create_canvas()

    message_lbl.pack(fill="both", expand=0, side="right")

    reset_btn_frame.pack(fill="both", expand=1)
    reset_btn.pack(fill="both", expand=1)
    
    roll_btn.pack(fill="both", expand=1, side="left")
    
    game_frame.mainloop()

def reset_game():
    global positions
    global player_index
    global players
    global HAS_WON
    HAS_WON = False
    positions = [1] * player_count.get()
    player_index = 0
    for player in players:
        canvas.coords(player, 5, BOARD_SIZE - CELL_SIZE + 5, CELL_SIZE - 5, BOARD_SIZE - 5)
    message_lbl.config(text="Roll the Die!")


# -- HOME MENU -- 

root = Tk()
root.title("Snakes and Ladders")
root.geometry("550x800")
root.resizable(False, False) 

home_frame = Frame(root, bg="white")
game_frame = Frame(root, bg="white")
home_frame.pack(fill="both", expand=1)

title = Label(home_frame, text="Snakes &\nLadders", font=('Londrina Solid', 100), bg="white")
title.pack(fill="x", expand=0)

message_frame = LabelFrame(home_frame, text="Rules", font=('Londrina Solid', 20), bg="white")
message_frame.pack(fill="x", expand=0)
msg = """
1.  Each player takes turns rolling the die. The pieces moves 
    forward based on the number on the die. 
2.  If your piece lands at the bottom of a ladder, you can
    climb that ladder to a new square!
3.  However, if your piece lands on the head of a snake...you
    must go down to the square where the the snake's tail ends.
4.  The first player to reach *exactly* 100 wins! 
    """
message_label = Label(message_frame, text=msg, justify="left", font=("DM Sans 14pt", 12), bg="white")
message_label.pack(fill="x", expand=0)

ttk.Separator(home_frame, orient='horizontal').pack(fill="x", expand=0)

start_btn = Button(home_frame, text="START\nGAME", command=start_game, font=('Londrina Solid', 30), bg="white")
start_btn.pack(side="left", fill="both", expand=1)

num_of_players = Frame(home_frame, bg="white")
num_of_players.pack(side="left", fill="both", expand=1)

num_player_prompt = Label(num_of_players, text="Select number\nof players", font=("DM Sans 14pt", 15), bg="white")
num_player_prompt.pack(fill="both", expand=1)

player_count = IntVar()
two_players = Radiobutton(num_of_players, text="2 PLAYERS", variable=player_count, value=2, font=('Londrina Solid', 20), bg="white", justify="left")
two_players.pack(fill="both", expand=1)

three_players = Radiobutton(num_of_players, text="3 PLAYERS", variable=player_count, value=3, font=('Londrina Solid', 20), bg="white", justify="left")
three_players.pack(fill="both", expand=1)

four_players = Radiobutton(num_of_players, text="4 PLAYERS", variable=player_count, value=4, font=('Londrina Solid', 20), bg="white", justify="left")
four_players.pack(fill="both", expand=1)

player_count.set(2)

exit_btn = Button(home_frame, text="EXIT\nGAME", command=exit_game, font=('Londrina Solid', 30), bg="white")
exit_btn.pack(side="left", fill="both", expand=1)


# -- GAME MENU --

canvas = Canvas(game_frame, width=BOARD_SIZE, height=BOARD_SIZE, bg="white")

positions = [0] * player_count.get()

dice_img = PhotoImage(file="./dice_img.png")
smaller_dice_img = dice_img.subsample(3, 3)

message_lbl = Label(game_frame, text="Roll the dice!", font=('Londrina Solid', 30), borderwidth=1, relief="flat", width=26, bg="white")
roll_btn = Button(game_frame, image=smaller_dice_img, bg="white", command=message_delay)

reset_btn_frame = Frame(game_frame)
reset_btn = Button(reset_btn_frame, text="Reset game", bg="white", command=reset_game)

ladders_list = generate_ladders_position()
snakes_list = generate_snakes_position(ladders_list)

root.mainloop()
