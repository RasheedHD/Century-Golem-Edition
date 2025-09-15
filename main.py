import pygame
from sys import exit
from random import shuffle
from math import dist
from os import environ

class MerchantCard:
    def __init__(self):
        pass


class CrystalCard(MerchantCard):
    def __init__(self, crystals, image):
        self.crystals = crystals
        self.image = image

    def __str__(self):
        return str(self.crystals)    


class UpgradeCard(MerchantCard):
    def __init__(self, num_upgrades, image):
        self.num_upgrades = num_upgrades
        self.image = image
    
    def __str__(self):
        return f'{self.num_upgrades} upgrade card'


class TradeCard(MerchantCard):
    def __init__(self, cost_crystals, gain_crystals, image):
        self.cost_crystals = cost_crystals
        self.gain_crystals = gain_crystals
        self.image = image


class Player:
    def __init__(self, name, inventory, active_cards, inactive_cards, golems, points, position):
        self.name = name
        self.inventory = inventory
        self.active_cards = active_cards
        self.inactive_cards = inactive_cards
        self.golems = golems
        self.points = points
        self.position = position

    @classmethod
    def from_name(cls, name, position):
        if position == 1:
            return cls(name, {'Yellow': 3, 'Green': 0, 'Blue': 0, 'Pink': 0}, [UpgradeCard(3, ""), CrystalCard({'Yellow': 2}, "")], [], [], 0, position)
        elif position in [2, 3]:
            return cls(name, {'Yellow': 4, 'Green': 0, 'Blue': 0, 'Pink': 0}, [UpgradeCard(2, ""), CrystalCard({'Yellow': 2}, "")], [], [], 0, position)
        elif position in [4, 5]:
            return cls(name, {'Yellow': 3, 'Green': 1, 'Blue': 0, 'Pink': 0}, [UpgradeCard(3, ""), CrystalCard({'Yellow': 2}, "")], [], [], 0, position)
        
    def add_crystals(self, crystals_to_add):
        for crystal in crystals_to_add:
            self.inventory[crystal] += crystals_to_add[crystal]

    def acquire(self, card):
        global selected_crystals
        card_position = cards.index(card)
        if card_position == 0:
            self.add_crystals(freebies[card_position])
            freebies[card_position] = {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}

            self.active_cards.append(card)
            cards.remove(card)
            print('Successfully added card!')
            return True

        else:
            if card_position > sum(self.inventory.values()):
                print('Not enough crystals to acquire card!')
                return False
            temp_inventory = self.inventory.copy()
            self.add_crystals(freebies[card_position - 1])
            if len(selected_crystals) == card_position:
                for selected_crystal_pos in selected_crystals:
                        c=0
                        for crystal in self.inventory:
                            for unit in range(self.inventory[crystal]):
                                if selected_crystal_pos == c:
                                    temp_inventory[crystal] -= 1
                                c+=1
                self.inventory = temp_inventory
            else:
                selected_crystals.clear()
                print("Please select a valid number of crystals!")
                return False

            for freebie in freebies[card_position]:
                self.inventory[freebie] += freebies[card_position][freebie]
            freebies[card_position] = {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}

            self.active_cards.append(card)
            cards.remove(card)
            selected_crystals.clear()
            print('Successfully added card!')
            return True



    def rest(self):
        if self.inactive_cards:
            self.active_cards = self.active_cards + self.inactive_cards
            self.inactive_cards = []
            print('Successfully rested!')
            return True
        else:
            print('No inactive cards!')
            return False

    def __str__(self):
        return self.name
    
    def buy_golem(self, golem):
        global copper_coins
        global silver_coins
        global silver_coins_slid
        for crystal in golem.crystals:
            if self.inventory[crystal] < golem.crystals[crystal]:
                print('Insufficient crystals!')
                return False
            
        for crystal, crystal_count in golem.crystals.items():
            self.inventory[crystal] -= crystal_count  

        self.points += golem.points
        if golems.index(golem) == 0 and copper_coins > 0:
            copper_coins -= 1
            self.points += 3
        elif golems.index(golem) == 0 and silver_coins > 0 and silver_coins_slid:
            silver_coins -= 1
            self.points += 1
        elif (golems.index(golem) == 1 and silver_coins > 0) and (not silver_coins_slid):
            silver_coins -= 1
            self.points += 1
        if copper_coins == 0:
            silver_coins_slid = True
            
        golems.remove(golem)
        self.golems.append(golem)
        print('Successfully purchased Golem!')
        return True
    
    def play(self, card):
        if isinstance(card, CrystalCard):
            for crystal in card.crystals:
                self.inventory[crystal] += card.crystals[crystal]
            self.inactive_cards.append(card)
            self.active_cards.remove(card)
            print('Successfully used Crystal Card!')
            return True
        elif isinstance(card, TradeCard):
            for crystal in card.cost_crystals:
                if self.inventory[crystal] < card.cost_crystals[crystal]:
                    print('Insufficient Crystals!')
                    return False
            for crystal in card.cost_crystals:
                self.inventory[crystal] -= card.cost_crystals[crystal]
            for crystal in card.gain_crystals:
                self.inventory[crystal] += card.gain_crystals[crystal]
            self.inactive_cards.append(card)
            self.active_cards.remove(card)
            print('Succesfully used Trade Card!')
            return True
        
        elif isinstance(card, UpgradeCard): #Input validation needs to be implemented
            if len(selected_crystals) > card.num_upgrades or len(selected_crystals) == 0:
                print(f'Please select {card.num_upgrades} cards or less! (Not zero)')
                selected_crystals.clear()
                return False
            temp_inventory = self.inventory.copy()
            round_finished = False
            if len(selected_crystals) == card.num_upgrades:
                for selected_crystal_pos in selected_crystals:
                    c=0
                    for crystal in self.inventory:
                        for unit in range(self.inventory[crystal]):
                            if selected_crystal_pos == c:
                                temp_inventory[crystal] -= 1
                                if crystal == 'Yellow':
                                    temp_inventory['Green'] += 1
                                elif crystal == 'Green':
                                    temp_inventory['Blue'] += 1
                                elif crystal == 'Blue':
                                    temp_inventory['Pink'] += 1
                            c+=1
            elif len(selected_crystals) == card.num_upgrades-1:
                for selected_crystal_pos in selected_crystals:
                    c=0
                    for crystal in self.inventory:
                        for unit in range(self.inventory[crystal]):
                            if selected_crystal_pos == c:
                                temp_inventory[crystal] -= 1
                                if round_finished:
                                    round_finished = False
                                    if crystal == 'Yellow':
                                        temp_inventory['Green'] += 1
                                    elif crystal == 'Green':
                                        temp_inventory['Blue'] += 1
                                    elif crystal == 'Blue':
                                        temp_inventory['Pink'] += 1
                                else:
                                    if crystal == 'Yellow':
                                        temp_inventory['Blue'] += 1
                                    elif crystal == 'Green':
                                        temp_inventory['Pink'] += 1
                                    round_finished = True
                            c+=1
            else:
                temp_inventory['Yellow'] -= 1
                temp_inventory['Pink'] += 1
            self.inventory = temp_inventory.copy()
            selected_crystals.clear()
            self.inactive_cards.append(card)
            #self.active_cards.remove(card)
            print('Successfully upgraded crystals!')
            #return True
    def remove_excess_crystals(self):
        num_crystals = sum(self.inventory.values())
        if num_crystals <= 10:
            return True
        if len(selected_crystals) != num_crystals - 10:
            selected_crystals.clear()
            print("Please select a valid number of crystals to return!")
            return False
        
        temp_inventory = self.inventory.copy()
        for selected_crystal_pos in selected_crystals:
                    c=0
                    for crystal in self.inventory:
                        for unit in range(self.inventory[crystal]):
                            if selected_crystal_pos == c:
                                temp_inventory[crystal] -= 1
                            c+=1
        self.inventory = temp_inventory
        selected_crystals.clear()
        print("Successfully returned excess crystals!")
        return True
                

