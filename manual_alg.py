import card_classes

def choose_card_lte(player_info, cost):
  available_cards = {}
  for card_name, num_left in player_info.bank.iteritems():
    card = card_classes.name_to_inst_dict[card_name]
    if num_left > 0 and card.cost <= cost:
      available_cards[card_name] = card.cost
  print 'Available Cards:'
  for card_name, cost in available_cards.iteritems():
    print card_name, cost
  return raw_input('Choose a card to gain: ')

def action_choice(player_info):
  print '### Action choice ###'
  print player_info
  available_cards = []
  return raw_input('Choose an action to play: ')

def buy_choice(player_info):
  print '### Buy Choice ###'
  print player_info
  return choose_card_lte(player_info, player_info.treasure)

def execute_action_strategy(player_info, action):
  if action.name == 'Remodel':
    trashable_cards = player_info.hand[:]
    trashable_cards.remove('Remodel')
    remodel_options = {}
    for trashable in trashable_cards:
      trashed_cost = card_classes.name_to_inst_dict[trashable].cost
      for gainable, num_left in player_info.bank.iteritems():
        card = card_classes.name_to_inst_dict[gainable]
        if num_left > 0 and trashed_cost + 2 >= card.cost:
          if trashable not in remodel_options:
            remodel_options[trashable] = []
          remodel_options[trashable].append(gainable)
    print 'Remodel Options:'
    for card_name, gainable_list in remodel_options.iteritems():
      print card_name, gainable_list
    card_to_trash = raw_input('Choose a card to trash: ')
    card_to_gain = choose_card_lte(player_info, card_classes.name_to_inst_dict[card_to_trash].cost + 2)
    return [card_to_trash, card_to_gain]
  elif action.name == 'Workshop':
    return choose_card_lte(player_info, 4)
  elif action.name == 'Workshop':
    return choose_card_lte(player_info, 5)
  elif action.name == 'Chapel':
    cards_to_trash = []
    for card_name in player_info.hand:
      if card_name == 'Estate':
        cards_to_trash.append(card_name)
      if len(cards_to_trash) == 4:
        return cards_to_trash
    for card_name in player_info.hand:
      if card_name == 'Copper':
        cards_to_trash.append(card_name)
      if len(cards_to_trash) == 4:
        return cards_to_trash
    return cards_to_trash
