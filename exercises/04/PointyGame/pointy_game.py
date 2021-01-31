"""
This is the module that implements the PointyGame.


There are two classes in this module:

class Reward:
    The rewards in the game

class Game:
    The class that implements the entire game.


See the associated notebook for further details.
"""


#import matplotlib.pyplot as plt
import numpy as np
import urllib3
import copy
import pickle
from PIL import Image, ImageDraw, ImageFont


class Reward:
    """
    This is just a simple class to keep track of the probabilities, points, and graphical
    elements for a reward.
    """
    def __init__(self, prob, points, asset=None):
        """
        Initialize a Reward
        
        Args:
            prob: a floating point number for how often this reward should appear
            points: the points given to the creature for this reward
            asset: a graphics object for drawing on the board
        """
        self.prob = prob  
        self.points = points
        self.asset = asset

# Do not change this cell
class Game:
    """
    This is a class that contains the logic to play a simple grid-based game.
    
    The game board must be sized as positive integers.
    
    The creature class implement methods to move about the board:
        move_forward
        rotate_left
        rotate_right
    
    All moves have an associated penalty.  (Think of it as an energy expenditure.)
    
    When a creature enters a grid cell with a reward, it automatically receives a score change
    consistent with that reward.  Rewards can be positive *or* negative.  There is at most
    one reward per cell.
    
    The creature must stay within the boundaries of the world.  If it leaves the boundaries
    of the world it is killed and the game ends.
    
    If the creature dies (its score is zero or less) then the game ends.
    
    Plays of the game can be rendered as a movie to observe how the game is played.
    
    See the play method for how to play turns.
    """
    
    # Rewards are autoamtically obtained when a creatures enters
    # a cell that contains one.  The first two arguments for reward
    # describe the probability of the reward and the points received
    # by a creature that enters a cell with that reward.
    rewards = [
        Reward(0.100, 100, 'cherry'),
        Reward(0.200, 50, 'turnip'),
        Reward(0.075, -100, 'potion-red'),
        Reward(0.150, -30, 'potion-blue')
    ]
    
    
    # Each move has an associated penalty for taking it.
    move_penalties = {
        'F':-10,  # Forward movment
        'L':-5,   # Rotate left
        'R':-5    # Rotate right
    }
    
    
    def __init__(self, world_size, creature):
        """
        Initialize a game
        
        Args:
            world_size: a list or tuple that contains the height and width of 
                        the world, respective
            creature: a creature to play in the world
            
        Returns:
            None
            
        Exceptions:
            Will throw an exception if the world dimensions are not positive
        """
        self.world_width, self.world_height = world_size
        if self.world_width < 1 or self.world_height < 1:
            raise Exception('World dimensions must be positive')
        self.creature = creature
        self.last_move = None # What was the last move
        self.build_world()
        self.init_world_rewards = copy.copy(self.world_rewards) #Backup initial rewards
        self.make_board()
        self.draw_board()
    
    
    
    def build_world(self):
        """
        Build the nested list that contains information about the rewards in the world.
        This is to be called internally.
        
        Args:
            self: ourselves
            
        Returns:
            None, but the world is constructed
        """
        total_reward_prob = 0.0  # Total probability of any type of reward
        probs_list = []   # List of reward probabilities
        
        # We want to create a list of reward probabilities for numpy's choice method
        for r in self.rewards:
            probs_list.append(r.prob)
            total_reward_prob += r.prob
        probs_list.append(1.0-total_reward_prob) # Add in the probability of no reward
        
        
        self.world_rewards = [] # Will hold all rewards for this game
        for y in range(self.world_height):
            row_rewards = []
            for x in range(self.world_width):
                # Given a probability for each reward (including None), select a reward for each cell
                cell = np.random.choice(self.rewards + [None], p=probs_list)
                row_rewards.append(cell)
            self.world_rewards.append(row_rewards)
    
    
    
    def make_board(self):
        """
        This is an internal method to build the gameboard for display 
        from downloaded assets.
        """
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://www.cse.msu.edu/~ruppmatt/itm891/tiles.pickle')
        tiles = pickle.loads(r.data)
        self.assets = tiles
        self.gameboard = Image.new('RGBA', (64*(self.world_width+2), 64*(self.world_height+2)))
        # Laydown land
        for c in range(0,self.world_width):
            for r in range(0, self.world_height):
                x = (c+1)*64
                y = (r+1)*64
                tile_ndx = np.random.choice(len(tiles['land']))
                self.gameboard.paste(tiles['land'][tile_ndx], (x,y))        
        # Laydown water
        for c in range(0,self.world_width):
            x = (c+1)*64
            yy = (self.world_height+1)*64
            self.gameboard.paste(tiles['water']['edge_north'], (x,0))
            self.gameboard.paste(tiles['water']['edge_south'], (x, yy))
        for r in range(0,self.world_height):
            y = (r+1)*64
            xx = (self.world_width+1)*64
            self.gameboard.paste(tiles['water']['edge_west'], (0,y))
            self.gameboard.paste(tiles['water']['edge_east'], (xx,y))
        self.gameboard.paste(tiles['water']['corner_nw'], (0,0))
        self.gameboard.paste(tiles['water']['corner_sw'], (0,(self.world_height+1)*64))
        self.gameboard.paste(tiles['water']['corner_ne'], ((self.world_width+1)*64,0))
        self.gameboard.paste(tiles['water']['corner_se'], ((self.world_width+1)*64,(self.world_height+1)*64))
        
        # Some land lines
        draw = ImageDraw.Draw(self.gameboard)
        for c in range(0,self.world_width-1):
            y_1 = 64
            y_2 = 64*(self.world_height+1)
            x = (2+c)*64
            draw.line([(x,y_1),(x,y_2)], fill='white', width=1)
        for r in range(0,self.world_height-1):
            y = (2+r)*64
            x_1= 64
            x_2 = 64 * (self.world_width+1)
            draw.line([(x_1,y),(x_2,y)], fill='white', width=1)
        return
    
    
    
    def draw_board(self):
        """
        This method will "draw" the current state of the gameboard.
        
        You shouldn't have to call this.
        
        Using display(game.current_board) will display the board
        in the notebook.
        
        Arguments:
            self: the current game
        
        Returns:
            None, but updates self.current_board
        """
        self.current_board = self.gameboard.copy()
        
        # Draw our rewards
        for r, row in enumerate(self.world_rewards):
            for c, reward in enumerate(row):
                if reward is not None:
                    asset_key = reward.asset
                    x = 64*(c+1)
                    y = 64*(r+1)
                    self.current_board.paste(\
                        self.assets[asset_key], (x,y), self.assets[asset_key])
                
        # Draw our creature
        cr_x, cr_y = self.creature.current_location
        x = 64*(cr_x + 1)  # Should be the center of the tile
        y = 64*(cr_y + 1)
        creature_image = self.assets['beaver']
        if self.creature.facing == 'S':
            creature_image = creature_image.rotate(-180)
        elif self.creature.facing == 'E':
            creature_image = creature_image.rotate(-90)
        elif self.creature.facing == 'W':
            creature_image = creature_image.rotate(-270)
        self.current_board.paste(creature_image, (x,y), creature_image)
    
    
    
    def points_matrix(self):
        """
        Return a nested list of points for each cell in the game.  Each top-level element 
        represents a row, and each row represents a cell in that row.  Points for each cell 
        are numbers.
        
        Args:
            self: the game
            
        Returns:
            a list of lists that contains the points for each cell in the game.
        """
        points = []  # We're going to use this to build a points list of lists
        for row in self.world_rewards:
            p_row = []
            for reward in row:
                if reward is None:  # If there is no reward, there are no points
                    p_row.append(0)
                else:
                    p_row.append(reward.points)  #If there is a reward, use its point value
            points.append(p_row)
        return points
        
    
    
    def reset(self):
        """
        Reset the game and the creature to their initial conditions.
        
        Args:
            self: the game
            
        Returns:
            None
        """
        self.creature.reset()
        self.current_world = copy.copy(self.init_world_rewards)
        self.draw_board()
        self.last_move = None
    
    
    
    def adjust_score(self):
        """
        Adjusts the score of the creature based upon what is in the present cell.
        If the creature is outside the bounds, then we return False.  Otherwise
        we attempt to apply the reward in the cell to the creature.
        
        You shouldn't have to call this.
        
        Args:
            self: this game
        
        Returns:
            True (the game may continue) or False (the game must end)
        """
        creature_x, creature_y = self.creature.current_location
        if not self.detect_in_bounds():
            self.creature.kill()
            return False
        self.creature.score += self.points_matrix()[creature_y][creature_x]
        self.world_rewards[creature_y][creature_x] = None  # Remove the reward/poison in this cell
        if not self.creature.is_alive():
            print('The creature is dead!')
            return False
        return True
    
    
    def detect_in_bounds(self):
        """
        Detects if our creature is within the bounds of our game's world.
        If the creature is not, it is killed.
        
        You shouldn't have to call this.
        
        Args:
            self: this game
            
        Returns:
            True or False: is the creature in bounds?
        """
        creature_x, creature_y = self.creature.current_location
        if creature_x < 0 or creature_x >= self.world_width\
            or creature_y < 0 or creature_y >= self.world_height:
            print('The creature is out of bounds!')
            return False
        return True
    
    
        
    def play(self, play_func, render=False, data=None):
        """
        Plays the the game.
        
        Args:
            play_func: a function that may receive parameters for the a PointyGame and a Creature, respectively
            num_moves: the number of moves to play.  The function should return one of the moves:
                'F' for forward
                'L' for rotate left
                'R' for rotate right
                'X' the game should end
            render: should we render a picture of this game?
            data: data to be collected
            
        Returns:
            True/False should the game be allowed to continue?  (Is the creature still alive.)
        """
        # Make sure our gameboard has been drawn
        self.draw_board()
     
        # We should process this cell we're currently on.
        # If we start the game out of bounds or there is a reward on the cell
        # we need to handle these exceptions first at the cost of having
        # to do them twice for each additonal play.
        if not self.adjust_score():
            return False

        # Ask our play_func for a move.  It should return a single-character string
        # as described in the comments above.
        move = play_func(self.points_matrix(), self.creature)
        self.last_move = move # Store our move
        if move == 'F':
            self.creature.move_forward()
        elif move == 'L':
            self.creature.rotate_left()
        elif move == 'R':
            self.creature.rotate_right()
        elif move == 'X':
            return False
        else:
            raise Exception(f'Unknown move {move}')

        # Each move has a penalty.  You can find them at the start of this class's definition
        self.creature.score += self.move_penalties[move]

        # Process the rewards for this cell and see if we are still in bounds
        if not self.adjust_score():
            return False

        # Draw our board
        self.draw_board()
            
        # We can continue the game
        return True
        
        