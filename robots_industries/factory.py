import argparse
import random
import time

from multiprocessing import (
    Event,
    Process,
    Value,
)


class ItemInt:
    """ Iventory item object of Integer type.
    """

    def __init__(self, value, *args, **kwargs):
        """ Class initialization.

        Most of the method in this class are for hide
        some multiprocessing.Value behavior.

        This class is made for imitate an Integer but not
        all the method are implemented yet.

        Arguments:
            value: the value of the multiprocessing.Value to set
            **kwargs: Additional keyword arguments
            *args: Additional arguments
        """
        super().__init__(*args, **kwargs)
        self._value = Value('i', value)

    def __get__(self, instance, owner):
        return self._value.value

    def __set__(self, instance, value):
        with self._value.get_lock():
            self._value.value = value

    def __str__(self):
        return str(self._value.value)

    def __int__(self):
        return int(self._value.value)

    def __repr__(self):
        return repr(self._value.value)

    def __eq__(self, value, /):
        return self._value.value == value

    def __ge__(self, value, /):
        return self._value.value >= value

    def __gt__(self, value, /):
        return self._value.value > value

    def __le__(self, value, /):
        return self._value.value <= value

    def __lt__(self, value, /):
        return self._value.value < value

    def __add__(self, value, /):
        self._value.value += value
        return self

    def __sub__(self, value, /):
        self._value.value -= value
        return self

    def __mod__(self, value, /):
        return self._value.value % value

    def __mul__(self, value, /):
        return self._value.value * value

    def __truediv__(self, value, /):
        return self._value.value / value

    def __rtruediv__(self, value, /):
        return value / self._value.value


class Inventory:
    """ Robot inventory system.
    """
    foo = ItemInt(0)
    bar = ItemInt(0)
    foobar = ItemInt(0)
    pending_robot = ItemInt(0)
    robots = ItemInt(0)
    coins = ItemInt(0)

    def __str__(self):
        """ Basic inventory visiblity.

        Returns:
            dict: A text representation in a dict format
        """
        return str({
            'foo': self.foo,
            'bar': self.bar,
            'foobar': self.foobar,
            'pending_robot': self.pending_robot,
            'robots': self.robots,
            'coins': self.coins,
        })


class Robot(Process):
    """ The main robot class.

    For a more simplistic system each robot is based on the
    multitprocessing.Process class
    """

    def __init__(self, inventory, state, speed, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f'{self.name} initialized, starting work')
        self.inventory = inventory
        self.state = state
        self.speed = speed
        self.inventory.robots += 1
        self.start()

    def run(self):
        """ Overwritten multiprocessing.Process run method.

        Simply launch the worker method of the Robot class.
        """
        while not self.state.is_set():

            self.worker()

        print(f'Day done for {self.name}, enabling standby mode')

    def worker(self):
        """ Basic robot worker method.

        Have a simple algorithm for handling the life of a
        robot, task by task.

        Note: This is maybe not safe in a way there is only a
        lock on the **modification** of the value not on the
        check for doing a particular action.
        """
        # Check if buying a new robot is a possibility
        if self.inventory.coins > 3 and self.inventory.foo > 6:
            self.inventory.coins -= 3
            self.inventory.foo -= 6
            time.sleep(1 * self.speed)
            self.inventory.pending_robot += 1
            print(
                'Successfully buy a new robot for 6 euros.\n',
                f'{self.inventory}',
            )
        # Check if selling some foobar is a possibility
        elif self.inventory.foobar and self.inventory.foobar % 5 == 0:
            self.inventory.foobar -= int(self.inventory.foobar / 5 * 5)
            time.sleep(10 * self.speed)
            self.inventory.coins += 1
            print(
                'Successfully sell a foobar for 1 euros.\n',
                f'{self.inventory}',
            )
        # Check if assembling some foobar is a possibility
        elif self.inventory.foo > 2 and self.inventory.bar > 2:
            print(self.name + ' assembling a foobar...')
            self.inventory.foo -= 1
            self.inventory.bar -= 1
            duration = 2 * self.speed
            time.sleep(duration)
            chance = random.randrange(101)
            if chance > 60:
                status = 'successfully'
                self.inventory.foobar += 1
            else:
                status = 'failed'
                self.inventory.bar += 1
            print(
                f'{self.name} {status} assembled a foobar after ',
                f'{str(duration)} seconds...\n',
                f'Here is our current inventory:\n{self.inventory}',
            )
        # Check if mining some bar is a possibility
        elif self.inventory.foo > 9:
            for action in range(0, 10):
                print(self.name + ' mining some bar...')
                duration = random.uniform(0.5, 2) * self.speed
                time.sleep(duration)
                self.inventory.bar += 1
                print(
                    f'{self.name} minned some bar after {str(duration)} ',
                    'seconds...\n',
                    f'Here is our current inventory:\n{self.inventory}',
                )
        # Check if mining some foor is a possibility
        else:
            for action in range(0, 10):
                print(self.name + ' mining some foo...')
                duration = 1 * self.speed
                time.sleep(duration)
                self.inventory.foo += 1
                print(
                    f'{self.name} minned some foo after {str(duration)} ',
                    'seconds...\n',
                    f'Here is our current inventory:\n{self.inventory}',
                )

        print(f'{self.name} is moving to a new activity...')
        time.sleep(5 * self.speed)


def main():

    parser = argparse.ArgumentParser(
        description='Robots Industries, automate robots building, make money.',
    )
    parser.add_argument(
        '--speed', type=float, default=1,
        help='Speed multiplicator for a second. Default to 1.',
    )
    args = parser.parse_args()

    inventory = Inventory()
    state = Event()
    robots = []
    robots.append(Robot(inventory, state, args.speed))
    robots.append(Robot(inventory, state, args.speed))

    while 0 < inventory.robots < 30:
        for robot in range(0, inventory.pending_robot):
            print('Put robot in production')
            inventory.pending_robot -= 1
            robots.append(Robot(inventory, state, args.speed))

    state.set()

    for robot in robots:
        robot.join()

    print(
        'We have enough robot for now, lets take a break. ',
        'Here is our today result:',
    )
    print(inventory)
