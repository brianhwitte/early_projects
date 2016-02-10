

import random
import re

from time import sleep

test_nv = [('King', 10), ('Ace', 10), ('jack', 10), ('k', 10),('a',11), ('a', 11)]*5

DECK_INFO = {
    'blackjack': {
        'card names and values': zip([str(x) for x in range(2,11)],[y for y in range(2,11)]) + zip(['Jack','Queen','King','Ace'],[10, 10,10, 11]),
        'suits': ['Heart','Diamond','Club','Spade']
        },
    'test': {'card names and values': test_nv, 'suits':['Heart','Diamond','Club','Spade']}
}


DIALOG = {

    'choice': "What do you want to do?",
    
    'emptyhand': "There are no cards in your hand.",

    'menu': "h) hit\ns) stand\nd) see dealer cards\ny) see your own cards\n",

    'second card': "The dealer's second card is face down.",

    'your hand': "The cards in your hand are: ",

    'dealer has': "The dealer has: ",

    'end': "At the end of the round,",

    'welcome': "\nWelcome to Blackjack.\n",

    'shuffle': "It looks like your dealer is ready to go and has a freshly shuffled 6-deck shoe ready to go.\n",

    'face down': "The dealer places a card face down in front of himself.\n"
}


def dialog_printer(*args):

    for line in args: 
       
        try:
            print DIALOG[line]

        except KeyError:

            print line


def int_getter(question, answer_set):
    
    while True:

        val = int_only(question)

        try:
            assert val in answer_set
            
        except AssertionError:
            print "That wasn't one of the options."

        else:

            return val
            
            break


def int_only(question):
    '''Entry validation for raw_input'''

    while True:
        val = raw_input(question)

        try:
            val = int(val)

        except ValueError:
            print "That was not an integer."

        else:
            return int(val)

            break
            

def str_only(question):
    '''Entry validation for raw_input'''

    while True:
        val = raw_input(question)

        try:
            assert re.match("^[a-zA-Z]*$", val)

        except AssertionError:

            print "That wasn't just a string..."

        else:
            return val

            break
            

def str_from_list(question, answer_set):
    '''Entry validation for raw_input'''

    while True:
        val = str_only(question)

        try:
            assert val in answer_set

        except AssertionError:

            print "That wasn't one of the options."

        else:

            return val

            break
            

def str_not_from_list(question, conflict_set):
    '''Accepts only strings'''

    while True:

        value = str_only(question)

        try:

            assert value not in conflict_set

        except AssertionError:

            print "That choice is already taken. Please try again.\n"

        else:

            return value


class Card(object):

    def __init__(self, name = None, suit = None, value = None, special = None, symbol = None):
        self.name = name
        self.suit = suit
        self.value = value
        self.symbol = symbol


    def __repr__(self):

        return  "%s of %ss" % (self.name, self.suit)

    def __str__(self):

        return "%s of %ss" % (self.name, self.suit)


class Deck(object):

    def __init__(self, suits=None, name_value_tuples=None):
        
        self.contents = []
        self.suits = suits
        self.name_value_tuples = name_value_tuples


    def make_deck(self):

        self.contents = [Card(suit=x,value=y,name=z) for x in self.suits for (z,y) in self.name_value_tuples] * 6


    def shuffle_deck(self):
        
        random.shuffle(self.contents)


    def draw_card(self):
        
        return self.contents.pop()


class Hand(object):

    def __init__(self):

        self.value = 0
        self.contents = []
        self.natural = False
        self.bust = False
        

    def new_round(self):

        self.value = 0
        self.contents = []
        self.natural = False
        self.bust = False


    def add_card(self, new_card):

        self.new_card = new_card
        
        self.contents.append(self.new_card)


    def eval_hand(self):

        self.value = sum([card.value for card in self.contents])
        
        elevens = [card for card in self.contents if card.value == 11]
        
        if self.value > 21 and elevens:

            self.if_aces(elevens)

        self.set_bust()


    def set_bust(self):

        if self.value > 21: 

            self.bust = True
            
            print "Bust!"


    def print_the_hand(self):
        
        for card in self.contents: print card


    def if_aces(self, list_of_elevens):

        list_of_elevens[0].value = 1

        self.eval_hand()


