def game_logic(game_type: str, player_1: int, choice_1: str | int, player_2: int, choice_2: str | int) -> set | tuple:
    if game_type == 'rsp':
        win_combinations = {'rock': 'scissors',
                            'scissors': 'paper',
                            'paper': 'rock'}
        if win_combinations[choice_1] == choice_2:
            return player_1, player_2
        elif win_combinations[choice_2] == choice_1:
            return player_2, player_1
        else:
            return {player_1, player_2}
    else:
        if choice_1 > choice_2:
            return player_1, player_2
        elif choice_2 > choice_1:
            return player_2, player_1
        else:
            return {player_1, player_2}

