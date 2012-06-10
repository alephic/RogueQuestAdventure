import libtcodpy as libtcod
import random
import math
import RQA_lists as lists

vowels = ['a','e','i','o','u']

MAP_WIDTH = 80
MAP_HEIGHT = 50

PANEL_HEIGHT = 15
STATS_WIDTH = 20

INVENTORY_WIDTH = 25

SCREEN_WIDTH = MAP_WIDTH
SCREEN_HEIGHT = MAP_HEIGHT + PANEL_HEIGHT

ROOM_MAX_SIZE = 15
ROOM_MIN_SIZE = 5

MAX_ROOMS = 15

MAX_ROOM_GOODIES = 5

visible_wall_color = libtcod.Color(0,0,0)
visible_floor_color = libtcod.Color(0,0,0)
char_wall_color = libtcod.Color(0,0,0)
char_floor_color = libtcod.Color(0,0,0)

hidden_wall_color = libtcod.Color(30,30,30)
hidden_floor_color = libtcod.Color(20,20,20)

libtcod.console_set_custom_font('terminal8x8_gs_as.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INCOL)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'RogueQuestAdventure')

map_con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)
game_over = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
inv_con = libtcod.console_new(INVENTORY_WIDTH, MAP_HEIGHT)

inv_open = False
inventory = []
inv_select = 0

took_turn = False

libtcod.console_set_background_color(game_over, libtcod.black)
libtcod.console_clear(game_over)
libtcod.console_set_foreground_color(game_over, libtcod.white)
libtcod.console_print_center(game_over, MAP_WIDTH/2, MAP_HEIGHT/2, libtcod.BKGND_NONE, 'Game Over')

experience = 0
dungeon_level = 1

blotter = [[('You awaken in a mysterious dungeon.',libtcod.white)]]

def descend():
    global blotter
    global creatures
    global items
    global dungeon_level

    dungeon_level += 1
    creatures = [player]
    items = []

    gen_map()
    blotter = [[('You descend to floor '+str(dungeon_level)+'.',libtcod.white)]]

def gen_colors():
    global visible_wall_color
    global visible_floor_color
    global char_wall_color
    global char_floor_color
    global wall_tile
    global floor_tile

    hue_walls = random.randint(0,359)
    sat_walls = 0.6
    val_walls = 0.6

    hue_floors = math.fmod(hue_walls + random.randint(140,220), 360)
    sat_floors = 0.6
    val_floors = 0.1
    
    libtcod.color_set_hsv(visible_wall_color, hue_walls, sat_walls, val_walls)
    libtcod.color_set_hsv(visible_floor_color, hue_floors, sat_floors, val_floors)

    libtcod.color_set_hsv(char_wall_color, hue_walls, sat_walls, val_walls + 0.1)
    libtcod.color_set_hsv(char_floor_color, hue_floors, sat_floors, val_floors + 0.1)

    wall_tile = Tile(True, '#', char_wall_color, visible_wall_color, hidden_wall_color)
    floor_tile = Tile(False, '/', char_floor_color, visible_floor_color, hidden_floor_color)
        
class Tile:
    def __init__(self, obstacle, char, char_color, vis_color, hidden_color, blocks_sight = 'nope'):
        self.blocks = obstacle
        if blocks_sight == 'nope':
            self.blocks_sight = self.blocks
        else:
            self.blocks_sight = blocks_sight
        self.char = char
        self.char_color = char_color
        self.vis_color = vis_color
        self.hidden_color = hidden_color

blood_bg = libtcod.Color(40,0,0)
blood_char = libtcod.Color(80,0,0)

bloody_tiles = [
    Tile(False, ';', blood_char, blood_bg, hidden_floor_color),
    Tile(False, '.', blood_char, blood_bg, hidden_floor_color),
    Tile(False, ',', blood_char, blood_bg, hidden_floor_color),
    Tile(False, ':', blood_char, blood_bg, hidden_floor_color),
]

stair_tile = Tile(False, '>', libtcod.Color(100,100,100), libtcod.Color(200,200,200), hidden_wall_color)

class Sprite:
    def __init__(self, char, color):
        self.char = char
        self.color = color

    def render(self):
        if self.owner.is_visible():
            libtcod.console_set_foreground_color(map_con, self.color)
            libtcod.console_put_char(map_con, self.owner.x, self.owner.y, self.char, libtcod.BKGND_NONE)

