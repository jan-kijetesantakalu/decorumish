global WIDTH, HEIGHT, colours, styles, types, canvas, canvas_label, canvas_tk, cursor_pos, cursor_order, redraw #, SCALE


redraw = True
types   = ["lamp", "hanging", "tat"]
colours = ["red", "blue", "green", "yellow"]
styles  = ["modern", "antique", "retro", "unusual"]
cursor_pos = 0
cursor_order = [("bathroom", "wall"), ("bathroom", "hanging"), ("bathroom", "tat"), ("bathroom", "lamp"), 
                ("bedroom", "wall"), ("bedroom", "tat"), ("bedroom", "lamp"), ("bedroom", "hanging"),
                ("lounge", "wall"), ("lounge", "tat"), ("lounge", "hanging"), ("lounge", "lamp"),
                ("kitchen", "wall"), ("kitchen", "lamp"), ("kitchen", "hanging"), ("kitchen", "tat")]

import tkinter as tk
from random import *
from PIL import Image, ImageTk

#Initial Room Definition

rooms = {"kitchen": {}, "bedroom": {}, "bathroom":{}, "lounge": {}} #Contains the rooms

rooms["kitchen"]  = {
        "colour": choice(colours), 
                     
        "hanging": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 71, "ypos": 59}, 
        "lamp": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 39, "ypos": 86},
        "tat": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 143, "ypos": 86},
                    
        "top": False,
        "left": False,
                    
        "img": None,
        "xpos": None,
        "ypos": None
}

rooms["bedroom"]  = {
       "colour": choice(colours), 
        
        "hanging": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 171, "ypos": 67}, 
        "lamp": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 115, "ypos": 107},
        "tat": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 77, "ypos": 95},
                    
        "top": True,
        "left": False,
                    
        "img": None,
        "xpos": None,
        "ypos": None
}

rooms["bathroom"]  = {
        "colour": choice(colours), 
                    
        "hanging": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos":51, "ypos":95}, 
        "lamp": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos":183, "ypos":67},
        "tat": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos":103, "ypos":123},
        
        "top": True,
        "left": True,
                    
        "img": None,
        "xpos": None,
        "ypos": None
}

rooms["lounge"]  = {
        "colour": choice(colours), 
        
        "hanging": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 139, "ypos": 63}, 
        "lamp": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 183, "ypos": 123},
        "tat": {"colour": choice(colours), "style": choice(styles), "img": None, "label": None, "xpos": 87, "ypos": 123},
                    
        "top": False,
        "left": True,
                    
        "img": None,
        "xpos": None,
        "ypos": None            
}

#Create Root Window
root = tk.Tk()
root.attributes('-fullscreen', True)

def cursor_next(e):
    global cursor_pos, redraw
    cursor_pos += 1
    cursor_pos %= 16
    redraw = True

def cursor_prev(e):
    global cursor_pos, redraw
    cursor_pos -= 1
    cursor_pos %= 16
    redraw = True

def handle_keypress(e):
    global cursor_pos, redraw
    
    cursor_loc = cursor_order[cursor_pos]
    cursor_room = rooms[cursor_loc[0]]
    cursor_obj = cursor_room[cursor_loc[1]] if cursor_loc[1] != "wall" else cursor_room
    
    if e.char.lower() == "a":
        cursor_obj["colour"] = "red"
    
    elif e.char.lower() == "s":
        cursor_obj["colour"] = "yellow"
    
    elif e.char.lower() == "d":
        cursor_obj["colour"] = "green"

    elif e.char.lower() == "f":
        cursor_obj["colour"] = "blue"
    

    elif cursor_loc[1] != "wall":
        if e.char.lower() == "z":
            cursor_obj["style"] = "antique"

        elif e.char.lower() == "x":
            cursor_obj["style"] = "retro"

        elif e.char.lower() == "c":
            cursor_obj["style"] = "modern"

        elif e.char.lower() == "v":
            cursor_obj["style"] = "unusual"


    redraw = True
    

    


root.bind("<Right>", cursor_next)
root.bind("<Left>", cursor_prev)
root.bind("<KeyPress>", handle_keypress)


WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

#Initialise Canvas

canvas = Image.new(mode= "RGBA", size=(596,336))





