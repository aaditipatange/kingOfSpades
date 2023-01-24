"""
This is a simple 4 Player game called King of Spades. 
On instantiating the game the deck is equally distributed among players i.e 13 cards each
Therefore there are 13 rounds.
For each round 1 card from each player's hand is shown.
The player with the highest value card (highest Rank then highest Suit; Ace has the highest Rank here) wins the round
The Player with most Round Winnings Becomes the King of Spades

"""

import random


class Card:
    # for the special feature Suits are represented by unicode symbols
    suit_list = ['\u2663', '\u2666', '\u2665', '\u2660']
    # Ace has the highest Rank. Therefore rank range is from 2 to 15
    rank_list = ['None', 'None', '2', '3', '4', '5', '6',
                 '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return (self.rank_list[self.rank] + self.suit_list[self.suit])

    def __eq__(self, other):
        return (self.rank == other.rank and self.suit == other.suit)

    # The Rank is checked first to find the highest Card, Suit is check incase rank is same
    def __gt__(self, other):
        if self.rank > other.rank:
            return True
        elif self.rank == other.rank:
            if self.suit > other.suit:
                return True
        return False


class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(2, 15):
                self.cards.append(Card(suit, rank))

    def __str__(self):
        s = ""
        for i in range(len(self.cards)):
            # Changes the Display to show cards of a player in single line
            s += str(self.cards[i]) + "  "
            #s += i*" " + str(self.cards[i]) + '\n'
        return s

    def shuffle(self):
        n_cards = len(self.cards)
        for i in range(n_cards):
            j = random.randrange(0, n_cards)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def pop_card(self):
        return self.cards.pop()

    def is_empty(self):
        return len(self.cards) == 0

    def deal(self, hands, n_cards=52):
        n_players = len(hands)
        for i in range(n_cards):
            if self.is_empty():
                break
            card = self.pop_card()
            current_player = i % n_players
            hands[current_player].add_card(card)


class Hand(Deck):
    def __init__(self, name=''):
        self.name = name
        self.cards = []
        # Counts the rounds won by player
        self.win = 0

    def add_card(self, card):
        self.cards.append(card)

    def __str__(self):
        s = "Hand of " + self.name
        if self.is_empty():
            return s + " is empty"
        s += " contains \n" + Deck.__str__(self)
        return s

    # Pop First card from Player's hand to Play the Round
    def pop_card(self):
        return self.cards.pop(0)

    # Function to keep the count of Rounds won by Player
    def game_win(self):
        self.win += 1

    # Function to retrieve the count of rounds won by Player
    def get_wins(self):
        return self.win


class CardGame():
    # The Game class to instantiate the players
    # We always have 4 players P1, P2, P3 and P4
    p1 = Hand('p1')
    p2 = Hand('p2')
    p3 = Hand('p3')
    p4 = Hand('p4')
    hands = [p1, p2, p3, p4]

    def __init__(self):
        # we use a Deck of 52 Cards, Shuffle the cards and
        # Deal the deck among the above defined Players
        self.deck = Deck()
        self.deck.shuffle()
        self.deck.deal(self.hands)

    # The funtion defined to play the actual game
    def round(self):
        print('Let the Game of K\u2660 begin')
        # Since we are always goning to have (maximum) 13 Rounds we define 1-14
        for i in range(1, 14):
            print('Round ' + str(i))
            # List defined to store cards of Round
            round_cards_list = []
            for hand in self.hands:
                # Poping 1 card from each players Hand (in order P1-P4)
                round_cards_list.append(hand.pop_card())
            # Printing the Cards of the Round
            for card in round_cards_list:
                print(card, end=" ")
            # Finding the winning cards of the Round using max (__gt__ method of Card class)
            round_card = max(round_cards_list)
            # Displaying the winning Card of the Round
            print('\nWinner Card of Round ' + str(i)+': ' + str(round_card))
            # To indentify the Player who won the round,
            # here we are finding the index of the winning card
            # from list of cards of that round
            # We then identify the Player by using this index to retrieve the element
            # from the hands list that stores the player objects
            round_winner = self.hands[round_cards_list.index(round_card)]
            # We add winning for the Player that won the Round
            round_winner.game_win()
            print('Winner of Round ' + str(i)+': ' +
                  round_winner.name.upper() + '!!')
            # Terminate the game anytime after 1st round (1st Round is played by default)
            end = input("Press E to exit OR any key to Continue...")
            if end.upper() == 'E':
                break
        # List defined to store the total winnings of each player
        winnings = []
        for hand in self.hands:
            # Retrieve the wins of each player and insert in the List
            winnings.append(hand.get_wins())
        # In order to identify the Game winner (player with maximum rounds win)
        # here we are finding the index of the highest wins
        # from list of winnings and adding 1 to adjust the index of player
        # Note: if the game is terminated with 2 players having equal rounds won then
        # Note: the index of the 1st player in order (P1-P4) with that winning is retrieved
        # Note: That player becomes the Game winner
        game_winner = winnings.index(max(winnings)) + 1
        print("Winner of K\u2660 is: P" +
              str(game_winner)+' Congratulationsss !!!')


game = CardGame()
print(game.p1)
print(game.p2)
print(game.p3)
print(game.p4)
game.round()