class Golem:
    def __init__(self, crystals, points, image):
        self.crystals = crystals
        self.points = points
        self.image = image

    def __str__(self):
        return self.crystals, self.points
    
def move_next():
    global move_text_surface
    global turn_text_surface
    global move
    global turn
    global final_turn
    if move != 3:
                move += 1
                move_text_surface = move_font.render(f"{players[move]}'s move", True, 'White')
    else:
        if not final_turn:
            move = 0
            turn += 1
            move_text_surface = move_font.render(f"{players[move]}'s move", True, 'White')
            turn_text_surface = turn_font.render(f'Turn {turn}', True, 'White')
        else:
            game_over()

def game_over():
    points = []
    leaderboard = []
    max = -1
    players_copy = players.copy()
    for player in players:
        points.append(player.points)
    points.sort(reverse=True)
    for score in points:
        for player in players_copy:
            if score == player.points:
                leaderboard.append(player)
                players_copy.remove(player)
    if leaderboard[0].points == leaderboard[1].points:
        winning_score = leaderboard[0].points
        for player in players:
            if player.points == winning_score and player.position > max:
                max = player.position
                max_player = player
        maxdex = leaderboard.index(max_player)
        temp = leaderboard[0]
        leaderboard[0] = max_player
        leaderboard[maxdex] = temp
    for player in leaderboard:
        print(f'{leaderboard.index(player)+1}: {player.name} - {player.points} points ')
    print('Game over!')
    exit()

