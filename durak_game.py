#!/usr/bin/env python
import random


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f'{self.rank} of {self.suit}'

    def is_higher(self, card):
        # return true if the card passed as a parameter is higher than self
        ranks = {'6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
        if self.suit == card.suit and ranks[card.rank] > ranks[self.rank]:
            return True
        return False


class Deck:
    deck = []
    discard_pile = []

    def __init__(self):
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        ranks = ['6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for rank in ranks:
            for suit in suits:
                card = Card(rank, suit)
                self.deck.append(card)

    def display(self):
        for card in self.deck:
            print(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def trump(self):
        return self.deck[-1]

    def is_exhausted(self):
        if len(self.deck) == 0:
            return True
        return False

    def draw_card(self):
        if not self.is_exhausted():
            return self.deck.pop(0)
        print("The deck is exhausted.")
        return None

    def left(self):
        return len(self.deck)


class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.hand = []

    def draw_card(self, deck):
        card = deck.draw_card()
        if card:
            self.hand.append(card)

    def refill(self, deck):
        while len(self.hand) < 6 and not deck.is_exhausted():
            self.draw_card(deck)

    def give_up(self, played_cards):
        for card in played_cards:
            self.hand.append(card)

    def play_card(self, message=''):
        for i, card in enumerate(self.hand, 1):
            print(i, card)
        print("To exit the game type Q.")
        card = None
        while not card:
            try:
                choice = input(message)
                if choice.isdigit():
                    card = self.hand[int(choice) - 1]
                    self.hand.remove(card)
                elif choice.lower() == 's':
                    break
                elif choice.lower() == 'q':
                    quit()
                else:
                    print('Invalid input. Try again.')
            except IndexError:
                print(f'There are only {len(self.hand)} cards. Try again.')
        return card

    def attack(self):
        attack_card = None
        while not attack_card:
            attack_card = self.play_card('Choose a card to attack: ')
            if attack_card is None:
                print("It's your turn. You must choose a card.")
        return attack_card

    def add_attack(self, played_cards):
        ranks = [card.rank for card in played_cards]
        self.display()
        for card in self.hand:
            if card.rank in ranks:
                choice = input(
                    f"Would you like to start a new attack with the card {card}? (y/n) ")
                if choice.lower() == 'y':
                    self.hand.remove(card)
                    return card
                else:  # any other input besides 'y' is handled as 'n' intentionally
                    return None
        print('There are no cards suitable for a new attack.')
        return None

    def defend(self, attack_card, trump_suit):
        def_card = self.play_card(
            'Choose a card to defend or type S to give up: ')
        if not def_card:
            return None
        while def_card is not None and not attack_card.is_higher(def_card):
            if attack_card.suit != trump_suit and def_card.suit == trump_suit:
                return def_card
            print("You can't defend with this card, choose another one or give up.")
            self.hand.append(def_card)
            def_card = self.play_card(
                'Choose a card to defend or type S to give up: ')
        return def_card

    def display(self):
        print("Your cards:")
        for card in self.hand:
            print(card)

    def get_min_trump(self, trump_suit):
        trumps = []
        for card in self.hand:
            if card.suit == trump_suit:
                trumps.append(card)
        if not trumps:
            return None
        min_trump = trumps[0]
        for card in trumps:
            if card.is_higher(min_trump):
                min_trump = card
        return min_trump


class Opponent(Player):
    # the second player emulated by computer
    def attack(self):
        card = random.choice(self.hand)  # TODO: Some logic here?
        self.hand.remove(card)
        return card

    def defend(self, attack_card, trump_suit):
        defend_cards = []
        trumps = []
        for card in self.hand:
            if attack_card.is_higher(card):
                defend_cards.append(card)
        if defend_cards:
            self.hand.remove(defend_cards[0])
            return defend_cards[0]  # TODO: sort them by rank
        if not defend_cards and attack_card.suit == trump_suit:
            return None
        for card in self.hand:
            if card.suit == trump_suit:
                trumps.append(card)  # TODO sort by ranks
        if trumps:
            self.hand.remove(trumps[0])
            return trumps[0]
        return None

    def add_attack(self, played_cards):
        ranks = [card.rank for card in played_cards]
        add_cards = []
        add_card = None
        for card in self.hand:
            if card.rank in ranks:
                add_cards.append(card)
        if add_cards:
            add_card = random.choice(add_cards)
            self.hand.remove(add_card)
        return add_card


def game_round(attacker, defender, trump_suit):
    print(f"\n---------New round!---------\n{attacker.name}'s turn.")
    print(f"Reminder: trump suit is {trump_suit}")
    played_cards = []
    # the number of attacks can't be greater than the number of defender's cards or greater than 6 by the rules
    max_attacks = min(len(defender.hand), 6)
    ctr = 0  # current number of attacks
    attack_card = attacker.attack()
    is_attack_successful = False
    while attack_card and ctr < max_attacks:  # the second condition is not necessary
        if played_cards:
            print(f"\nAt the end of the attack #{ctr}, the cards on the table: " +
                  ", ".join([card.__str__() for card in played_cards]))
        played_cards.append(attack_card)
        ctr += 1
        print(f"\nAttack # {ctr}")
        print(f'{attacker.name} is attacking with the card {attack_card}')
        def_card = defender.defend(attack_card, trump_suit)
        if def_card:
            print(f"{defender.name} is defending with {def_card}")
            played_cards.append(def_card)
            if ctr < max_attacks:
                attack_card = attacker.add_attack(played_cards)
        else:
            print(
                f'{defender.name} has given up, picked up all the played cards and skipped their turn.')
            print("The played cards in this round were:", ", ".join(
                [card.__str__() for card in played_cards]))
            defender.give_up(played_cards)
            played_cards = []
            attack_card = None
            is_attack_successful = True
    print("\n------The round is over------")
    return is_attack_successful, played_cards


def game():
    name = input("Enter your name: ")
    deck = Deck()
    deck.shuffle()
    trump_suit = deck.trump().suit
    print('Trump suit is', trump_suit)
    player = Player(name)
    comp = Opponent('The Computer')
    for i in range(6):
        player.draw_card(deck)
        comp.draw_card(deck)
    attacker = player
    defender = comp
    player.display()
    comp_min_trump = comp.get_min_trump(trump_suit)
    player_min_trump = player.get_min_trump(trump_suit)
    print("\nMin trump card of your opponent is:",
          comp_min_trump if comp_min_trump else "no")
    print('Your min trump is:', player_min_trump if player_min_trump else "no")
    if (not player_min_trump and comp_min_trump) or (comp_min_trump and player_min_trump and comp_min_trump.is_higher(player_min_trump)):
        print('Your opponent attacks first.')
        attacker = comp
        defender = player
    else:
        print("Your turn first!")
    while player.hand and comp.hand:
        print("Cards left in the deck: ", deck.left())
        print("In the discard pile:", len(deck.discard_pile))
        print(f'{comp.name} has {len(comp.hand)} cards')
        attack_status, played_cards = game_round(
            attacker, defender, trump_suit)
        deck.discard_pile.extend(played_cards)
        attacker.refill(deck)
        defender.refill(deck)
        if attack_status == False:
            temp = attacker
            attacker = defender
            defender = temp

    print("The game is over.")
    print("Cards left in the deck: ", deck.left())
    print("In the discard pile:", len(deck.discard_pile))
    print(f'The {comp.name} has {len(comp.hand)} cards')
    print(f"{player.name} has {len(player.hand)} cards")
    if not player.hand and not comp.hand:
        print("Nobody has lost.")
    elif player.hand and not comp.hand:
        print(f'{player.name} has lost.')
    else:
        print(f'{comp.name} has lost.')


if __name__ == "__main__":
    game()