class ai_player:
    def __init__(self):
        self.alliance = 'player'

    def take_turn(self):
        global player_motion
        player.move(player_motion[0], player_motion[1])

        for item in items:
            if item.x == player.x and item.y == player.y:
                inventory.insert(0, item)
                announce('You found a '+item.name+'!')
                items.remove(item)

        if tile_map[player.x][player.y] == stair_tile:
            descend()

class ai_simple_melee:
    def __init__(self):
        self.alliance = 'enemy'
        self.has_seen_player = False

    def take_turn(self):
        if self.owner.is_visible():
            self.has_seen_player = True
        if self.has_seen_player:
            self.path_toward(player.x, player.y)

    def path_toward(self, target_x, target_y):
        if libtcod.path_compute(base_path, self.owner.x, self.owner.y, target_x, target_y):
            (path_x, path_y) = libtcod.path_get(base_path, 0)
            dx = path_x - self.owner.x
            dy = path_y - self.owner.y
            self.owner.move(dx, dy)

class Weapon:
    def __init__(self, name, attribute, enchantment, power, bonus):
        self.name = name
        self.attribute = attribute
        self.enchantment = enchantment
        self.power = power
        self.bonus = bonus

    def use(self):
        player.weapon = self
        announce('You are now wielding the '+self.full_name()+'.')

    def full_name(self):
        fullname = self.name
        if self.attribute:
            fullname = self.attribute+' '+fullname
        if self.enchantment:
            fullname = fullname+' of '+self.enchantment
        if self.bonus > 0:
            fullname = '+'+str(self.bonus)+' '+fullname
        return fullname

unarmed = Weapon('fists', 'bare', None, 1, 0)

class Creature:
    def __init__(self, name, adjective, x, y, sprite, ai, level, strength, agility, health):
        self.x = x
        self.y = y
        self.name = name
        self.adjective = adjective
        self.sprite = sprite
        self.ai = ai
        self.level = level
        self.strength = strength
        self.agility = agility
        self.health = health
        self.max_health = health
        
        self.sprite.owner = self
        self.ai.owner = self

        self.weapon = unarmed

        self.was_visible = False
        self.dead = False

    def move(self, dx, dy):
        target_x = self.x + dx
        target_y = self.y + dy

        is_blocked = False
        
        for creature in creatures:
            if creature.x == target_x and creature.y == target_y:
                if not self.ai.alliance == creature.ai.alliance:
                    self.attack(creature)
                is_blocked = True

        if tile_map[target_x][target_y].blocks:
            is_blocked = True

        if not is_blocked:
            self.x = target_x
            self.y = target_y

    def full_name(self):
        fullname = self.name
        if self.adjective:
            fullname = self.adjective+' '+fullname
        return fullname

    def attack(self, victim):
        global experience
        
        evade_roll = random.randint(0, 100 + victim.agility)
        if evade_roll > 100:
            announce(victim.full_name().capitalize()+' dodged the '+self.full_name()+'\'s attack!', color = victim.sprite.color)
        else:
            damage = int(math.ceil(float(self.strength)/10.0 * self.weapon.power + self.weapon.bonus))
            victim.health -= damage
            victim.health = max(victim.health, 0)
            if self == player:
                announce('You '+random.choice(lists.attacks)+' the '+victim.full_name()+' with your '+self.weapon.name+'!')
            elif victim == player:
                announce('The '+self.full_name()+' '+random.choice(lists.attacks)+'s you!', color = self.sprite.color)
                
            if victim.health <= 0:
                if self == player:
                    experience += victim.level
                victim.die()

    def die(self):
        creatures.remove(self)
        announce('The '+self.full_name()+' was slain!', color = libtcod.Color(196,0,0))
        self.dead = True

    def is_visible(self):
        visible = libtcod.map_is_in_fov(path_map, self.x, self.y)
        if visible and not self.was_visible and not self == player:
            announce('You see a level '+str(self.level)+' '+self.full_name()+'!', color = self.sprite.color)
            self.was_visible = True
        return visible

player = Creature('player', '', 0, 0, Sprite('@',libtcod.white), ai_player(), 1, 10, 10, 10)
creatures = [player]
items = []