class Player(object):

    def __init__(self, name=''):
        self.name = name
        self.hand = Hand()
        self.bet = 0
        self.money = 100


    def begin_round(self):

        self.bet = 0
        
        self.hand.new_round()


    def set_bet(self):

        self.bet = int_getter("{}, you have {} in your bank.  How much do you want to bet on this hand?\n> ".format(self.name, self.money), range(self.money+1))

        self.money -= self.bet

        print "{} places ${} on the table.\n".format(self.name, self.bet)


    def natural_payout(self, dealer_bj=None):
        # bets were deducted from money in bet()

        if dealer_bj and self.hand.natural:

            print "{} pushes with the dealer and gets to keep their money.".format(self.name)
            self.money += self.bet
            
        elif dealer_bj:

            print "{} loses their bet.".format(self.name)

        elif self.hand.natural:

            print "{} wins {}, 1.5 times their bet of {} (rounded to the nearest dollar).\n".format(self.name, self.bet * 1.5, self.bet)
            self.money += self.bet + int(round(self.bet * 1.5)) 
            
        else:

            print "{} waits patiently for the long game.\n".format(self.name)


    def take_card(self,card):
        #updates hand value with each card by calling eval_hand

        self.hand.contents.append(card)

        self.hand.eval_hand()


    def print_new_card(self, card):

        print "The dealer places a {} of {}s in front of {}.\n".format(card.name, card.suit, self.name)


    def handle_round(self, card):

        self.take_card(card)

        self.print_new_card(card)

        if len(self.hand.contents) == 2:

            self.check_naturals()
            

    def hit_me(self, card):
        
        self.print_new_card(card)
        
        self.take_card(card)


    def check_naturals(self):

        if self.hand.value == 21:

            self.hand.natural = True

            print self.name + " has a natural!\n"


class Dealer(Player):

    def __init__(self,name=''):
       
        self.name = name
        self.hand = Hand()
      

    def set_bet(self):
        pass


    def natural_payout(self, dealer_bj=None):
        pass


    def endgame_payout(self):
        pass


    def begin_round(self):
        # normal players have self.bet set to 0
        
        self.hand.new_round()


    def print_hand(self):

        if len(self.hand.contents) == 2:
            
            dialog_printer(self.hand.contents[0], 'second card')

        elif len(self.hand.contents) > 2:
            
            dialog_printer('dealer has')

            self.hand.print_the_hand()

            print "The value is: ", self.hand.value


    def print_new_card(self, card):

        if len(self.hand.contents) == 2:

            dialog_printer('face down')
        
        else:
            print "The dealer places a {} of {}s in front of himself.\n".format(card.name, card.suit)

        
