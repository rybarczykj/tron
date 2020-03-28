# tron.py
# Jack Rybarczyk
# cs 111 Titus Klinge
#
# A two player, one-keyboard clone of the classic arcade game TRON light cylces
# implemented with Zelle's graphics library as a final project for cs111
#
#TODO: Keep track of score
#TODO: Allow caps lock keyboard presses for WASD
#TODO: Implement 3 players or 4 players
#TODO: Implement boost
#TODO: Implement AI

from graphics import *

class motorcycle:
    """A motorcycle that drives and leaves a trail"""

    def __init__(self, color, keylist, startX, startY):
        self.color = color
        self.keylist = keylist
        self.dir = 0
        self.x = startX
        self.y = startY

    def move(self):
        """
        Updates the motorcycles x or y position by 1, depending
        on which direction it's facing
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

    def turn(self, key):
        """
        Faces the bike in the given direction based on the key given.
        Does not allow 180 degree or self turns
        """
        new_dir = self.keylist.index(key) * 90
        if new_dir % 180 == self.dir % 180:
            pass
        else:
            self.dir = new_dir

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
        self.grid=[[0 for y in range(coords)] for x in range(coords)]

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
        banner = Rectangle(Point(coords / 4, 2*coords / 6), Point((3 * coords / 4), (4 * coords / 6)))
        banner.setFill("White")
        banner.draw(self.win)

        message = Text(Point(coords / 2, coords / 2), message)
        message.draw(self.win)
        return banner

def main():
    size = 600 # Size of the window
    coords = 99  # Scale of the window (how many boxes wide)
    board = gameboard(size, coords)

    b = board.announcement(
        "TRON clone \n Jack Rybarczyk \n cs 111 \n \n "
        "press any key to start \n \n Red: wasd \n Yellow: arrow keys")
    board.win.getKey()
    b.undraw()

    restart = True

    try:
        while restart == True:
            board.clear()
            board.add_border()

            player1 = motorcycle("Red", ["d", "w", "a", "s"], coords // 3, coords // 2)
            player2 = motorcycle("Yellow", ["Right", "Up", "Left", "Down"], (2 * coords // 3)-1, coords // 2)
            PLAYERS = [player1, player2]

            while True:
                keypress = board.win.checkKey()
                PLAYERS_COPY = PLAYERS[:]
                for player in PLAYERS:
                    player.move()

                    if keypress in player.keylist:
                        player.turn(keypress)

                    # If crashed
                    if board.grid[player.x][player.y] != 0:
                        PLAYERS_COPY.remove(player)
                    else:
                        board.fill_a_box(player.color, player.x, player.y)
                if len(PLAYERS)-len(PLAYERS_COPY)>=1:
                    PLAYERS = PLAYERS_COPY
                    break
                update(30)

            if len(PLAYERS) == 0 or (player1.x == player2.x and player1.y == player2.y):
                result_banner = board.announcement\
                    ("It's a tie! \n\n 'q' to quit \n 'r' to restart")
            else:
                result_banner = board.announcement(PLAYERS[0].color +
                    " wins! \n\n 'q' to quit \n 'r' to restart")

            while True:
                keypress = board.win.checkKey()
                if keypress == "r":
                    result_banner.undraw()
                    break
                elif keypress == 'q':
                    restart = False
                    break
    except GraphicsError:
        pass

if __name__ == "__main__":
    main()