def random_monster(x,y):
    name = random.choice(lists.monster_names)
    level = dungeon_level
    if random.randint(0,1) == 1:
        adjective = random.choice(lists.monster_attributes)
        level += random.randint(1,dungeon_level)
    else:
        adjective = None
    strength = int(round(level * (random.random()+1.0)))
    agility = int(round(level * (random.random()+1.0)))
    health = int(round(level * (random.random()+1.0)))
    hue = lists.monster_colors[name]
    color = libtcod.Color(0,0,0)
    libtcod.color_set_hsv(color, hue, 0.8, 1.0)
    sprite = Sprite(name[0], color)
    new_creature = Creature(name, adjective, x, y, sprite, ai_simple_melee(), level, strength, agility, health)
    return new_creature

def random_weapon():
    name = random.choice(lists.weapon_names)
    power = int(round(dungeon_level*(random.random() + 1)))
    bonus = 0
    if random.randint(0,1) == 1:
        attribute = random.choice(lists.weapon_traits)
        bonus += random.randint(1,dungeon_level)
    else:
        attribute = None

    if random.randint(0,1) == 1:
        enchantment = random.choice(lists.weapon_enchantments)
        bonus += random.randint(1,dungeon_level)
    else:
        enchantment = None
    new_weapon = Weapon(name, attribute, enchantment, power, bonus)
    return new_weapon

def random_food():
    name = random.choice(lists.food_names)
    value = random.randint(1, 10)
    new_food = Food(name, value)
    return new_food

class Item:
    def __init__(self, x, y, sprite, content):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.content = content
        self.name = self.content.full_name()
        
        self.sprite.owner = self
        self.content.owner = self

    def is_visible(self):
        visible = libtcod.map_is_in_fov(path_map, self.x, self.y) and not self in inventory
        return visible

    def drop(self):
        inventory.remove(self)
        self.x = player.x
        self.y = player.y
        items.append(self)
        announce('You dropped the '+self.name+'.')
        if player.weapon == self.content:
            player.weapon = unarmed
    
class Food:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def use(self):
        inventory.remove(self.owner)
        max_healed = player.max_health - player.health
        player.health = min(player.health + self.value, player.max_health)
        announce('You ate the '+self.name+'! Health restored by '+str(min(self.value, max_healed))+' points.')

    def full_name(self):
        return self.name
        
class Rect:
    def __init__(self, x, y, w,  h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

def carve_room(room):
    global tile_map
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            tile_map[x][y] = floor_tile

def carve_h_tunnel(x1, x2, y):
    global tile_map

    for x in range(min(x1,x2), max(x1,x2) + 1):
        tile_map[x][y] = floor_tile

def carve_v_tunnel(y1, y2, x):
    global tile_map

    for y in range(min(y1,y2), max(y1,y2) + 1):
        tile_map[x][y] = floor_tile

def populate(room):
    blocked = []
    goodies = random.randint(1, MAX_ROOM_GOODIES)
    
    for i in range(goodies):
        x = random.randint(room.x1+1, room.x2-1)
        y = random.randint(room.y1+1, room.y2-1)
        if [x,y] not in blocked:
            chance = random.randint(0,100)
            if chance > 25:
                creatures.append(random_monster(x, y))
            elif chance > 20:
                wep = random_weapon()
                sprite = Sprite('!', libtcod.white)
                items.append(Item(x, y, sprite, wep))
            else:
                fud = random_food()
                sprite = Sprite('%', libtcod.white)
                items.append(Item(x, y, sprite, fud))
        blocked.append([x,y])

def gen_map():

    global tile_map
    global explore_map
    global path_map
    global base_path
    
    gen_colors()
    
    tile_map = [[ wall_tile
                 for y in range(MAP_HEIGHT) ]
               for x in range(MAP_WIDTH) ]

    explore_map = [[ False
                     for y in range(MAP_HEIGHT) ]
                   for x in range(MAP_WIDTH) ]

    rooms = []
    num_rooms = 0

    for r in range(MAX_ROOMS):
        w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = random.randint(1, MAP_WIDTH - w - 2)
        y = random.randint(1, MAP_HEIGHT - h - 2)
        new_room = Rect(x, y, w, h)

        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
        if not failed:
            carve_room(new_room)
            (new_x, new_y) = new_room.center()

            if num_rooms == 0:
                player.x = new_x
                player.y = new_y
            else:
                populate(new_room)
                (prev_x, prev_y) = rooms[num_rooms-1].center()

                if random.randint(0,1) == 1:
                    carve_h_tunnel(prev_x, new_x, prev_y)
                    carve_v_tunnel(prev_y, new_y, new_x)
                else:
                    carve_h_tunnel(prev_x, new_x, new_y)
                    carve_v_tunnel(prev_y, new_y, prev_x)
            rooms.append(new_room)
            num_rooms += 1
    last_room = rooms[num_rooms-1]
    (stairs_x, stairs_y) = last_room.center()
    tile_map[stairs_x][stairs_y] = stair_tile

    path_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            libtcod.map_set_properties(path_map, x, y, not tile_map[x][y].blocks, not tile_map[x][y].blocks_sight)
    base_path = libtcod.path_new_using_map(path_map)

def blit_consoles(dead = False):
    libtcod.console_blit(map_con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)
    libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, MAP_HEIGHT)
    if dead:
        libtcod.console_blit(game_over, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0, bfade = 0.5)
    elif inv_open:
        libtcod.console_blit(inv_con, 0, 0, INVENTORY_WIDTH, MAP_HEIGHT, 0, MAP_WIDTH-INVENTORY_WIDTH, 0)

