import pygame
from sys import exit
from random import shuffle

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
    def __init__(self, name, inventory, active_cards, inactive_cards, golems, points):
        self.name = name
        self.inventory = inventory
        self.active_cards = active_cards
        self.inactive_cards = inactive_cards
        self.golems = golems
        self.points = points

    @classmethod
    def from_name(cls, name, position):
        if position == 1:
            return cls(name, {'Yellow': 3, 'Green': 0, 'Blue': 0, 'Pink': 0}, [UpgradeCard(2, ""), CrystalCard({'Yellow': 2}, "")], [], [], 0)
        elif position in [2, 3]:
            return cls(name, {'Yellow': 4, 'Green': 0, 'Blue': 0, 'Pink': 0}, [UpgradeCard(2, ""), CrystalCard({'Yellow': 2}, "")], [], [], 0)
        elif position == 4:
            return cls(name, {'Yellow': 3, 'Green': 1, 'Blue': 0, 'Pink': 0}, [UpgradeCard(2, ""), CrystalCard({'Yellow': 2}, "")], [], [], 0)

    def acquire(self, card):
        card_position = cards.index(card)
        if card_position == 0:
            for freebie in freebies[card_position]:
                self.inventory[freebie] += freebies[card_position][freebie]
            freebies[card_position] = {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}

            self.active_cards.append(card)
            cards.remove(card)
            print('Successfully added card!')
            return True

        else: # This whole thing should be improved to allow any crystal (not just yellows) to be sacrificed to acquire card.
            if card_position > self.inventory['Yellow']:
                print('Not enough crystals to acquire card!')
                return False
            
            for sacrificial_crystal in range(card_position):
                freebies[card_position - 1]['Yellow'] += 1
                self.inventory['Yellow'] -= 1

            for freebie in freebies[card_position]:
                self.inventory[freebie] += freebies[card_position][freebie]
            freebies[card_position] = {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}

            self.active_cards.append(card)
            cards.remove(card)
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
        elif golems.index(golem) == 1 and silver_coins > 0:
            silver_coins -= 1
            self.points += 1
            
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
            print('Succesfully used Trade Card!')
            self.inactive_cards.append(card)
            self.active_cards.remove(card)
            return True
    


class Golem:
    def __init__(self, crystals, points):
        self.crystals = crystals
        self.points = points

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
                move_text_surface = test_font_2.render(f"{players[move]}'s move", True, 'White')
    else:
        if not final_turn:
            move = 0
            turn += 1
            move_text_surface = test_font_2.render(f"{players[move]}'s move", True, 'White')
            turn_text_surface = test_font_1.render(f'Turn {turn}', True, 'White')
        else:
            game_over()

def game_over():
    print('Game over!')
    exit()

def load_crystals(player):
    i=0
    for crystal, crystal_count in player.inventory.items():
        for x in range(crystal_count):
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

pygame.init()
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Century: Golem Edition")
clock = pygame.time.Clock()

test_font_1 = pygame.font.Font(None, 110)
test_font_2 = pygame.font.Font(None, 80)

board_surface = pygame.image.load('Graphics/Background.jpg').convert()


merchant_surf = pygame.image.load('Graphics/Merchant_Card_Back.png').convert_alpha()
merchant_rect = merchant_surf.get_rect(topleft = (1650, 480))

golem_surf = pygame.image.load('Graphics/Golem_Card_Back.png').convert_alpha()
golem_rect = golem_surf.get_rect(topleft = (1650, 80))

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




#(Yellow --> Green --> Blue --> Pink).

players = [
    Player.from_name('P1', 1),
    Player.from_name('P2', 2),
    Player.from_name('P3', 3),
    Player.from_name('P4', 4)
]

copper_coins = 2 * len(players)
silver_coins = 2 * len(players)

golems = [
    Golem({'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}, 20),
    Golem({'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}, 20),
    Golem({'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}, 20),
    Golem({'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}, 20),
    Golem({'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0}, 20),
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

#  uncomment later for real shuffling

#shuffle(golems)
#shuffle(cards)

turn = 1
move = 0
final_turn = False
if len(players) >= 4:
    max_golems = 2
else:
    max_golems = 6
turn_text_surface = test_font_1.render(f'Turn {turn}', True, 'White')
move_text_surface = test_font_2.render(f"{players[move]}'s move", True, 'White')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #if event.type == pygame.MOUSEMOTION:
        #    print(pygame.mouse.get_pos())

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                if players[move].buy_golem(golems[0]):
                    if len(players[move].golems) == max_golems:
                        final_turn = True
                    move_next()
            elif event.key == pygame.K_2:
                if players[move].acquire(cards[0]):
                    move_next()
            elif event.key == pygame.K_3:
                if players[move].play(players[move].active_cards[1]):
                    move_next()
            elif event.key == pygame.K_4:
                if players[move].rest():
                    move_next()
            elif event.key == pygame.K_i:
                print(players[move].inventory)
                print(players[move].active_cards)
                print(players[move].inactive_cards)
                print(players[move].golems)
                print(players[move].points)
            elif event.key == pygame.K_SPACE:
                move_next()
            


    
    screen.blit(board_surface, (0,0))
    screen.blit(turn_text_surface, (60,50))
    screen.blit(move_text_surface, (60, 140))
    #merchant_rect.x-=5
    if merchant_rect.right <= 0:
        merchant_rect.left = 1920
    screen.blit(merchant_surf, merchant_rect)
    screen.blit(golem_surf, golem_rect)
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
    pygame.draw.circle(screen, (137,55,39), (663, 50), 30)
    pygame.draw.circle(screen, (113,112,110), (882, 50), 30)
    load_crystals(players[move])

    pygame.display.update()
    clock.tick(60)
    ###