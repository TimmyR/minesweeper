# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 11:00:38 2021

Main code for minesweeper package.

@author: TimmyR
"""
# ===========================================================================
# TODO: Find out why foreground option doesn't work with tk Buttons.
# TODO: Error message when grid size and mine number inputs aren't integers.
# TODO: Change colours to something that isn't ridiculous.
# TODO: Add standard game options (easy, medium, dificult)
# TODO: Add a clock.
# ===========================================================================
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import re
from random import randint

import numpy as np

# Global Variables ----------------------------------------------------------

minesweeper = None    # will contain Main class object

rows = int
columns = int
mine_num = int
game_over = False


# Classes -------------------------------------------------------------------


class MineGrid:
    """
    Called whenever the GameWindow opens, creates a random minesweeper grid
    containing the positions of the mines as well as the values of adjacent
    tiles.
    """

    def __init__(self):
        """Create the mine grid."""
        global rows
        global columns
        global mine_num

        self.grid_size = (rows, columns)

        self.mine_pos = []
        self.full_grid = np.empty(self.grid_size, dtype='<U11')

        self.mine_positions(self.grid_size, mine_num)
        self.set_tile_values(self.grid_size)

    def mine_positions(self, grid_size, mine_num):
        """Define the position of the mines."""
        for mine in range(mine_num):
            while True:
                row = randint(0, grid_size[0] - 1)
                column = randint(0, grid_size[1] - 1)

                if [row, column] not in self.mine_pos:
                    self.mine_pos.append([row, column])
                    self.full_grid[row, column] = 'm'
                    break
                else:
                    pass

    def set_tile_values(self, grid_size):
        """
        Set the value of all the tiles that aren't mines, by counting
        how many mines are adjacent to the tile.
        """
        # TODO: make this function a lot clearer and concise.
        for row in range(grid_size[0]):
            for column in range(grid_size[1]):
                if [row, column] in self.mine_pos:
                    continue

                # Create a grid of adjacent tiles for each tile and count
                # the number of mines contained within the grid.
                # Central tiles
                elif (row > 0 and row < grid_size[0] - 1 and column > 0
                      and column < grid_size[1] - 1):
                    adjacent_tiles = self.full_grid[row-1:row+2,
                                                    column-1:column+2]
                    self.full_grid[row, column] = len(
                        np.where(adjacent_tiles == 'm')[0])

                # Exceptions: avoid negative or out-of-bounds indices
                # Corners
                elif row == 0 and column == 0:
                    adjacent_tiles = self.full_grid[row:row+2,
                                                    column:column+2]
                    self.full_grid[row, column] = len(
                        np.where(adjacent_tiles == 'm')[0])

                elif row == 0 and column == grid_size[1] - 1:
                    adjacent_tiles = self.full_grid[row:row+2,
                                                    column-1:column+1]
                    self.full_grid[row, column] = len(
                        np.where(adjacent_tiles == 'm')[0])

                elif (row == grid_size[0] - 1
                      and column == grid_size[1] - 1):
                    adjacent_tiles = self.full_grid[row-1:row+1,
                                                    column-1:column+1]
                    self.full_grid[row, column] = len(
                        np.where(adjacent_tiles == 'm')[0])

                elif row == grid_size[0] - 1 and column == 0:
                    adjacent_tiles = self.full_grid[row-1:row+1,
                                                    column:column+2]
                    self.full_grid[row, column] = len(
                        np.where(adjacent_tiles == 'm')[0])

                # Sides
                elif (row == 0 and column > 0
                      and column < grid_size[1] - 1):
                    adjacent_tiles = self.full_grid[row:row+2,
                                                    column-1:column+2]
                    self.full_grid[row, column] = len(
                        np.where(adjacent_tiles == 'm')[0])

                elif (row == grid_size[0] - 1 and column > 0
                      and column < grid_size[1] - 1):
                    adjacent_tiles = self.full_grid[row-1:row+1,
                                                    column-1:column+2]
                    self.full_grid[row, column] = len(
                        np.where(adjacent_tiles == 'm')[0])

                elif row > 0 and row < grid_size[0] - 1 and column == 0:
                    adjacent_tiles = self.full_grid[row-1:row+2,
                                                    column:column+2]
                    self.full_grid[row, column] = len(
                        np.where(adjacent_tiles == 'm')[0])

                elif (row > 0 and row < grid_size[0] - 1
                      and column == grid_size[1] - 1):
                    adjacent_tiles = self.full_grid[row-1:row+2,
                                                    column-1:column+1]
                    self.full_grid[row, column] = len(
                        np.where(adjacent_tiles == 'm')[0])


class Main:
    """
    Game starting menu.

    The menu contains entries for grid size and the number of mines.
    """

    def __init__(self, root):
        """Create main window."""
        self.root = root
        self.root.title('Minesweeper')

        self.mainframe = ttk.Frame(root)
        self.frame1 = ttk.Frame(self.mainframe, padding=10)
        self.frame2 = ttk.Frame(self.mainframe, padding=10)

        # Widgets
        self.welcome_lbl = ttk.Label(self.frame1, text='Welcome!')
        self.grid_size_lbl = ttk.Label(self.frame1, text='Grid size:')
        self.by_lbl = ttk.Label(self.frame1, text='by', padding=10)
        self.mine_num_lbl = ttk.Label(self.frame1, text='Number of mines:')

        # Entry values
        self.rows = tk.StringVar()
        self.columns = tk.StringVar()
        self.mine_num = tk.StringVar()

        self.row_entry = ttk.Entry(self.frame1, textvariable=self.rows)
        self.column_entry = ttk.Entry(self.frame1,
                                      textvariable=self.columns)
        self.mine_num_entry = ttk.Entry(self.frame1,
                                        textvariable=self.mine_num)

        self.start_btn = ttk.Button(self.frame2, text='Start!',
                                    command=self.start_game)
        self.exit_btn = ttk.Button(self.frame2, text='Exit',
                                   command=self.destroy)

        # Grid positions
        self.mainframe.grid(row=0, column=0, sticky='NSEW')
        self.frame1.grid(row=0)
        self.frame2.grid(row=1)

        self.welcome_lbl.grid(row=0, column=0, columnspan=4)
        self.grid_size_lbl.grid(row=1, column=0, sticky='W')
        self.row_entry.grid(row=1, column=1, sticky='EW')
        self.by_lbl.grid(row=1, column=2)
        self.column_entry.grid(row=1, column=3, sticky='EW')
        self.mine_num_lbl.grid(row=2, column=0)
        self.mine_num_entry.grid(row=2, column=3)

        self.exit_btn.grid(row=0, column=0, padx=30)
        self.start_btn.grid(row=0, column=1, padx=30)

    def start_game(self):
        """Start the game."""
        self.master = tk.Toplevel(self.root)
        self.game_window = GameWindow(self.master)

    def destroy(self):
        """Exit the application."""
        self.root.quit()
        self.root.destroy()


class GameWindow:
    """
    Window that contains the game.
    """

    def __init__(self, master):
        """Create the GameWindow."""
        global rows
        global columns
        global mine_num
        global game_over

        self.master = master

        self.mainframe = ttk.Frame(master, padding=10)
        self.mainframe.grid(row=1, column=0)

        self.frame0 = ttk.Frame(master)
        self.frame0.grid(row=0, column=0)

        game_over = False

        try:
            rows = int(minesweeper.rows.get())
            columns = int(minesweeper.columns.get())
            mine_num = int(minesweeper.mine_num.get())

            self.buttons = []
            self.create_buttons()

            self.mine_grid = MineGrid()

        except (ValueError, TypeError):
            if messagebox.showwarning('Error!',
                                      'Please insert numbers!'):
                self.master.destroy()

        self.mines_left_lbl = ttk.Label(self.frame0,
                                        text='Mines left: ')
        self.mines_left_lbl.grid(row=0, column=0)

        self.mines_left = tk.StringVar()
        self.mines_left.set(mine_num)
        ttk.Label(self.frame0, textvariable=self.mines_left).grid(row=0,
                                                                  column=1)

    def create_buttons(self):
        """
        Create the initial button grid on the window. Appends the buttons to
        the self.button list, a 2D list containing the buttons in the same
        position as on the grid.
        """
        global rows
        global columns

        for i in range(rows):
            temp_row = []
            for j in range(columns):
                button = tk.Button(self.mainframe, width=2, relief='raised',
                                   font='sans 9 bold', bg='#99FFCC', fg='red')
                button.bind('<ButtonPress-1>',
                            partial(self.left_click, row=i, column=j))
                button.bind('<ButtonPress-3>',
                            partial(self.right_click, row=i, column=j))
                button.grid(row=i, column=j)

                temp_row.append(button)
            self.buttons.append(temp_row)

    def left_click(self, event, row, column):
        """Command when a game button is left-clicked on."""
        global game_over

        if self.buttons[row][column]['state'] == tk.DISABLED:
            pass

        elif self.buttons[row][column]['state'] == tk.NORMAL:
            self.tile_command(row, column)
            if not game_over:
                self.check_game_won()

    def right_click(self, event, row, column):
        """Command when a game button is right-clicked on."""
        if self.buttons[row][column]['relief'] == 'groove':
            pass

        elif self.buttons[row][column]['state'] == tk.NORMAL:
            self.buttons[row][column]['state'] = tk.DISABLED
            self.buttons[row][column]['text'] = 'F'
            self.buttons[row][column]['bg'] = 'red'
            self.mine_flagged()

        else:
            self.buttons[row][column]['state'] = tk.NORMAL
            self.buttons[row][column]['text'] = ''
            self.buttons[row][column]['bg'] = '#99FFCC'
            self.mine_unflagged()

    def tile_command(self, row, column):
        """
        Execute the tile clearing following a left_click on an enabled tile.
        """
        if self.buttons[row][column]['state'] == tk.DISABLED:
            pass

        elif self.buttons[row][column]['state'] == tk.NORMAL:
            self.buttons[row][column]['state'] = tk.DISABLED

            if (re.match('\d', self.mine_grid.full_grid[row, column]) and
                    self.mine_grid.full_grid[row, column] != '0'):
                # Set text to itself, relief to groove.
                text = self.mine_grid.full_grid[row, column]
                self.buttons[row][column].configure(text=text,
                                                    relief='groove',
                                                    bg='SystemButtonFace',
                                                    fg='red')

            elif self.mine_grid.full_grid[row, column] == 'm':
                text = self.mine_grid.full_grid[row, column]
                self.buttons[row][column]['text'] = text

                if not game_over:
                    self.buttons[row][column]['bg'] = 'red'
                    self.game_over()

            elif self.mine_grid.full_grid[row, column] == '0':
                self.buttons[row][column]['relief'] = 'groove'
                self.buttons[row][column]['bg'] = 'SystemButtonFace'

                for i in range(row-1, row+2):
                    for j in range(column-1, column+2):
                        try:
                            if i >= 0 and j >= 0:
                                self.tile_command(i, j)
                        except IndexError:
                            pass

    def mine_flagged(self):
        """Flags a mine."""
        self.mines_left.set(int(self.mines_left.get()) - 1)

    def mine_unflagged(self):
        """Unflags a mine."""
        self.mines_left.set(int(self.mines_left.get()) + 1)

    def game_over(self):
        """What to do when a mine is exploded."""
        global rows
        global columns
        global game_over

        game_over = True

        for i in range(rows):
            for j in range(columns):
                # Remove all flags before clearing the board.
                if self.buttons[i][j]['text'] == 'F':
                    self.right_click(None, i, j)

                if self.buttons[i][j]['state'] == tk.NORMAL:
                    self.tile_command(i, j)

        self.mines_left.set(0)
        dialog = messagebox.askyesnocancel('Game over!',
                                           'Game over!\n'
                                           'Restart with a new grid?',
                                           type='yesnocancel')

        # Return from dialog is None for Cancel, False for No, True for Yes.
        if dialog is None:
            self.master.destroy()

        elif dialog:
            self.master.destroy()
            minesweeper.start_game()

        elif not dialog:
            self.restart_game()

    def check_game_won(self):
        """Checks to see if the game is won yet..."""
        global rows
        global columns

        untouched_safe_tiles = 0

        for i in range(rows):
            for j in range(columns):
                if (self.buttons[i][j]['relief'] == 'raised' and
                        self.mine_grid.full_grid[i][j] != 'm'):
                    untouched_safe_tiles += 1

        if untouched_safe_tiles == 0:
            self.mines_left.set(0)
            dialog = messagebox.showinfo("Congratulations!",
                                         "Congratulations!\n"
                                         "You've won the game!")
            if dialog:
                self.master.destroy()

    def restart_game(self):
        """Restarts the game with the same grid."""
        global rows
        global columns
        global game_over

        game_over = False

        self.buttons = []
        self.create_buttons()


# Main code ----------------------------------------------------------------
def main():
    """Main code for minesweeper package."""
    global minesweeper

    root = tk.Tk()
    minesweeper = Main(root)
    root.mainloop()


if __name__ == '__main__':
    main()
