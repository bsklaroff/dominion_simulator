import card_classes

turn_count = 0
logging = False

def estate_after_chapel(player_info):
  sum = count_card(player_info, 'Estate')
  for card_name in player_info.hand:
    if card_name == 'Estate':
      sum -= 1
  return sum

def money_after_chapel(player_info):
  sum = count_money(player_info)
  for card_name in player_info.hand:
    if card_name == 'Copper':
      sum -= 1
  sum += 2 * count_card(player_info, 'Festival')
  return sum

def count_card(player_info, card):
  count = 0
  for card_name in player_info.deck + player_info.hand + player_info.discard:
    if card_name == card:
      count += 1
  for action in player_info.actions_played:
    if card_classes.name_to_inst_dict[card] == action:
      count += 1
  return count

def copper_in_hand(hand):
  for card_name in hand:
    if card_name == 'Copper':
      return True
  return False

def money_without_coppers(player_info):
  sum = 0
  for card_name in player_info.deck + player_info.hand + player_info.discard:
    if card_name == 'Silver':
      sum += 2
    elif card_name == 'Gold':
      sum += 3
  return sum

def num_useless(hand):
  count = 0
  for card_name in hand:
    if card_name == 'Copper' or card_name == 'Estate':
      count += 1
  return count

def count_money(player_info):
  sum = 0
  for card_name in player_info.deck + player_info.hand + player_info.discard:
    if card_name == 'Copper':
      sum += 1
    elif card_name == 'Silver':
      sum += 2
    elif card_name == 'Gold':
      sum += 3
  return sum

def choose_buy(player_info):
  available_cards = {}
  for card_name, num_left in player_info.bank.iteritems():
    card = card_classes.name_to_inst_dict[card_name]
    if num_left > 0 and card.cost <= player_info.treasure:
      available_cards[card_name] = card.cost
  if money_without_coppers(player_info) > 7 and 'Province' in available_cards:
    return 'Province'
  if player_info.bank['Province'] <= 2 and 'Duchy' in available_cards:
    return 'Duchy'
  if count_card(player_info, 'Gold') < 3:
    if 'Gold' in available_cards:
      return 'Gold'
    if count_card(player_info, 'Festival') == 0 and 'Festival' in available_cards:
      return 'Festival'
  if 'Silver' in available_cards and money_without_coppers(player_info) == 0:
    return 'Silver'
  if 'Laboratory' in available_cards and count_card(player_info, 'Laboratory') == 0:
    return 'Laboratory'
  if 'Smithy' in available_cards and count_card(player_info, 'Smithy') == 0:
    return 'Smithy'
  if 'Silver' in available_cards and money_without_coppers(player_info) < 6:
    return 'Silver'
  if 'Laboratory' in available_cards:
    return 'Laboratory'
  if 'Smithy' in available_cards:
    return 'Smithy'
  if 'Silver' in available_cards and count_card(player_info, 'Gold') < 3:
    return 'Silver'
  if player_info.bank['Province'] <= 1 and 'Estate' in available_cards and count_card(player_info, 'Estate') == 0:
    return 'Estate'
  return 'None'

def action_choice(player_info):
  global turn_count
  c = 'None'
  if card_classes.name_to_inst_dict['Festival'] in player_info.actions_available:
    c = 'Festival'
  elif card_classes.name_to_inst_dict['Laboratory'] in player_info.actions_available:
    c = 'Laboratory'
  elif card_classes.name_to_inst_dict['Chapel'] in player_info.actions_available and num_useless(player_info.hand) >= 3 and money_after_chapel(player_info) >= 3:
    c = 'Chapel'
  elif card_classes.name_to_inst_dict['Smithy'] in player_info.actions_available:
    c = 'Smithy'
  elif card_classes.name_to_inst_dict['Chapel'] in player_info.actions_available and num_useless(player_info.hand) > 0 and money_after_chapel(player_info) >= 3:
    c = 'Chapel'
  if logging:
    print player_info
    print 'Turn', turn_count
    print 'Going to play', c
    x = raw_input('continue')
  return c

def buy_choice(player_info):
  global turn_count
  buy = None
  if len(player_info.hand) == 5 and len(player_info.deck) == 5 and player_info.bank['Chapel'] == 10:
    turn_count = 0
  if turn_count == 0 or turn_count == 1:
    if player_info.treasure == 5:
      buy = 'Festival'
    elif player_info.treasure == 4:
      buy = 'Smithy'
    elif player_info.treasure in [2, 3]:
      buy = 'Chapel'
  if player_info.buys == 1:
    turn_count += 1
  if buy:
    return buy
  a = choose_buy(player_info)
  if logging:
    print player_info
    print 'Turn', turn_count
    print 'Going to buy', a
    x = raw_input('continue')
  return a

def execute_action_strategy(player_info, action):
  if action.name == 'Chapel':
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