class Blackjack(object):

    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.hand_over = False
        self.sitting_out = []


    def play(self):
        '''controls play of game, order of players, calls other functions'''
        
        dialog_printer('welcome','shuffle')

        self.add_players()
        self.add_dealer()

        for person in self.players[:-1]: person.money = 100

        ready = str_from_list("Are you ready to play a hand? (y/n)\n> ", ['n', 'y']).lower()
        
        self.new_deck()

        while ready != 'n':

            if len(self.deck.contents) < 6 * 52 * 0.7: 
                print "The shoe is more than 3/4 exhausted.  A new, shuffled shoe is brought out."

                self.new_deck()
                
            self.check_money()

            self.alter_players()

            self.play_round()

            ready = str_from_list("Are you ready to play a hand? (y/n)\n> ", ['n', 'y']).lower()
        
        self.end_game_status()
    

    def check_money(self):

        for person in self.players[:-1]: 

                if person.money <= 0: 

                    print "{0} is broke! There's a pawnshop in the lobby.\n {0} has left the game.\n".format(person.name)
                    
                    self.players.remove(person)


    def alter_players(self):

        changes = str_from_list("Do you want to make any changes to the players in the game? (y/n)\n> ", ['y','n'])
        
        menu2 = "a) add a player\nr) remove a player\ns) sit out a round\nc) come back from sitting out\n"

        while changes != 'n':

            choice = str_from_list(menu2, ['a','r','s','c'])

            if choice == 'a': self.add_one_player()
                
            elif choice == 'r': self.remove_player('r')

            elif choice == 's': self.remove_player('s')

            elif choice == 'c': self.re_enter_game()

            changes = str_from_list("Do you want to make any more changes to the players in the game? (y/n)\n> ", ['y','n'])

        self.player_num()


    def re_enter_game(self):

        if not(len(self.sitting_out)):

            print "There's no one currently siting out.  You can add a new player, though.\n"

        else:

            print "Currently sitting out: \n"

            for person in self.sitting_out: print person.name

            mover_name = str_from_list("Which player wants to get back in to the game?\n(enter 'oops' to go back to the main menu.\n> ",[person.name for person in self.sitting_out] + ['oops'])
            
            if mover_name == 'oops':
                
                pass

            else:

                mover = next(person for person in self.sitting_out if person.name == mover_name)

                self.players = self.players[:-1] + [mover] + [self.players[-1]]
                
                self.sitting_out.remove(mover)

            


    def add_one_player(self):

        inadmissable_names = [person.name for person in self.players + self.sitting_out]

        new_name = str_not_from_list("What is the name of the new player?\n> ", inadmissable_names)
        
        self.players = self.players[:-1] + [Player(new_name)] + [self.players[-1]]
        
        print "{} has joined the game.".format(self.players[-2].name)


    def player_num(self):

        if len(self.players) == 1:

            print "There are no players left in the game!  If you don't add at least one player, the game will be over.\n"

            second_chance = str_from_list("Do you want to add a player, or exit the game? ('add'/'exit')\n> ", ['add', 'exit'])

            if second_chance == 'add': 

                self.alter_players()
            
            else: 

                print "I guess we're done here."

                self.end_game_status()

                
    def remove_player(self, flag):

        print "The current players are: "

        in_game = [person.name for person in self.players[:-1]]
        
        for name in in_game: print name

        kick_out = str_from_list("Which person is leaving the game?\n> ", in_game)
        
        mover = next(person for person in self.players[:-1] if person.name == kick_out)
        
        if flag == 'r':
            
            print "{} has left the game".format(mover.name)
            
            self.players.remove(mover)
        
        elif flag == 's':
            
            print "{} goes to the bar for a drink.".format(mover.name)
            
            self.sitting_out.append(mover)
            
            self.players.remove(mover)


    def end_game_status(self):

        if len(self.players) > 1:
            
            for person in self.players[:-1]:

                print "{} ended the game with ${}.".format(person.name, person.money)

        raise SystemExit()


    def add_players(self):

        for player in range(int_only("How many players, in addition to the dealer?\n> ")):
        
            self.players.append(Player(str_only("What is the name of player #{}?\n> ".format(str(player+1)))))


    def new_deck(self):
        
        self.deck = Deck(DECK_INFO['blackjack']['suits'], DECK_INFO['blackjack']['card names and values'])

        self.deck.make_deck()
        
        self.deck.shuffle_deck()
        

    def add_dealer(self):

        dealer = Dealer(name='Dealer')

        self.players.append(dealer)


    def play_round(self):
        #self.hand_over is set to True when dealer has natural 21, busts or stands
        
        self.hand_over = False
        
        for person in self.players: 
            person.begin_round()
            person.set_bet()

        self.deal_round()
        self.deal_round()

        blackjacks = [person for person in self.players if person.hand.natural]

        if blackjacks:
            self.handle_naturals(blackjacks)

        if not(self.hand_over):
        
            self.after_two_cards()
            
            self.evaluate_hands()    


    def handle_naturals(self, list_of_blackjacks):
        
        dealer_natural = [person for person in list_of_blackjacks if isinstance(person, Dealer)]
        
        self.hand_over = dealer_natural

        if dealer_natural:
            
            print "The dealer has blackjack! The round is over."
            
            self.hand_over = True

        elif len(list_of_blackjacks) == len(self.players) - 1:

            print "The round is over, with the dealer holding the losing hand."
            
            self.hand_over = True
        
        for person in self.players: person.natural_payout(dealer_bj=bool(dealer_natural))


    def after_two_cards(self):

        for person in [player for player in self.players[:-1] if not player.hand.natural]: 
            
            self.hit_or_not(person)

        self.dealer_hit_or_not()


    def dealer_hit_or_not(self):

        d = self.players[-1]

        if len(d.hand.contents) == 2:
            
            print "The dealer's first card is a %s.\n" % d.hand.contents[0]
            print "He turns over his second card to show a %s.\n" % d.hand.contents[1]

        while d.hand.value <= 16:

            d.hit_me(self.deck.draw_card())

            dialog_printer('dealer has')

            d.hand.print_the_hand()

            print "The value is: ",d.hand.value,"\n"

            sleep(2)


    def hit_or_not(self, person):

        while not(person.hand.bust):
            
            person.hand.print_the_hand

            print "{}, it's your turn.\n\nYou have: ".format(person.name)

            person.hand.print_the_hand()

            dialog_printer("\nYour options are:\n", 'menu')
            
            choice = str_from_list("What do you want to do?\n> ",['s','h','d','y']).lower()
            
            if choice == 's':
                
                print "%s stands.\n" % person.name

                break

            elif choice == 'h':
                
                person.hit_me(self.deck.draw_card())

            elif choice == 'd':

                dialog_printer('','dealer has')

                self.players[-1].print_hand()

            elif choice == 'y':

                dialog_printer('', "{}'s hand is: ".format(self.name))
                
                person.hand.print_the_hand()
                
                print "The hand value is: %s.\n" % person.hand.value


    def evaluate_hands(self):

        dealer_hand = self.players[-1].hand
        
        for person in self.players[:-1]:

            if person.hand.bust: 

                print "{} went bust when drawing a {} of {}s.".format(person.name, person.hand.contents[-1].name, person.hand.contents[-1].suit )

                result = 'lost'

            elif dealer_hand.bust: 

                result = 'won'
                person.money += person.bet * 2

            elif person.hand.value > dealer_hand.value:

                result = 'won'
                person.money += person.bet * 2

            elif person.hand.value < dealer_hand.value: 

                result = 'lost'

            else:

                result = 'kept'
                person.money += person.bet
      
            self.end_round_status(person)

            print "{} {} ${}!".format(person.name, result, person.bet)

            anything = raw_input("Hit 'return' when ready to continue.")


    def end_round_status(self, person):

        dealer_hand = self.players[-1].hand

        print ''

        dialog_printer("The cards in {}'s hand are: ".format(person.name))
        person.hand.print_the_hand()
        print "The value is: ", person.hand.value

        print ''

        dialog_printer("dealer has")
        dealer_hand.print_the_hand()
        print "The value is: ", dealer_hand.value
        
        print ''


    def deal_round(self):

        for person in self.players:

            person.handle_round(self.deck.draw_card())
            
            sleep(1)


b = Blackjack()
b.play()

      
