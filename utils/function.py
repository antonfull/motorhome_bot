def list_gamer(players):
    gamers = []
    if (players):
        for player in players:
            players = player[4]
            gamers.append(players)
        gamers = '\n'.join(gamers)
    else:
        gamers = 'На данный тур никто не записался'
    return gamers