def create_object(room, rooms, obj_type):
    #Open object or placeholder
    try:
        rooms[room][obj_type]["img"] = Image.open(f'''assets/{room}/{obj_type}/{rooms[room][obj_type]["style"]}/{room}_{rooms[room][obj_type]["style"]}_{rooms[room][obj_type]["colour"]}_{obj_type}.png''')
    except FileNotFoundError:
        print(f'''Failed opening: assets/{room}/{obj_type}/{rooms[room][obj_type]["style"]}/{room}_{rooms[room][obj_type]["style"]}_{rooms[room][obj_type]["colour"]}_{obj_type}.png falling back to assets/placeholder.png''')
        rooms[room][obj_type]["img"] = Image.open(f'''assets/placeholder.png''')

    #Paste (With Alpha Mask), to the top left of room (TEMP LOCATION)
    try:
        Image.Image.paste(canvas, rooms[room][obj_type]["img"], (rooms[room][obj_type]["xpos"]+rooms[room]["xpos"]-rooms[room][obj_type]["img"].size[0]+1, rooms[room][obj_type]["ypos"]+rooms[room]["ypos"]-rooms[room][obj_type]["img"].size[1]+1), rooms[room][obj_type]["img"].convert("RGBA"))
    except KeyError:
        pass


def create_rooms(rooms):
    for room in rooms.keys():
        #Open room (or use placeholder):
        try:
            rooms[room]["img"]= Image.open(f'''assets/{room}/room/{room}_{rooms[room]["colour"]}.png''')
        except FileNotFoundError:
            try:
                print(f'''Failed opening: assets/{room}/room/{room}_{rooms[room]["colour"]} falling back to assets/{room}/room/{room}_blank.png''')
                rooms[room]["img"] = Image.open(f'''assets/{room}/room/{room}_blank.png''')
            except FileNotFoundError:
                print(f'''Failed opening: assets/{room}/room/{room}_placeholder.png falling back to assets/room_blank.png''') 
                rooms[room]["img"] = Image.open(f'''assets/room_placeholder.png''')

        #Resize Room (Rooms are upsampled 2x to make art easier) with Nearest Neighbour Resampling (best for pixel art)
        rooms[room]["img"] = rooms[room]["img"].resize((192, 128), Image.NEAREST)
        

        #Place in middle
        xpos = 298
        if rooms[room]["left"]:
            xpos -= 192
        
        #Place on floor (or on other room)
        ypos = 80
        if not rooms[room]["top"]:
            ypos += 128
        
        #Paste onto canvas (With transparency)
        Image.Image.paste(canvas, rooms[room]["img"], (xpos, ypos), rooms[room]["img"].convert("RGBA"))

        rooms[room]["xpos"] = xpos
        rooms[room]["ypos"] = ypos

        #Create objects
        for obj in types:
            create_object(room, rooms, obj)

canvas_tk = ImageTk.PhotoImage(canvas.resize((WIDTH, HEIGHT), Image.NEAREST))
canvas_label = tk.Label()
canvas_label.place(x=0, y=0)
quit = tk.Button()

def draw_canvas():
    global canvas, canvas_label, canvas_tk, cursor_order, cursor_pos
    
    #Load and Place Background
    try:
        back_img = Image.open('assets/back.png') # If house.png does not open -
    except FileNotFoundError:
        print(f'Failed opening: assets/back.png, falling-back to: assets/back_placeholder.png')
        back_img = Image.open('assets/back_placeholder.png') # - Use placeholder

    #Place background on canvas

    back_img = back_img.resize((596, 336), Image.NEAREST)
    Image.Image.paste(canvas, back_img, (0, 0))


    #Draw rooms and objects onto canvas
    create_rooms(rooms)
    
    #Draw cursor
    cursor_loc = cursor_order[cursor_pos]
    cursor_room = rooms[cursor_loc[0]]
    cursor_obj = cursor_room[cursor_loc[1]] if cursor_loc[1] != "wall" else cursor_room

    if cursor_obj["img"].size == (32,32):
        cursor_img = Image.open("assets/cursor_square.png")
        cur_xpos = cursor_obj["xpos"]-31+cursor_room["xpos"]
        cur_ypos = cursor_obj["ypos"]-31+cursor_room["ypos"]

    elif cursor_obj["img"].size == (32,64):
        cursor_img = Image.open("assets/cursor_tall.png")
        cur_xpos = cursor_obj["xpos"]-31+cursor_room["xpos"]
        cur_ypos = cursor_obj["ypos"]-63+cursor_room["ypos"]

    elif cursor_obj["img"].size == (64,32):
        cursor_img = Image.open("assets/cursor_wide.png")
        cur_xpos = cursor_obj["xpos"]-63+cursor_room["xpos"]
        cur_ypos = cursor_obj["ypos"]-31+cursor_room["ypos"]
    
    else:
        cursor_img = Image.open("assets/cursor_room.png")
        cur_xpos = cursor_obj["xpos"]
        cur_ypos = cursor_obj["ypos"]

    
    Image.Image.paste(canvas, cursor_img, (cur_xpos,cur_ypos), cursor_img.convert("RGBA"))
    
    #Convert Canvas to Tk Label and draw to screen
    #Resample to screen size using NN
    canvas_tk = ImageTk.PhotoImage(canvas.resize((WIDTH, HEIGHT), Image.NEAREST))

    canvas_label.config(image = canvas_tk)

    #Place Quit Button
    quit = tk.Button(root, text="QUIT", bg="darkred", fg = "white", command=root.destroy)
    quit.place(x = 0, y = 0) #Ugly and Hardcoded, fix later
    
