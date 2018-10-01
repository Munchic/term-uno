from random import shuffle
from functools import reduce

class Card():
    colors = ['red', 'green', 'blue', 'yellow']
    values = list(range(10)) + ['+4', '+2', 'color switch', 'reverse', 'skip']
    
    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.is_action = isinstance(value, str)

    def __str__(self):
        return self.card_format()
    
    def card_format(self):
        formatted_card = "[ " + str(self.value) + " " + self.color + " ]"
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
        
        if any_value_match or any_color_match:
            while invalid_card:
                # Handle ew inputs
                step = input("\rEnter the number of the card you would like to play: ")
                try:
                    step = int(step)
                    invalid_card = False
                except ValueError:
                    print("This is not a number. Please try again.")


                if not invalid_card and 0 <= step < len(self.cards):
                    
                    value_match = self.cards[step].value == top_card.value
                    color_match = self.cards[step].color == top_card.color
                    
                    if value_match or color_match:
                        chosen_card = self.cards[step]
                        del self.cards[step]
                        return chosen_card, False
                    else:
                        print("This card cannot be played.")
                        invalid_card = True

                    if not 0 <= step < len(self.cards):
                        print("This card does not exist.")
        else:
            while step == -1:
                step = input("Pick a card from the deck or skip (get/skip): ")
                if step == "get":
                    self.cards.append(next_card)
                    return top_card, True
                elif step == "skip":
                    return top_card, False
                else:
                    step = -1
        
    def sort_hand(self):
        # Logic for sorting cards in hand
        pass
    
        
class Uno():
    '''
    GAME INITIALIZATION
    '''
    def __init__(self, num_players):
        self.num_players = num_players
        self.deck = self.generate_deck()
        self.players = self.distribute_cards(num_players)
        self.start_game()
        
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
        print(players)

        return players


    '''
    PLAYER DYNAMICS
    '''
    def clear_screen(self):
        print("\033[H\033[J")
        print("----- UNO GAME -----\n")

    def next_turn(self):
        next_turn = (self.turn + self.rotation) % self.num_players
        return next_turn

    def display_ready_screen(self):
        self.clear_screen()
        print("Card on top: \033[1m", self.top_card, '\033[0m')

        step = ""
        input("Player {0}'s turn. Press Enter to continue.".format(self.turn + 1))
        self.clear_screen()
        print("Card on top: \033[1m", self.top_card, '\033[0m')
        
    def upd_cur_action(self):
        top_value = self.top_card.value
        if top_value == 'reverse':
            self.rotation *= -1
        elif top_value in ['color switch', '+4']:
            invalid_color = True
            while invalid_color:
                color = input("Choose the next color (red, green, blue, yellow): ")
                if color in Card.colors:
                    self.top_card.color = color
                invalid_color = False

        action = {"act": self.top_card.value, "at_turn": self.next_turn(), "used": False}
        self.current_action = action

    def handle_action(self):
        if self.current_action["at_turn"] == self.turn and not self.current_action["used"]:
            self.current_action["used"] = True
            top_value = self.top_card.value
            deck_len = len(self.deck)

            if top_value == '+4':
                self.players[self.turn].cards += self.deck[:min(deck_len, 4)]
                del self.deck[:min(deck_len, 4)]
                self.turn = self.next_turn()
            elif top_value == '+2':
                self.players[self.turn].cards += self.deck[:min(deck_len, 2)]
                del self.deck[:min(deck_len, 2)]
                self.turn = self.next_turn()
            elif top_value == 'skip':
                self.turn = self.next_turn()

    def announce_winner(self):
        pass
    

    '''
    MAIN LOOP
    '''
    def start_game(self):
        self.top_card = self.deck[0]
        del self.deck[0]
        
        self.turn = 0
        self.rotation = 1
        self.current_action = {"act": None, "at_turn": None, "used": None}
        while len(self.deck) > 0 and all(map(lambda player: len(player.cards) > 0, self.players)):
            self.handle_action()
            self.display_ready_screen()

            self.clear_screen()
            print("Card on top: \033[1m", self.top_card, '\033[0m')

            print("Player {0}'s turn:".format(self.turn % self.num_players + 1))
            self.prev_top_card = self.top_card
            self.top_card, got_new_card = self.players[self.turn].step(self.top_card, self.deck[0])

            if got_new_card:
                del self.deck[0]
            if self.top_card.is_action and self.top_card != self.prev_top_card:
                self.upd_cur_action()

            self.turn = self.next_turn()
            
        
        announce_winner()
    
'''
UNO GAME
'''
print("WELCOME TO THE UNO GAME!\n")
invalid_input = True

while invalid_input:
    num_players = input("Please enter the number of players (2-8): ")

    try:
        num_players = int(num_players)
        if 2 <= num_players <= 8: 
            invalid_input = False
    except ValueError:
        print("This is not an integer. Please try again.")

game = Uno(num_players)