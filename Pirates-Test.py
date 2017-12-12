"""
This is an example for a bot.
"""
from pirates import *
import math
 
   
def bunk_push(pirate, game):
    # Go over all enemies.
    for enemy in game.get_enemy_living_pirates():
        # Check if the pirate can push the enemy.
        if pirate.can_push(enemy) and enemy.has_capsule:
            # Push enemy!
            ship_loc = game.get_enemy_mothership().location
            push_to = Location(row=pirate.location.row, col=(-1 if ship_loc.col<3200 else 6401))
            pirate.push(enemy, push_to)
            # Print a message.
            # Did push.
            return True
 
    # Didn't push.
    return False
 
def bunk_move(pirate, game):
    #NoBeard.GenTwo
    radius = 400
    ship = game.get_enemy_mothership()
    ship_x = ship.location.col
    ship_y = ship.location.row
   
    #if someone is holding the enemie's capsule
    if game.get_enemy_capsule().holder != None:
        #find ehc = the enemy who holds the capsule
        ehc = game.get_enemy_capsule().holder
        ehc_x = ehc.location.col
        ehc_y = ehc.location.row
       
        angle = math.atan( (ehc_y-ship_y)/(ehc_x-ship_x) )
       
       
        goto_x = ship_x + (radius * math.cos(angle) * (-1 if ship_x>3200 else 1))
        goto_y = ship_y + (radius * math.sin(angle) * (-1 if ship_x>3200 else 1))
   
    else:
        goto_x = ship_x + (radius * math.sqrt(2)/2 * (-1 if ship_x>3200 else 1))
        goto_y = ship_y + (radius * math.sqrt(2)/2 * (-1 if ship_x>3200 else 1))
   
    goto_location = Location(col=int(goto_x), row=int(goto_y))
   
    pirate.sail(goto_location)
 
 
def try_push(pirate, game):
    """
   Makes the pirate try to push an enemy pirate. Returns True if it did.
 
   :param pirate: The pushing pirate.
   :type pirate: Pirate
   :param game: The current game state.
   :type game: PirateGame
   :return: True if the pirate pushed.
   :rtype: bool
   """
    # Go over all enemies.
    for enemy in game.get_enemy_living_pirates():
        # Check if the pirate can push the enemy.
        if pirate.can_push(enemy):
            # Push enemy!
            pirate.push(enemy, enemy.initial_location)
            # Print a message.
            print 'pirate', pirate, 'pushes', enemy, 'towards', enemy.initial_location
            # Did push.
            return True
 
    # Didn't push.
    return False
   
 
def do_turn(game):
   
   
    mothership = game.get_my_mothership()
    enemy_mothership = game.get_enemy_mothership()
    enemy_mine = game.get_enemy_capsule().initial_location
    pivot_x = mothership.location.col + 1400 if mothership.location.col < 3200 else mothership.location.col - 1400
    pivot_y = mothership.location.row
    pivot_point = Location(col=pivot_x, row = pivot_y)
    pirates = game.get_my_living_pirates()
    bunkers = pirates[4:8]
    has_capsule = False
   
    print len(pirates), "ally pirates alive"
    print len(game.get_enemy_living_pirates()), "enemy pirates alive"
 
    for pirate in pirates:
        if pirate in bunkers:
            if not bunk_push(pirate, game):
                bunk_move(pirate, game)
               
               
            continue
        # Try to push, if you didn't - take the capsule and go to the mothership.
        if not try_push(pirate, game):
            # If the pirate doesn't have a capsule, go and get it!
            if pirate.capsule is None and has_capsule == False:
                capsule = game.get_my_capsule()
                pirate.sail(capsule.initial_location)
            # Else, go to my mothership.
            else:
                pirate.sail(pivot_point) if pirate.location.row != pivot_y else pirate.sail(mothership)
 
            #else:
                # Go towards the mothership.
                #pirate.sail(mothership)