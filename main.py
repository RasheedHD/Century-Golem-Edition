import pygame
from sys import exit
from random import shuffle

class MerchantCard:
    def __init__(self):
        pass


class CrystalCard(MerchantCard):
    def __init__(self, crystals):
        self.crystals = crystals

    def __str__(self):
        return str(self.crystals)    


class UpgradeCard(MerchantCard):
    def __init__(self, num_upgrades):
        self.num_upgrades = num_upgrades
    
    def __str__(self):
        return f'{self.num_upgrades} upgrade card'


class TradeCard(MerchantCard):
    def __init__(self, cost_crystals, gain_crystals):
        self.cost_crystals = cost_crystals
        self.gain_crystals = gain_crystals


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
            return cls(name, {'Yellow': 3, 'Green': 0, 'Blue': 0, 'Pink': 0}, [UpgradeCard(2), CrystalCard({'Yellow': 2})], [], [], 0)
        elif position in [2, 3]:
            return cls(name, {'Yellow': 4, 'Green': 0, 'Blue': 0, 'Pink': 0}, [UpgradeCard(2), CrystalCard({'Yellow': 2})], [], [], 0)
        elif position == 4:
            return cls(name, {'Yellow': 3, 'Green': 1, 'Blue': 0, 'Pink': 0}, [UpgradeCard(2), CrystalCard({'Yellow': 2})], [], [], 0)

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
        self.active_cards = self.active_cards + self.inactive_cards
        self.inactive_cards = []
        print('Successfully rested!')
        return True

    def __str__(self):
        return self.name
    
    def buy_golem(self, golem):
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
    if move != 3:
                move += 1
                move_text_surface = test_font_2.render(f"{players[move]}'s move", True, 'White')
    else:
        move = 0
        turn += 1
        move_text_surface = test_font_2.render(f"{players[move]}'s move", True, 'White')
        turn_text_surface = test_font_1.render(f'Turn {turn}', True, 'White')

        

pygame.init()
screen_width = 1736
screen_height = 980
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Century: Golem Edition")
clock = pygame.time.Clock()
test_font_1 = pygame.font.Font(None, 90)
test_font_2 = pygame.font.Font(None, 60)

board_surface = pygame.image.load('Graphics/Board 2.png').convert()


test_card_surface = pygame.image.load('Graphics/2Gold.png').convert_alpha()
test_card_rect = test_card_surface.get_rect(topleft = (1200, 500))

#Game Logic VVV (Yellow --> Green --> Blue --> Pink).

players = [
    Player.from_name('P1', 1),
    Player.from_name('P2', 2),
    Player.from_name('P3', 3),
    Player.from_name('P4', 4)
]

copper_coins = 2 * len(players)
silver_coins = 2 * len(players)

golems = [
    Golem({'Yellow': 1, 'Green': 1, 'Blue': 1, 'Pink': 3}, 20),
    Golem({'Yellow': 2, 'Green': 1}, 6)
]

cards = [
    TradeCard({'Yellow': 2}, {'Green': 2}),
    CrystalCard({'Yellow': 4}),
    CrystalCard({'Pink': 1}),
    CrystalCard({'Blue': 1}),
    CrystalCard({'Green': 2}),
]

freebies = [
    {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0},
    {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0},
    {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0},
    {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0},
    {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0},
    {'Yellow': 0, 'Green': 0, 'Blue': 0, 'Pink': 0},
]

#  uncomment later for real shuffling

#shuffle(golems)
#shuffle(cards)

turn = 1
move = 0
turn_text_surface = test_font_1.render(f'Turn {turn}', True, 'White')
move_text_surface = test_font_2.render(f"{players[move]}'s move", True, 'White')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONUP:
            pass

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                if players[move].buy_golem(golems[1]):
                    move_next()
            elif event.key == pygame.K_2:
                if players[move].acquire(cards[0]):
                    move_next()
            elif event.key == pygame.K_3:
                if players[move].play(players[move].active_cards[2]):
                    move_next()
            elif event.key == pygame.K_4:
                if players[move].rest():
                    move_next()
            elif event.key == pygame.K_i:
                print(players[move].inventory)
                print(players[move].active_cards)
                print(players[move].inactive_cards)
                print(players[move].points)
            



    screen.blit(board_surface, (0,0))
    screen.blit(turn_text_surface, (60,50))
    screen.blit(move_text_surface, (60, 140))
    test_card_rect.x-=5
    if test_card_rect.right <= 0:
        test_card_rect.left = 1736
    screen.blit(test_card_surface, test_card_rect)

    pygame.display.update()
    clock.tick(60)