from random import shuffle
from functools import reduce
from sys import stdout

class Card():
    colors = ['red', 'green', 'blue', 'yellow']
    values = list(range(10)) + ['+4', '+2', 'color switch', 'reverse', 'skip']
    
    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.is_action = isinstance(value, str)

    def __str__(self):
        return card_format(self)
        
def card_format(card):
    formatted_card = "[ " + str(card.value) + " " + card.color + " ]"
    return formatted_card
        

class Player():
    def __init__(self, cards):
        self.cards = cards
    
    def display_cards(self):
        for idx, card in enumerate(self.cards):
            print(idx, ". ", card, sep="", end="   ")
        print("\n")
    
    def step(self, top_card, next_card):
        self.display_cards()
        
        invalid_card = True
        step = -1
        
        any_value_match = any(map(lambda card: card.value == top_card.value, self.cards))
        any_color_match = any(map(lambda card: card.color == top_card.color, self.cards))
        
        if any_value_match and any_color_match:
            while invalid_card:
                step = int(input("\rEnter the number of the card you would like to play: "))
                if 0 <= step < len(self.cards):
                    
                    value_match = self.cards[step].value == top_card.value
                    color_match = self.cards[step].color == top_card.color
                    
                    if value_match or color_match:
                        chosen_card = self.cards[step]
                        del self.cards[step]
                        return chosen_card, False
                    else:
                        stdout.write("\rThis card cannot be played\n")
                else:
                    stdout.write("\rThis card does not exist\n")
        else:
            self.cards.append(next_card)
            # handle getting a new card
            return top_card, True
            pass
        
    def sort_hand(self):
        # Logic for sorting cards in hand
        pass
    
        
class Uno():
    def __init__(self, num_players):
        self.num_players = num_players
        self.deck = self.generate_deck()
        self.players = self.distribute_cards(num_players)
        self.start()
        
    def generate_deck(self):
        deck = []
        
        for color in Card.colors:
            for value in Card.values:
                deck.append(Card(value, color))
        shuffle(deck)
        
        return deck
    
    def distribute_cards(self, num_players):
        players = []
        
        for i in range(num_players):
            cards_to_hand = self.deck[:7] # fetch 7 cards from the top of the deck
            del self.deck[:7] # constant time card removal
            players.append(Player(cards_to_hand))
        
        return players
    
    def start(self):
        self.top_card = self.deck[0]
        print("Hellu", self.top_card)
        del self.deck[0]
        
        turn = 0
        while len(self.deck) > 0 and reduce(lambda player_1, player_2:
                len(player_1.cards) * len(player_2.cards), self.players):
            print("Card on top:", self.top_card)
            print("Player {0}'s turn:".format(turn % self.num_players + 1))
            self.top_card, got_new_card = self.players[turn].step(self.top_card, self.deck[0])

            if got_new_card:
                del self.deck[0]

            turn = (turn + 1) % self.num_players
    
game = Uno(2)
game.players[0].display_cards()