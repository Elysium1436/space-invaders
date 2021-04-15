print('yeet')

from .game import Game
import os
def main():
    os.chdir(os.path.dirname(__file__))
    g = Game()
    g.execute()

if __name__ == '__main__':
    main()