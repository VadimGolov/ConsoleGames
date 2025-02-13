from random import shuffle


class Card:

    def __init__(self, rank, suit, score) -> None:
        self.__rank: str = rank
        self.__suit: str = suit
        self.__score: int = score

    def __str__(self) -> str:
        return '|{:^15}|{:^8}|{:^18}|'.format(self.__rank, self.__suit, self.__score)


class CardShoe:
    __suits: list[str] = ['Пик', 'Бубнов', 'Треф', 'Червей']
    __ranks: list[str] = [str(item) for item in range(2, 11)] + ['Валет', 'Дама', 'Король', 'Туз']
    __scores: list[int] = [value for value in range(2, 11)] + [10, 10, 10, 11]

    def __init__(self, deck_count: int = 6) -> None:
        self.__cards: list[Card] = []
        for _ in range(deck_count):
            self.__cards += [Card(rank, suit, self.__scores[index]) for suit in self.__suits for index, rank in
                             enumerate(self.__ranks)]
        self.shuffle()

    # Перемешиваем карты
    def shuffle(self) -> None:
        shuffle(self.__cards)

    def __len__(self) -> int:
        return len(self.__cards)

    def __getitem__(self, position) -> Card:
        return self.__cards[position]

    def get_card(self) -> Card:
        if len(self.__cards) == 0:
            raise ValueError("Нет доступных карт в колоде")
        current_card: Card = self.__cards.pop()
        return current_card


class Player:

    def __init__(self, name: str, card_shoe: CardShoe) -> None:
        self.__name: str = name
        self.__shoe: CardShoe = card_shoe
        self.__hand: list[Card] = [self.__shoe.get_card(), self.__shoe.get_card()]

    def take_card(self) -> None:
        new_card: Card = self.__shoe.get_card()
        self.__hand.append(new_card)

    def __ace_index(self) -> int:
        index: int = len(self.__hand)

        for item in reversed(self.__hand):
            index -= 1
            split_item: list[str] = str(item).split('|')
            if 'Туз' in split_item[1]:
                return index
        else:
            return -1

    def __get_score(self) -> int:
        amount: int = 0

        for item in self.__hand:
            split_item = str(item).split('|')
            amount += int(split_item[3])

        return amount

    def ace_downgrade(self) -> None:
        limit_score: int = self.__get_score()
        work_index: int = self.__ace_index()

        if work_index == -1:
            return
        else:
            if limit_score > 21:
                item: Card = self.__hand[work_index]
                split_item: list[str] = str(item).split('|')
                suite: str = split_item[2].strip()

                self.__hand[work_index] = Card('Туз', suite, 1)

    def get_name(self) -> str:
        return self.__name

    def get_info(self) -> tuple[str, int]:
        hand_cards: str = ''
        hand_score: int = 0

        for item in self.__hand:
            split_item: list[str] = str(item).split('|')
            hand_cards += str(item) + '\n'
            hand_score += int(split_item[3])

        return hand_cards, hand_score

    def is_blackjack(self) -> bool:
        hand_cards: int = len(self.__hand)
        hand_score: int = self.__get_score()

        if hand_cards == 2 and hand_score == 21:
            return True
        else:
            return False


# Таблица карт
def print_scores(get_name, get_cards, get_score):
    print('\n+{:->43}+'.format('-'))
    print('|{:^43}|'.format(get_name))
    print('+{:->15}+{:->8}+{:->18}+'.format('-', '-', '-'))
    print('|{:^15}|{:^8}|{:^18}|'.format('Достоинство', 'Масть', 'Количество очков'))
    print('+{:->15}+{:->8}+{:->18}+'.format('-', '-', '-'))
    print(get_cards[:-1])
    print('+{:->15}+{:->8}+{:->18}+'.format('-', '-', '-'))
    print('| {: <11} : {: <28}|'.format('Сумма очков', get_score))
    print('+{:->43}+'.format('-'))
    print()


# Запуск игры
def start_game(some_names: list[str]) -> None:
    # Играем в 6 колод
    formed_shoe: CardShoe = CardShoe()

    player_name = some_names[0]
    dealer_name = some_names[1]

    player: Player = Player(player_name, formed_shoe)
    dealer: Player = Player(dealer_name, formed_shoe)

    player.ace_downgrade()

    player_cards, player_score = player.get_info()
    dealer_cards, dealer_score = dealer.get_info()

    print_scores(player.get_name(), player_cards, player_score)

    while True:
        ask: str = input('Вы хотите взять ещё одну карту? (да/нет): ').lower()

        if ask == 'да' or ask == 'yes':
            player.take_card()
            player.ace_downgrade()

            player_cards, player_score = player.get_info()
            print_scores(player.get_name(), player_cards, player_score)
        else:
            break

    while True:
        if dealer_score <= 16:
            dealer.take_card()
            dealer.ace_downgrade()
            dealer_cards, dealer_score = dealer.get_info()
        if dealer_score >= 17:
            break

    print_scores(player.get_name(), player_cards, player_score)
    print_scores(dealer.get_name(), dealer_cards, dealer_score)

    if player.is_blackjack() and dealer.is_blackjack():
        print(f'Ничья, но {player.get_name()} забрал выигрыш до того как Крупье открыл вторую карту | Выигрыш 1 к 1')
    elif player.is_blackjack() and not dealer.is_blackjack():
        print(f'{player.get_name()} выиграл | Выигрыш 3 к 2')
    elif not player.is_blackjack() and dealer.is_blackjack():
        print(f'{player.get_name()} проиграл')

    elif 21 >= player_score > dealer_score:
        print(f'{player.get_name()} выиграл | Выигрыш 1 к 1')
    elif player_score <= 21 < dealer_score:
        print(f'{player.get_name()} выиграл | Выигрыш 1 к 1')

    elif 21 >= dealer_score > player_score:
        print(f'{player.get_name()} проиграл')
    elif dealer_score <= 21 < player_score:
        print(f'{player.get_name()} проиграл')

    elif player_score == dealer_score:
        print('Ничья - менее 21 у обоих ')
    elif player_score > 21 and dealer_score > 21:
        print('Ничья - перебор у обоих')


if __name__ == '__main__':
    while True:
        user_name: str = input('Введите свое имя: ')
        croupier_name: str = input('Если хотите вы можете ввести имя крупье: ')

        if user_name:
            break

    if croupier_name:
        players: list[str] = [user_name, croupier_name]
    else:
        players: list[str] = [user_name, 'Дилер']

    print('\n', ' {:^43} '.format('Сегодня играм на 6 колодах'))

    while True:
        start_game(players)
        game_ask: str = input('Хотите сыграть еще раз? (да/нет): ').lower()

        if game_ask == 'нет' or game_ask == 'no':
            break

    input('\nДля закрытия окна программы нажмите Enter')