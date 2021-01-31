import numpy as np
"""
These are the functions to play different straetegies in PointyGame
"""
def num_rewards_remaining(points):
    rewards_remaining = 0
    for row in points:
        for cell in row:
            if cell > 0:
                rewards_remaining += 1
    return rewards_remaining

def no_more_rewards(points):
    return num_rewards_remaining(points) == 0


def play_move_forward(game, creature):
    """
    Play always moves the creature forward
    """
    return 'F'

def play_rotate_left(game, creature):
    """
    Play always rotates the creature left
    """
    return 'L'

def play_rotate_right(game, creature):
    """
    Play always rotates the creature right
    """
    return 'R'

def play_exit(game, creature):
    """
    Play always ends the game
    """
    return 'X'

def play_randomly(game, creature):
    import numpy as np
    """
    Play will always randomly chose (with weight) from a rotation or movement option
    """
    possible_moves = ['F', 'L', 'R']
    return np.random.choice(possible_moves, p=[0.50, 0.25, 0.25])


# Change this cell to implement a "locally greedy" solution to the game
# as described in the comments.

def get_max_local(cr_x, cr_y, current_facing, points, world_w, world_h):
    """
    Return the cardinal direction with the highest point value and that value.
    
    This will bias movement in the order the offset dictionary
    is iterated over as the first key examined will break any tie.
    """
    offsets = {
        'N':(0,-1), 
        'E':(1,0), 
        'S':(0,1), 
        'W':(-1,0)
    }
    
    big_bad = -10000   # This should be lower than any cell's penalty
    max_local = big_bad # This will store the point value of the largest reward 
    point_toward = None # This will store the direction the creature should face
                        # to get the most rewards
        
    # Iterate around our offsets
    local_points = {}
    for facing,offset in offsets.items():
        off_x, off_y = offset
        new_x = cr_x + off_x
        new_y = cr_y + off_y
        points_facing = None
        if new_x < 0 or new_x >= world_w or new_y < 0 or new_y >= world_h:
            points_facing = big_bad
        else:
            points_facing = points[new_y][new_x]
        local_points[facing] = points_facing
        if points_facing > max_local:
            max_local = points_facing
            point_toward = facing

    if local_points[current_facing] == max_local:
        return current_facing
    return point_toward
                
    
def find_distance(curr, dest):
    """
    Return a pair left, right that will be the
    number of turns needed to move the current
    facing to be the one in destination
    """
    locales = {
        'N':0,
        'E':1,
        'S':2,
        'W':3
    }
    dist_right =  (locales[dest]-locales[curr])%4
    dist_left = (locales[curr]-locales[dest])%4
    return dist_left, dist_right
    
    

def play_greedily(game, creature):
    """
    I would like you to play a locally greedy strategy.
    
    In this strategy, you will only be examining the four cells
    you can rotate to around the creature.
    
    To play this strategy, you will rotate the creature to face
    the cell with the highest reward then walk forward to claim it.  
    
    Ties can be randomly broken.
    
    If there is no cell with a reward around the creature, 
    pick a heuristic that you'd like and use it to move.  
    
    Try to optimize your creature's score.
    
    I will allow you to examine the global state of the game to
    know when to end: when there are no more rewards.
    
    (Open question: Is this the optimal strategy?)
    """
    cr_x, cr_y = creature.current_location
    world_w, world_h = creature.world_size
    points = game
    current_facing = creature.facing
    
    if no_more_rewards(game):
        return 'X'
    
    
    # We want to see which cell we should point toward
    # We're greedy -- we want the cell with the highest point value
    point_toward = get_max_local(cr_x, cr_y, current_facing, points, world_w, world_h)
    
    #print('Should point toward', {point_toward})
    
    # If we're facing the highest reward cell, go forward
    if current_facing == point_toward:
        return 'F'
    else:
        # Otherwise we're going to have to rotate
        num_left, num_right = find_distance(current_facing, point_toward)
        if num_left < num_right:
            return 'L'
        else:
            return 'R' # This will bias right if there is a tie
    

def play_greedy_with_random(game, creature):
    odds_random = 0.25
    to_play = play_greedily(game, creature)
    if to_play == 'X':
        return 'X'
    if np.random.random() < odds_random:
        return play_randomly(game, creature)
    return to_play