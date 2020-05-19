# tron.py
# Jack Rybarczyk
# cs 111 Titus Klinge
#
# A two player, one-keyboard clone of the classic arcade game TRON light cylces
# implemented with Zelle's graphics library as a final project for cs111
#
# TODO: Keep track of score
# TODO: Allow caps lock keyboard presses for WASD
# TODO: Implement 3 players or 4 players?
# TODO: Implement boost?
# TODO: Implement AI

from graphics import *

class motorcycle:
    """A motorcycle that drives and leaves a trail"""

    def __init__(self, color, keylist, startX, startY):
        self.color = color
        self.keylist = keylist
        self.dir = 0
        self.x = startX
        self.y = startY

    def move(self, grid):
        """
        Updates the motorcycles x or y position by 1, depending
        on which direction it's facing
        
        Grid isn't used in this superclass
        """
        d = self.dir
        if d == 0:
            self.x += 1
        elif d == 90:
            self.y -= 1
        elif d == 180:
            self.x -= 1
        elif d == 270:
            self.y += 1

    def takeInput(self, key):
        """
        Takes in a key input and calls takeTurn    
        """
        new_dir = self.keylist.index(key) * 90
        if not (new_dir % 180 == self.dir % 180):
            self.dir = new_dir


class bot(motorcycle):
    """
    Dumb bot only turns left when about to crash
    """

    def move(self, grid):
        super().move(grid)
        if self.getNextSquare(grid) != 0:
            self.turnLeft()

    def turnLeft(self):
        self.dir = (self.dir + 90) % 360

    def turnRight(self):
        self.dir = (self.dir - 90) % 360

    def getNextSquare(self, grid):
        """
        Returns the contents of the next box which will be visitedw
        """
        try:
            if self.dir == 0:
                return grid[self.x + 1][self.y]
            elif self.dir == 90:
                return grid[self.x][self.y - 1]
            elif self.dir == 180:
                return grid[self.x - 1][self.y]
            else:
                return grid[self.x][self.y + 1]
        except IndexError:
            return True


class gameboard():
    """
    Gameboard class manages the grid's visuals and data
    Values in 2D array defaults 0, but change to the color if visited
    represented as a string. Example "Red" or "White"
    """

    def __init__(self, size, coords):
        self.grid = []
        self.coords = coords
        self.win = GraphWin("TRON clone cs111", size, size, autoflush=False)
        self.win.setCoords(0, coords, coords, 0)

        self.clear()
        self.add_border()

    def fill_a_box(self, color, x, y):
        """
        Fills a single square, both visually and in the grid
        """
        r = Rectangle(Point(x, y), Point(x + 1, y + 1))
        r.setFill(color)
        r.draw(self.win)
        self.grid[x][y] = color

    def clear(self):
        """
        Draws a black background over everything and clears 2D array.
        """
        coords = self.coords
        background = Rectangle(Point(0, 0), Point(coords, coords))
        background.setFill("Black")
        background.draw(self.win)
        self.grid = [[0 for y in range(coords)] for x in range(coords)]

    def add_border(self):
        """
        Makes the white border
        Calls: self.fill_a_box()
        """
        buffer = 0
        edge = self.coords - buffer - 1
        for x in range(buffer, edge + 1):
            for y in range(buffer, edge + 1):
                if (x == buffer or x == edge or y == buffer or y == edge):
                    self.fill_a_box("White", x, y)

    def announcement(self, message):
        """
        Creates and draws a banner with the input message.
        Returns: The banner so that it can be undrawn
        """
        coords = self.coords
        banner = Rectangle(Point(coords / 4, 2 * coords / 6), Point((3 * coords / 4), (4 * coords / 6)))
        banner.setFill("White")
        banner.draw(self.win)

        message = Text(Point(coords / 2, coords / 2), message)
        message.draw(self.win)
        return banner


def main():
    size = 600  # Size of the window
    coords = 99  # Scale of the window (how many boxes wide)
    board = gameboard(size, coords)
    b = board.announcement(
        "TRON clone \n Jack Rybarczyk \n cs 111 \n \n "
        "press any key to start \n \n Red: wasd \n Yellow: arrow keys")
    board.win.getKey()
    b.undraw()

    restart = True
    try:
        while restart:
            board.clear()
            board.add_border()

            player1 = motorcycle("Red", ["d", "w", "a", "s"], coords // 3, coords // 2)
            player2 = bot("Yellow", ["Right", "Up", "Left", "Down"], (2 * coords // 3) - 1, coords // 2)
            PLAYERS = [player1, player2]

            while True:
                keys = board.win.checkKeys()
                PLAYERS_TEMP = PLAYERS[:]
                for player in PLAYERS:
                    player.move(board.grid)

                    for key in keys:
                        if key in player.keylist:
                            player.takeInput(key)

                    # If crashed
                    if board.grid[player.x][player.y] != 0:
                        PLAYERS_TEMP.remove(player)
                    else:
                        board.fill_a_box(player.color, player.x, player.y)

                if len(PLAYERS) - len(PLAYERS_TEMP) >= 1:
                    PLAYERS = PLAYERS_TEMP
                    break
                update(30)
            if len(PLAYERS) == 0 or (player1.x == player2.x and player1.y == player2.y):
                result_banner = board.announcement \
                    ("It's a tie! \n\n 'q' to quit \n 'r' to restart")
            else:
                result_banner = board.announcement(PLAYERS[0].color +
                                                   " wins! \n\n 'q' to quit \n 'r' to restart")
            while True:
                key = board.win.checkKey()
                if key == "r":
                    result_banner.undraw()
                    break
                elif key == 'q':
                    restart = False
                    break
                update(30)
    except GraphicsError:
        pass


if __name__ == "__main__":
    main()