def render_all():
    libtcod.map_compute_fov(path_map, player.x, player.y, 0, True, libtcod.FOV_SHADOW)

    libtcod.console_set_background_color(map_con, libtcod.black)
    libtcod.console_clear(map_con)

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if not libtcod.map_is_in_fov(path_map, x, y):
                if explore_map[x][y]:
                    libtcod.console_set_back(map_con, x, y, tile_map[x][y].hidden_color, libtcod.BKGND_SET)
            else:
                libtcod.console_set_background_color(map_con, tile_map[x][y].vis_color)
                libtcod.console_set_foreground_color(map_con, tile_map[x][y].char_color)
                libtcod.console_put_char(map_con, x, y, tile_map[x][y].char, libtcod.BKGND_SET)
                explore_map[x][y] = True

    entities = items + creatures
    for entity in entities:
        entity.sprite.render()

    render_panel()
    render_inventory()

    blit_consoles()

def render_panel():
    libtcod.console_set_background_color(panel, libtcod.black)
    libtcod.console_clear(panel)
    #bar
    libtcod.console_set_foreground_color(panel, libtcod.white)
    for x in range(SCREEN_WIDTH):
        libtcod.console_put_char(panel, x, 0, '_', libtcod.BKGND_NONE)
    for y in range(PANEL_HEIGHT - 1):
        libtcod.console_put_char(panel, STATS_WIDTH, y+1, '|', libtcod.BKGND_NONE)

    #stats
    libtcod.console_print_left(panel, 1, 2, libtcod.BKGND_NONE, 'Level '+str(player.level))
    libtcod.console_print_left(panel, 1, 3, libtcod.BKGND_NONE, 'Health: '+str(player.health)+'/'+str(player.max_health))
    draw_bar(1, 4, STATS_WIDTH-2, player.health, player.max_health, libtcod.Color(255,0,0), libtcod.Color(128,0,0))
    libtcod.console_print_left(panel, 1, 6, libtcod.BKGND_NONE, 'Exp: '+str(experience)+'/'+str(player.level*10))
    draw_bar(1, 7, STATS_WIDTH-2, experience, player.level*10, libtcod.Color(0,255,255),libtcod.Color(0,64,64))
    libtcod.console_print_left(panel, 1, 9, libtcod.BKGND_NONE, 'Strength: '+str(player.strength)+' (x'+str(player.weapon.power)+')')
    libtcod.console_print_left(panel, 1, 10, libtcod.BKGND_NONE, 'Agility: '+str(player.agility))

    render_blotter()

def render_blotter():
    global blotter
    global took_turn
    
    reached_top = False
    y = PANEL_HEIGHT - 2
    for turn in range(len(blotter)):
        messages = blotter[turn]
        for message in range(len(messages)):
            (text, color) = messages[message]
            color = libtcod.color_lerp(color, libtcod.black, min(turn * 0.2, 1))
            libtcod.console_set_foreground_color(panel, color)
            y -= libtcod.console_height_left_rect(panel, STATS_WIDTH + 2, y, SCREEN_WIDTH - STATS_WIDTH - 3, 0, text)
            libtcod.console_print_left_rect(panel, STATS_WIDTH + 2, y+1, SCREEN_WIDTH - STATS_WIDTH - 3, 0, libtcod.BKGND_NONE, text)
            if y <= 1:
                reached_top = True
                break
        if reached_top:
            break

    if took_turn:
        blotter.insert(0,[])
    blotter = blotter[0:5]