draw_canvas()


#RULES

# checks 2 rules against each other, returns TRUE if they don't contradict
def rule_compatability(rule1, rule2):
    if rule1 == rule2:
        return False

    #If asking for same type of thing in same room
    if rule1["room_top"] == rule2["room_top"] and rule1["room_top"] != None and rule1["type"] == rule2["type"] and rule1["type"] != None:
        return False

    return True
 

#make rules for objects
rules = []
num_rules = 6

type_options = types*2

class VarietyException(Exception):
    pass

while len(rules) < num_rules:
    try:
        obj_variety = 192
        pos_variety = 12
        target = 24
    
        rule = {"obj": True, "room_top": None, "room_left": None, "type": None, "colour": None, "style": None}
    
        rule["room_top"] = choice([True, False, None, None])
        if rule["room_top"] != None:
            obj_variety /= 2
            pos_variety /=2
            if obj_variety * pos_variety <= target:
                raise(VarietyException)

        rule["room_left"] = choice([True, False, None, None])
        if rule["room_left"] != None:
            obj_variety /= 2
            pos_variety /= 2
            if obj_variety * pos_variety <= target: 
                raise(VarietyException) 

        if choice([True, False]):
            rule["type"] = type_options.pop(type_options.index(choice(type_options)))
        else:
            rule["type"] = None
        
        if rule["type"] != None:
            obj_variety /= 3
            pos_variety /= 3
            if obj_variety * pos_variety <= target:    
                raise(VarietyException)

        rule["colour"] = choice(colours+([None]))
        if rule["colour"] != None:
            obj_variety /= 4
            if obj_variety * pos_variety <= target:
                raise(VarietyException) 

        rule["style"] = choice(styles+([None]))
        if rule["style"] != None:
            obj_variety /= 4
            if obj_variety * pos_variety <= target:
                raise(VarietyException)

        raise(VarietyException)

    except VarietyException:
        comp = True
        for rul in rules:
            if not comp:
                break
            else:
                comp = rule_compatability(rule, rul)
        if comp:
            rules.append(rule)   
        elif rule["type"] != None:
            type_options.append(rule["type"])



# make rules for room colour
walls = []
num_wall_rules = 4
wall_option_top = [True, True, False, False]
wall_option_left = [True, True, False, False]

while len(walls) < num_wall_rules:
    wall = {"obj": False, "top": None, "left": None, "colour": None}
    valid = True
    
    if choice([True, False]):
        # choose option from list for wall option top and remove it
        wall["top"] = wall_option_top.pop(wall_option_top.index(choice(wall_option_top)))
    else:
        # set to None 1/3 of the time
        wall["top"] = None
    

    if choice([True, False]):
        # choose option from list for wall option top and remove it
        wall["left"] = wall_option_left.pop(wall_option_left.index(choice(wall_option_left)))
    else:
        # set to None 1/3 of the time
        wall["left"] = None

    wall["colour"] = choice(colours)
     
    for wal in walls:
        if wall["top"] == wal["top"] and wal["top"] != None and wall["left"] == wal["left"] and wal["left"] != None:
            valid = False
        
        if wal == wall:
            valid = False

    if not valid:
        wall_option_top.append(wall["top"])
        wall_option_left.append(wall["left"])
        continue
    else: 
        walls.append(wall)

rules += walls

for rule in rules:
    print(rule)


#Mainloop
x = 0
while root.state() == 'normal':
    root.update_idletasks()
    root.update()
    
    if redraw:
        print(f"Update {x}")
        draw_canvas()
        redraw = False

    x += 1
