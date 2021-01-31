import unittest

class TestCreature(unittest.TestCase):

    def test_alive_0(self):
        from creature import Creature
        # This is an exmaple of initializing this game and displaying the current gameboard
        world_size = (5,5)

        # Our creature is going to start at position (2,2) in the world, facing "North"
        creature = Creature(500, world_size, (2,2), init_facing='N')

        self.assertEqual(True, creature.is_alive())


    def test_alive_1(self):
        from creature import Creature
        # This is an exmaple of initializing this game and displaying the current gameboard
        world_size = (5,5)

        # Our creature is going to start at position (2,2) in the world, facing "North"
        creature = Creature(0, world_size, (2,2), init_facing='N')

        self.assertEqual(False, creature.is_alive())


    def test_kill(self):
        from creature import Creature
        # This is an exmaple of initializing this game and displaying the current gameboard
        world_size = (5,5)

        # Our creature is going to start at position (2,2) in the world, facing "North"
        creature = Creature(700, world_size, (2,2), init_facing='N')
        creature.kill()

        self.assertGreaterEqual(0, creature.score)


    def test_move_forward(self):
        from creature import Creature
        # This is an exmaple of initializing this game and displaying the current gameboard
        world_size = (5,5)

        # Our creature is going to start at position (2,2) in the world, facing "North"
        creature = Creature(700, world_size, (2,2), init_facing='N')
        creature.move_forward()


        self.assertEqual((2,1), creature.current_location)


    def test_rotate_left(self):
        from creature import Creature
        # This is an exmaple of initializing this game and displaying the current gameboard
        world_size = (5,5)

        # Our creature is going to start at position (2,2) in the world, facing "North"
        creature = Creature(700, world_size, (2,2), init_facing='N')
        self.assertEqual('N', creature.facing)
        creature.rotate_left()
        self.assertEqual('W', creature.facing)
        creature.rotate_left()
        self.assertEqual('S', creature.facing)
        creature.rotate_left()
        self.assertEqual('E', creature.facing)
        creature.rotate_left()
        self.assertEqual('N', creature.facing)
        creature.rotate_left()
        

    def test_rotate_right(self):
        from creature import Creature
        # This is an exmaple of initializing this game and displaying the current gameboard
        world_size = (5,5)

        # Our creature is going to start at position (2,2) in the world, facing "North"
        creature = Creature(700, world_size, (2,2), init_facing='N')
        self.assertEqual('N', creature.facing)
        creature.rotate_right()
        self.assertEqual('E', creature.facing)
        creature.rotate_right()
        self.assertEqual('S', creature.facing)
        creature.rotate_right()
        self.assertEqual('W', creature.facing)
        creature.rotate_right()
        self.assertEqual('N', creature.facing)
        creature.rotate_right()


    def test_north_wall(self):
        from creature import Creature
        # This is an exmaple of initializing this game and displaying the current gameboard
        world_size = (5,5)

        # Our creature is going to start at position (2,2) in the world, facing "North"
        creature = Creature(700, world_size, (2,2), init_facing='N')
        for k in range(0,5):
            creature.move_forward()

        self.assertEqual((2,0), creature.current_location)


    def test_west_wall(self):
        from creature import Creature
        # This is an exmaple of initializing this game and displaying the current gameboard
        world_size = (5,5)

        # Our creature is going to start at position (2,2) in the world, facing "North"
        creature = Creature(700, world_size, (2,2), init_facing='W')
        for k in range(0,5):
            creature.move_forward()

        self.assertEqual((0,2), creature.current_location)


    def test_east_wall(self):
        from creature import Creature
        # This is an exmaple of initializing this game and displaying the current gameboard
        world_size = (5,5)

        # Our creature is going to start at position (2,2) in the world, facing "North"
        creature = Creature(700, world_size, (2,2), init_facing='E')
        for k in range(0,5):
            creature.move_forward()

        self.assertEqual((4,2), creature.current_location)


    def test_south_wall(self):
        from creature import Creature
        # This is an exmaple of initializing this game and displaying the current gameboard
        world_size = (5,5)

        # Our creature is going to start at position (2,2) in the world, facing "North"
        creature = Creature(700, world_size, (2,2), init_facing='S')
        for k in range(0,5):
            creature.move_forward()

        self.assertEqual((2,4), creature.current_location)