def load_crystals(player): #For the future, if you want user to be able to remove ANY excess crystals (not just the 10 least valuable ones), possibly add a second page to the caravan. Users can cycle through pages with a key.
    i=0
    for crystal, crystal_count in player.inventory.items():
        for x in range(crystal_count):
            if i >= 10:
                return
            else:
                if crystal == 'Yellow':
                    color = (255, 255, 0)
                elif crystal == 'Green':
                    color = (0, 255, 0)
                elif crystal == 'Blue':
                    color = (64, 224, 208)
                else:
                    color = (253, 61, 181)
                coordinate = crystal_positions[i]    
                pygame.draw.circle(screen, color, coordinate, 20)
            i+=1

def load_golems():
    i = 0
    for golem in golems[:5]:
        coordinate = golem_positions[i]
        golem_surf = pygame.image.load(golem.image)
        golem_rect = golem_surf.get_rect(topleft = coordinate)
        screen.blit(golem_surf, golem_rect)
        i+=1

def load_merchant_cards():
    i = 0
    for card in cards[:6]:
        coordinate = merchant_card_positions[i]
        merchant_surf = pygame.image.load(card.image)
        merchant_rect = merchant_surf.get_rect(topleft = coordinate)
        screen.blit(merchant_surf, merchant_rect)
        i+=1

def select():
    pos = pygame.mouse.get_pos()
    for circle_pos in crystal_positions:
        distance = dist(pos, circle_pos)
        if distance <= 20:
            curr_circle_clicked = crystal_positions.index(circle_pos)
            if curr_circle_clicked in selected_crystals:
                print("Crystal already selected!")
            else:   
                print(f"Crystal {curr_circle_clicked} selected!")
                selected_crystals.append(curr_circle_clicked)


pygame.init() #When finished with everything, switch back width and height to be 1199x630 so main menu appears upon startup (1920x1080)
screen_width = 1199
screen_height = 630
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Century: Golem Edition")
clock = pygame.time.Clock()

turn_font = pygame.font.Font(None, 110)
move_font = pygame.font.Font(None, 80)
start_font = pygame.font.Font(None, 115)
settings_font = pygame.font.Font(None, 60)


start_surface = start_font.render(f'Start', True, 'Black')
start_rect = start_surface.get_rect(center = (599, 450))

settings_surface = settings_font.render(f'Settings', True, 'gray16')
settings_rect = settings_surface.get_rect(center = (599, 520))

board_surface = pygame.image.load('Graphics/Background.jpg').convert()
main_menu_surface = pygame.image.load('Graphics/Main Menu.png').convert()

merchant_back_surf = pygame.image.load('Graphics/Merchant_Card_Back.png').convert_alpha()
merchant_back_rect = merchant_back_surf.get_rect(topleft = (1650, 480))

golem_back_surf = pygame.image.load('Graphics/Golem_Card_Back.png').convert_alpha()
golem_back_rect = golem_back_surf.get_rect(topleft = (1650, 80))

