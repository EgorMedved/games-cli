import random
from games import Deck
from dataclasses import dataclass
from dataclasses import field
# туз считать как 11 или 1
@dataclass
class BlackJackDeck(Deck):
    deck = Deck.deck
    random.shuffle(deck)


class Dealer:
    hand = []

    def get_points(self):
        return sum([card.game_value for card in Dealer.hand])

    def take_card(self):
        Dealer.hand.append(BlackJackDeck.deck.pop(0))

    def hit_me_card(self):
        while Dealer.get_points(self) < 17:
            Dealer.take_card(self)
            if Dealer.get_points(self) > 21:
                for ace in Dealer.hand:
                    if ace.game_value == 11:
                        ace.game_value = 1
                        if Dealer.get_points(self) == 21:
                            BlackJack.check_blackjack(self)
                            return True
                else:
                    Player.cash += Player.bet * 2
                    BlackJack.print_final(self)
                    print('У крупье перебор. Вы выиграли.')
                    return True
            elif Dealer.get_points(self) == 21:
                BlackJack.check_blackjack(self)
                return True


class Player:
    bet: int
    cash = 100
    hand = []

    def get_points(self):
        return sum([card.game_value for card in Player.hand])

    def take_card(self):
        Player.hand.append(BlackJackDeck.deck.pop(0))

    def make_bet(self):
        while True:
            try:
                bet = int(input(f'У вас {Player.cash} монет. Введите размер ставки:\n'))
            except:
                print('Неверное значение\n')
                continue
            else:
                if bet > Player.cash:
                    print('Ставка больше вашего банка. Попробуйте снова\n')
                    continue
                elif bet <= 0:
                    print('Такая ставка не может быть принята. Попробуйте снова\n')
                    continue
                else:
                    Player.cash -= bet
                    Player.bet = bet
                    return print('Ставка принята. Раздача...')

    def hit_me_card(self):
        hit_me = input('Введите "y" для добора, другое - пасс.\n')
        while hit_me == 'y':
            Player.take_card(self)
            if Player.get_points(self) > 21:
                for ace in Player.hand:
                    if ace.game_value == 11 and Player.get_points(self) > 21:
                        ace.game_value = 1
                        if Player.get_points(self) == 21:
                            BlackJack.check_blackjack(self)
                            return True
                        else:
                            BlackJack.print_field(self)
                            hit_me = input('Введите "y" для добора, другое - пасс.\n')
                            continue
                else:
                    BlackJack.print_final(self)
                    print('Перебор. Победа крупье.')
                    return True
            elif Player.get_points(self) == 21:
                BlackJack.check_blackjack(self)
                return True
            else:
                BlackJack.print_field(self)
                hit_me = input('Введите "y" для добора, другое - пасс.\n')


class BlackJack:

    def give_start_cards(self):
        for i in range(2):
            Player.take_card(self)
            Dealer.take_card(self)

    def print_field(self):
        print('Ваша рука: \n')
        for card in Player.hand:
            print(f'{card.human_value}, {card.suit}\n')
        print(f'Ваши очки: {Player.get_points(self)}\n')
        print('Рука крупье: \n')
        print(f'{Dealer.hand[0].human_value} {Dealer.hand[0].suit}\n')

    def print_final(self):
        print('Ваша рука: \n')
        for card in Player.hand:
            print(f'{card.human_value}, {card.suit}\n')
        print(f'Ваши очки: {Player.get_points(self)}\n')
        print('Рука крупье: \n')
        for card in Dealer.hand:
            print(f'{card.human_value}, {card.suit}\n')
        print(f'Очки крупье: {Dealer.get_points(self)}\n')

    def check_blackjack(self):
        if Player.get_points(self) == 21 and Dealer.get_points(self) < 17:
            Dealer.hit_me_card(self)
            if Dealer.get_points(self) <= 21:
                if Player.get_points(self) == Dealer.get_points(self) == 21:
                    Player.cash += Player.bet
                    BlackJack.print_final(self)
                    print('Ничья')
                    return True
                elif Player.get_points(self) == 21:
                    Player.cash += Player.bet * 2
                    BlackJack.print_final(self)
                    print('Blackjack! Вы выиграли!')
                    return True
                elif Dealer.get_points(self) == 21:
                    BlackJack.print_final(self)
                    print('У крупье Blackjack. Победа крупье.')
                    return True

    def check_winner(self):
        if Player.get_points(self) > Dealer.get_points(self):
            Player.cash += Player.bet * 2
            BlackJack.print_final(self)
            return print('Вы выиграли.')
        elif Dealer.get_points(self) > Player.get_points(self):
            BlackJack.print_final(self)
            return print('Крупье выиграл.')
        else:
            Player.cash += Player.bet
            BlackJack.print_final(self)
            return print('Ничья.')

    def check_cash(self):
        if Player.cash > 0:
            return print(f'Ваш банк: {Player.cash}')
        else:
            return print('Вы всё проиграли...')

    def resume_game(self):
        BlackJack.check_cash(self)
        Player.hand = []
        Dealer.hand = []
        global start
        start = input('Для старта нажмите y, другое - стоп.\n')


blackjackdeck = BlackJackDeck()
player = Player()
dealer = Dealer()
blackjack = BlackJack()

start = input('Для старта нажмите y, другое - стоп.\n')
while start == 'y':
    player.make_bet()
    blackjack.give_start_cards()
    blackjack.print_field()

    if blackjack.check_blackjack():

        blackjack.resume_game()
        continue

    if player.hit_me_card():
        blackjack.resume_game()
        continue

    if dealer.hit_me_card():
        blackjack.resume_game()
        continue

    blackjack.check_winner()
    blackjack.resume_game()
