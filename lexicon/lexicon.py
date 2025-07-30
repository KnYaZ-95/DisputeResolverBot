lexicon_ru = {"main": {
    'start': lambda name: f'Привет, {name}! Я помогу тебе и твоему другу разрешить любой '
                          f'спор с помощью всеми известной игры "Камень, ножницы, бумага", '
                          f'либо с помощью броска кубика. Выбирай, что по душе 😉',
    'stop': 'Прекратить поиск',
    'remind': 'Напомнить 👊',
    'back_to_choice': 'Возвращаемся к выбору игры.',
    'player_is_found': 'Игрок найден! Помни, что играем до трех побед.',
    'player_is_not_found': 'Никого нет😟 Придется немного подождать. Я обязательно сообщу, '
                           'когда кто-нибудь присоединится.',
    'player_is_not_found_stop': "Устал ждать? Что ж, возвращаемся в лобби...",
    'you_win': 'Ура! Ты выиграл! Поздравляю 🥳',
    'win_td': 'В связи с отсутствием активности, второму игроку засчитано техническое поражение',
    'l_round': lambda res_1, res_2: f'К сожалению ты проиграл☹️ У тебя еще есть шанс отыграться!\n'
                                    f'<b>Счет {res_1}:{res_2}</b>\nЖми кнопку',
    'w_round': lambda res_1, res_2: f'Ты выиграл раунд, но не выиграл войну🤓\n'
                                    f'<b>Счет {res_1}:{res_2}</b>\nЖми кнопку',
    'you_lose': 'Увы, ты проиграл 😔. Ничего, выиграешь в следующий раз!',
    'lose_td': 'Долго тебя ждали. Засчитано техническое поражение',
    'ttl': lambda sec: f'Напомнить можно только раз в 30 секунд! Осталось {sec} сек.',
    'got_reminder': 'Другой игрок получил уведомление 👊',
    'chop-chop': "Другой игрок попросил тебя поторопиться!"
},
    'rsp': {
        'begin': 'Итак...Камень, ножницы, бумага! Отличный выбор. Если внезапно забыл, '
                 'как играть - жми "Помощь". Если не забыл, то ты молодец. '
                 'Можешь нажимать "Начать! 🤜🏻 🤛🏻". Но ведь тебе интересно, кто же эти '
                 '10 самых крутых игроков, правда? Если да, то жми "Статистика"',
        'help': 'Серьезно? Ладно, смотри: камень тупит ножницы, ножницы режут бумагу, '
                'бумага накрывает камень. Проше некуда 😉',
        'chosen': 'Выбор сделан!',
        'draw': 'Ваши силы равны!\n\nЖми кнопку',
        'choice_is_made': 'Псс..другой игрок уже сделал свой выбор. Поторапливайся 😉'
    },
    'dice': {
        'begin': 'Итак, твой выбор упал на кубики 🎲🎲 ',
        'help': 'У кого выпало больше, тот и выиграл. Все просто 😉',
        'result_wait': lambda result: f"Выпало {result}!\n\nТеперь подождем броска другого игрока...⏳",
        'result_check': lambda result: f"Выпало {result}!\n\n",
        'choice_is_made': 'Псс..другой игрок уже бросил кубик. Поторапливайся 😉',
        'draw_first': "И у нас тут ничья!\n\n Бросай еще раз",
        'draw_last': lambda result: f"Выпало {result}! И у нас тут ничья!\n\nБросай еще раз",
    }
}

lexicon_en = {"main": {
    'start': lambda name: f'Hello, {name}! I will help you and your friend resolve any '
                          f'dispute using the well-known game "Rock, Paper, Scissors" '
                          f'or by throwing a dice. Choose what you like 😉',
    'stop': 'Stop searching',
    'remind': 'Remind 👊',
    'back_to_choice': 'Returning to the beginning',
    'player_is_found': 'Player is found! Remember, we play until three wins',
    'player_is_not_found': "There's no one here😟 We'll have to wait a bit. I'll let you know "
                           "when someone joins",
    'player_is_not_found_stop': "Tired of waiting? Well, let's go back to the lobby...",
    'you_win': 'You win! Congratulations 🥳',
    'win_td': 'Due to lack of activity, the second player was awarded a technical defeat',
    'l_round': lambda res_1, res_2: f"Unfortunately, you lost ☹️ You still have a chance "
                                    f"to win back!\n<b>Score {res_1}:{res_2}</b>\nPress the button",
    'w_round': lambda res_1, res_2: f"You won the round, but you didn't win the war🤓\n"
                                    f"<b>Score {res_1}:{res_2}</b>\nPress the button",
    'you_lose': "You lost 😔. Never mind, you'll win next time!",
    'lose_td': "We've been waiting for you for a long time, so you've been awarded a technical defeat",
    'ttl': lambda sec: f'You can only remind once every 30 seconds! {sec} sec left',
    'got_reminder': 'Second player received a notification 👊',
    'chop-chop': "Second player asked you to hurry up!"
},
    "rsp": {
        'begin_rsp': "So... Rock, Paper, Scissors! A great choice. If you suddenly forgot "
                     "how to play - press 'Help'. If you haven't forgotten, then you're great. "
                     "You can press 'Start! 🤜🏻 🤛🏻'. But you are interested in who these 10 "
                     "badass players are, don't you? If so, press 'Statistics'",
        'help': 'Seriously? Okay, look: rock dulls scissors, scissors cut paper, paper '
                'covers rock. Simple 😉',
        'chosen': 'The choice is made!',
        'choice_is_made': 'Psst..the other player has already made his choice. Chop-chop 😉',
        'draw': 'Draw!!\n\nPress the button'
    },
    "dice": {
        'begin': 'So you chose dices 🎲🎲 ',
        'help': 'Whoever got more, wins. Simple. 😉',
        'result_wait': lambda result: f"The dice came up with {result} point(s)!\n\n"
                                      f"Now let's wait for the other player to throw...⏳",
        'result_check': lambda result: f"The dice came up with {result} point(s)!\n\n",
        'choice_is_made': 'Psst..the other player has already rolled the dice. Chop-chop 😉',
        'draw_first': "So we have a draw!\n\n Throw again",
        'draw_last': lambda result: f"The dice came up with {result} points! Draw!\n\nThrow again",
    }
}