def draw_bar(x,y, width, current_val, max_val, full_color, empty_color):
    full_length = int(float(current_val)/max_val * width)

    libtcod.console_set_background_color(panel, empty_color)
    for i in range(width):
        libtcod.console_put_char(panel, x+i, y, ' ', libtcod.BKGND_SET)

    libtcod.console_set_background_color(panel, full_color)
    for i in range(full_length):
        libtcod.console_put_char(panel, x+i, y, ' ', libtcod.BKGND_SET)

def announce(message, color=libtcod.white):
    blotter[0].insert(0, (message, color))

def render_inventory():
    libtcod.console_set_background_color(inv_con, libtcod.black)
    libtcod.console_clear(inv_con)
    libtcod.console_set_foreground_color(inv_con, libtcod.white)
    for y in range(MAP_HEIGHT):
        libtcod.console_put_char(inv_con, 0, y, '|', libtcod.BKGND_NONE)

    libtcod.console_print_left(inv_con, 2, 1, libtcod.BKGND_NONE, 'Inventory:')
    y = 3
    for item_index in range(len(inventory)):
        if inv_select == item_index:
            libtcod.console_set_foreground_color(inv_con, libtcod.white)
            libtcod.console_put_char(inv_con, 2, y, '>', libtcod.BKGND_NONE)
        else:
            libtcod.console_set_foreground_color(inv_con, libtcod.Color(128,128,128))
            libtcod.console_put_char(inv_con, 2, y, '-', libtcod.BKGND_NONE)
        name = inventory[item_index].name
        y += libtcod.console_print_left_rect(inv_con, 3, y, INVENTORY_WIDTH-4, 0, libtcod.BKGND_NONE, name)

def handle_keys():
    global took_turn
    global player_motion
    global inv_open
    global inv_select
    player_motion = [0,0]
    took_turn = False
    
    key = libtcod.console_wait_for_keypress(True)

    if not inv_open:
        if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            player_motion = [0,-1]
            took_turn = True
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            player_motion = [0,1]
            took_turn = True
        elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
            player_motion = [-1,0]
            took_turn = True
        elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
            player_motion = [1,0]
            took_turn = True
        elif key.vk == libtcod.KEY_KP9:
            player_motion = [1,-1]
            took_turn = True
        elif key.vk == libtcod.KEY_KP7:
            player_motion = [-1,-1]
            took_turn = True
        elif key.vk == libtcod.KEY_KP1:
            player_motion = [-1,1]
            took_turn = True
        elif key.vk == libtcod.KEY_KP3:
            player_motion = [1,1]
            took_turn = True

        elif key.vk == libtcod.KEY_CHAR and key.c == ord('i'):
            inv_open = True

        elif key.vk == libtcod.KEY_CHAR and key.c == ord('l'):
            announce('You examine your surroundings.')
            for creature in creatures:
                creature.was_visible = False
    else:
        if key.vk == libtcod.KEY_CHAR and key.c == ord('i'):
            inv_open = False
        elif key.vk == libtcod.KEY_CHAR and key.c == ord('e') and not inventory == []:
            inventory[inv_select].content.use()
        elif key.vk == libtcod.KEY_CHAR and key.c == ord('d') and not inventory == []:
            inventory[inv_select].drop()
        elif key.vk == libtcod.KEY_UP:
            inv_select -= 1
        elif key.vk == libtcod.KEY_DOWN:
            inv_select += 1

        inv_select = max(inv_select, 0)
        inv_select = min(inv_select, max(len(inventory)-1,0))

gen_map()

while not libtcod.console_is_window_closed():

    render_all()

    libtcod.console_flush()

    if not player.dead:
        handle_keys()
    else:
        blit_consoles(dead = True)
        libtcod.console_flush()
        libtcod.console_wait_for_keypress(True)
        quit()

    if took_turn:
        for creature in creatures:
            creature.ai.take_turn()
    
    if experience >= player.level*10:
        player.level += 1
        player.strength += random.randint(1,2)
        player.agility += random.randint(1,2)
        player.max_health += random.randint(1,2)
        announce('Level up!')
        announce('Strength increased to '+str(player.strength)+'!')
        announce('Agility increased to '+str(player.agility)+'!')
        announce('Health increased to '+str(player.max_health)+'!')
        experience = 0