caravan_surf = pygame.image.load('Graphics/Caravan_Card_Back.png').convert_alpha()
caravan_rect = caravan_surf.get_rect(bottomleft = (30, 1100))

merchant_surf6 = pygame.image.load('Graphics/Merchant_Card_Back.png').convert_alpha()
merchant_rect6 = merchant_surf6.get_rect(topleft = (1650-220*1, 480))

merchant_surf5 = pygame.image.load('Graphics/Merchant_Card_Back.png').convert_alpha()
merchant_rect5 = merchant_surf5.get_rect(topleft = (1650-220*2, 480))

merchant_surf4 = pygame.image.load('Graphics/Merchant_Card_Back.png').convert_alpha()
merchant_rect4 = merchant_surf4.get_rect(topleft = (1650-220*3, 480))

merchant_surf3 = pygame.image.load('Graphics/Merchant_Card_Back.png').convert_alpha()
merchant_rect3 = merchant_surf3.get_rect(topleft = (1650-220*4, 480))

merchant_surf2 = pygame.image.load('Graphics/Merchant_Card_Back.png').convert_alpha()
merchant_rect2 = merchant_surf2.get_rect(topleft = (1650-220*5, 480))

merchant_surf1 = pygame.image.load('Graphics/Merchant_Card_Back.png').convert_alpha()
merchant_rect1 = merchant_surf1.get_rect(topleft = (1650-220*6, 480))

golem_surf5 = pygame.image.load('Graphics/Golem_Card_Back.png').convert_alpha()
golem_rect5 = golem_surf5.get_rect(topleft = (1650-220*1, 80))

golem_surf4 = pygame.image.load('Graphics/Golem_Card_Back.png').convert_alpha()
golem_rect4 = golem_surf4.get_rect(topleft = (1650-220*2, 80))

golem_surf3 = pygame.image.load('Graphics/Golem_Card_Back.png').convert_alpha()
golem_rect3 = golem_surf3.get_rect(topleft = (1650-220*3, 80))

golem_surf2 = pygame.image.load('Graphics/Golem_Card_Back.png').convert_alpha()
golem_rect2 = golem_surf2.get_rect(topleft = (1650-220*4, 80))

golem_surf1 = pygame.image.load('Graphics/Golem_Card_Back.png').convert_alpha()
golem_rect1 = golem_surf1.get_rect(topleft = (1650-220*5, 80))


players = [
    Player.from_name('P1', 1),
    Player.from_name('P2', 2),
    Player.from_name('P3', 3),
    Player.from_name('P4', 4)
]

copper_coins = 2 * len(players)
silver_coins = 2 * len(players)

