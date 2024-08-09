def rsp_logic(player_1: int, choice_1: str, player_2: int, choice_2: str) -> set | tuple:
    win_combinations = {'rock': 'scissors',
                        'scissors': 'paper',
                        'paper': 'rock'}
    if win_combinations[choice_1] == choice_2:
        return player_1, player_2
    if win_combinations[choice_2] == choice_1:
        return player_2, player_1
    return {player_1, player_2}