golems = [
    Golem({'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}, 15, ""),
    Golem({'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}, 10, ""),
    Golem({'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}, 5, ""),
    Golem({'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}, 15, ""),
    Golem({'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}, 20, ""),
    Golem({'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}, 20, ""),
    Golem({'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}, 20, ""),
    Golem({'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}, 20, ""),
]

cards = [
    TradeCard({'Yellow': 2}, {'Green': 2}, ""),
    CrystalCard({'Yellow': 4}, ""),
    CrystalCard({'Pink': 1}, ""),
    CrystalCard({'Blue': 1}, ""),
    CrystalCard({'Green': 2}, ""),
]

freebies = [
    {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0},
    {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0},
    {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0},
    {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0},
    {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0},
    {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0},
]

crystal_positions = [
    (98, 944),
    (98+67*1, 945),
    (98+67*2, 946),
    (98+67*3, 947),
    (98+67*4, 948),
    (98, 1006),
    (98+67*1, 1007),
    (98+67*2, 1008),
    (98+67*3, 1010),
    (98+67*4, 1012),
]

golem_positions = [
    (),
    (),
    (),
    (),
    ()
]

merchant_card_positions = [
    (),
    (),
    (),
    (),
    (),
    ()
]

selected_crystals = []

#  uncomment later for real shuffling

#shuffle(golems)
#shuffle(cards)
#shuffle(players)

turn = 1
move = 0
final_turn = False
main_menu_active = True
settings_menu_active = False
silver_coins_slid = False

turn_text_surface = turn_font.render(f'Turn {turn}', True, 'White')
move_text_surface = move_font.render(f"{players[move]}'s move", True, 'White')

if len(players) >= 4:
    max_golems = 5
else:
    max_golems = 6

while True:
    if not main_menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            #if event.type == pygame.MOUSEMOTION:
            #    print(pygame.mouse.get_pos())

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    screen_width = 1199
                    screen_height = 630
                    environ['SDL_VIDEO_CENTERED'] = '1'
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                    main_menu_active = True

                if event.key == pygame.K_1:
                    if players[move].buy_golem(golems[0]):
                        if len(players[move].golems) == max_golems:
                            final_turn = True
                        
                        move_next()
                elif event.key == pygame.K_2:
                    if players[move].acquire(cards[3]):
                        move_next()
                elif event.key == pygame.K_3:
                    if players[move].play(players[move].active_cards[0]):
                        move_next()
                elif event.key == pygame.K_4:
                    if players[move].rest() or players[move].remove_excess_crystals():
                        move_next()
                elif event.key == pygame.K_5:
                    if players[move].buy_golem(golems[1]):
                        if len(players[move].golems) == max_golems:
                            final_turn = True
                        
                        move_next()
                elif event.key == pygame.K_i:
                    print(players[move].inventory)
                    print(players[move].active_cards)
                    print(players[move].inactive_cards)
                    print(players[move].golems)
                    print(players[move].points)
                elif event.key == pygame.K_SPACE:
                    move_next()
                    #load_golems()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    select()
                    print(selected_crystals)
                elif event.button == 3:
                    selected_crystals.clear()
                    print('Deselected crystals!')

                

        screen.blit(main_menu_surface, (0,0))
        screen.blit(board_surface, (0,0))
        screen.blit(turn_text_surface, (60,50))
        screen.blit(move_text_surface, (60, 140))
        if merchant_back_rect.right <= 0:
            merchant_back_rect.left = 1920
        screen.blit(merchant_back_surf, merchant_back_rect)
        screen.blit(golem_back_surf, golem_back_rect)
        screen.blit(caravan_surf, caravan_rect)
        screen.blit(merchant_surf1, merchant_rect1)
        screen.blit(merchant_surf2, merchant_rect2)
        screen.blit(merchant_surf3, merchant_rect3)
        screen.blit(merchant_surf4, merchant_rect4)
        screen.blit(merchant_surf5, merchant_rect5)
        screen.blit(merchant_surf6, merchant_rect6)
        screen.blit(golem_surf1, golem_rect1)
        screen.blit(golem_surf2, golem_rect2)
        screen.blit(golem_surf3, golem_rect3)
        screen.blit(golem_surf4, golem_rect4)
        screen.blit(golem_surf5, golem_rect5)
        if silver_coins_slid:
            pygame.draw.circle(screen, (113,112,110), (663, 50), 30)
        else:
            pygame.draw.circle(screen, (137,55,39), (663, 50), 30)
            pygame.draw.circle(screen, (113,112,110), (882, 50), 30)
            
       
        load_crystals(players[move])
        #load_golems()
        #load_merchant_cards

        pygame.display.update()
        clock.tick(60)
        ###
    elif main_menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    pass

            if event.type == pygame.MOUSEBUTTONUP:
                if start_rect.collidepoint(event.pos):
                    screen_width = 1920
                    screen_height = 1080
                    environ['SDL_VIDEO_CENTERED'] = '1'
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                    main_menu_active = False

            if start_rect.collidepoint(mouse_pos):
                start_surface = start_font.render(f'Start', True, 'Red')
            else:
                start_surface = start_font.render(f'Start', True, 'Black')

            if settings_rect.collidepoint(mouse_pos):
                settings_surface = settings_font.render(f'Settings', True, 'Red')
            else:
                settings_surface = settings_font.render(f'Settings', True, 'grey16')


        screen.blit(main_menu_surface, (0,0))
        screen.blit(start_surface, start_rect)
        screen.blit(settings_surface, settings_rect)
        pygame.display.update()
        clock.tick(60)