from random import randint
from tkinter import *
from tkinter.messagebox import showinfo
from functools import partial



NEIGHBORS = [
    lambda x, y: (x - 1, y - 1), # top left
    lambda x, y: (x - 1, y),     # top
    lambda x, y: (x - 1, y + 1), # top right
    lambda x, y: (x,     y - 1), # left
    lambda x, y: (x,     y + 1), # right
    lambda x, y: (x + 1, y - 1), # bottom left
    lambda x, y: (x + 1, y),     # bottom
    lambda x, y: (x + 1, y + 1)  # bottom right
]



class Matrix:

    def __init__(self, numberOfRows, numberOfColumns, numberOfMines):

        self.numberOfRows = numberOfRows
        self.numberOfColumns = numberOfColumns
        self.numberOfMines = numberOfMines

        self.neighbors = NEIGHBORS
        
        
    def creates_the_matrix(self):

        self.matrix = [[0 for x in range(self.numberOfColumns)] for x in range(self.numberOfRows)]


    def put_mines_in_the_matrix(self):

        while True:
            self.minePositions = []
            self.creates_the_matrix()

            while len(self.minePositions) != self.numberOfMines:
                minePosition = [randint(0, self.numberOfRows - 1), randint(0, self.numberOfColumns - 1)]

                if minePosition not in self.minePositions: 
                    self.minePositions.append(minePosition) 
                    self.matrix[minePosition[0]][minePosition[1]] = 'M'
                
            if self.checks_if_there_are_accumulated_mines_in_the_matrix(self.matrix):
                break


    def checks_if_there_are_accumulated_mines_in_the_matrix(self, matrix):
       
        for x in range(self.numberOfRows):

            for y in range(self.numberOfColumns):
                numberOfMines = 0
                numberOfNeighbors = 0

                for neighborPosition in self.neighbors:
                    try:
                        xN, yN = neighborPosition(x, y)
                        
                        if xN < 0 or yN < 0:
                            raise IndexError

                        numberOfNeighbors += 1

                        if self.matrix[xN][yN] == 'M':
                            numberOfMines += 1

                    except IndexError:
                        pass
            
                if numberOfNeighbors == numberOfMines:
                    return False

        return True


    def put_number_in_the_matrix(self):
        
        for x, y in self.minePositions:

            for positionNeighbor in self.neighbors:
                try:
                    xN, yN = positionNeighbor(x, y)
                    if xN < 0 or yN < 0: 
                        raise IndexError

                    if self.matrix[xN][yN] != 'M':
                        self.matrix[xN][yN] += 1
       
                except IndexError:
                    pass


    def main(self):

        self.creates_the_matrix()
        self.put_mines_in_the_matrix()
        self.put_number_in_the_matrix()

        return self.matrix



class Minesweeper:

    def __init__(self, window, matrix):

        self.matrix = matrix
        self.x = len(self.matrix)
        self.y = len(self.matrix[0])

        self.window = window

        self.flags = []
        self.mines = []
        
        self.neighbors = NEIGHBORS

        self.game_creator()

        self.window.resizable(0, 0)
        self.window.title('Minesweeper')
        self.window.mainloop()


    def game_creator(self):

        if self.x * self.y == 400:

            size = 15
            
            self.window.geometry(f"{self.x * size}x{self.y * size}")
            self.images('big')

        else:

            size = 21
            self.window.geometry(f"{self.x * size}x{self.y * size}")
            self.images('small')


        for x in range(self.x):
            for y in range(self.y):
                    
                pos = [x, y]

                label = Label(window, borderwidth=1, relief='groove', bg='darkgrey')

                self.matrixButtons[x][y] = Button(self.window, image = self.bgButton)
                self.matrixButtons[x][y].bind("<Button-3>", partial(self.right_click, self.matrixButtons[x][y]))

                if self.matrix[x][y] == 'M':
                        
                    self.mines.append(self.matrixButtons[x][y])
                    self.matrixButtons[x][y].config(command = partial(self.game_over, self.matrixButtons[x][y]))

                    label.config(image = self.mine)

                else:
                    self.matrixButtons[x][y].config(command = partial(self.left_click, self.matrixButtons[x][y], pos))
                    self.put_pictures(x, y, label)

                label.place(x= x*size, y = y*size)
                self.matrixButtons[x][y].place(x= x*size, y = y*size)


    def put_pictures(self, x, y, label):

            if self.matrix[x][y] == 0: label.config(image = self.zero)
            if self.matrix[x][y] == 1: label.config(image = self.one)
            if self.matrix[x][y] == 2: label.config(image = self.two)
            if self.matrix[x][y] == 3: label.config(image = self.three)
            if self.matrix[x][y] == 4: label.config(image = self.four)
            if self.matrix[x][y] == 5: label.config(image = self.five)
            if self.matrix[x][y] == 6: label.config(image = self.six)
            if self.matrix[x][y] == 7: label.config(image = self.seven)


    def images(self, gameSize):

        if gameSize == 'big': 
            
            self.zero     = PhotoImage(file = "images/bigGame/zero.png")
            self.one      = PhotoImage(file = "images/bigGame/one.png")
            self.two      = PhotoImage(file = "images/bigGame/two.png")
            self.three    = PhotoImage(file = "images/bigGame/three.png")
            self.four     = PhotoImage(file = "images/bigGame/four.png")
            self.five     = PhotoImage(file = "images/bigGame/five.png")
            self.six      = PhotoImage(file = "images/bigGame/six.png")
            self.seven    = PhotoImage(file = "images/bigGame/seven.png")
            self.mine     = PhotoImage(file = "images/bigGame/mine.png")
            self.explosion= PhotoImage(file = "images/bigGame/explosion.png")
            self.flag     = PhotoImage(file = "images/bigGame/flag.png")
            self.bgButton = PhotoImage(file = "images/bigGame/backgroundButton.png")

        if gameSize == 'small':
            self.zero     = PhotoImage(file = "images/smallGame/zero.png")
            self.one      = PhotoImage(file = "images/smallGame/one.png")
            self.two      = PhotoImage(file = "images/smallGame/two.png")
            self.three    = PhotoImage(file = "images/smallGame/three.png")
            self.four     = PhotoImage(file = "images/smallGame/four.png")
            self.five     = PhotoImage(file = "images/smallGame/five.png")
            self.six      = PhotoImage(file = "images/smallGame/six.png")
            self.seven    = PhotoImage(file = "images/smallGame/seven.png")
            self.mine     = PhotoImage(file = "images/smallGame/mine.png")
            self.explosion= PhotoImage(file = "images/smallGame/explosion.png")
            self.flag     = PhotoImage(file = "images/smallGame/flag.png")
            self.bgButton = PhotoImage(file = "images/smallGame/backgroundButton.png")
    

    def left_click(self, button, pos):

        x, y = pos

        self.deletedButtons = []
        button.destroy()
        self.deletedButtons.append(button)

        if self.matrix[x][y] == 0:
            
            self.delete_blank_buttons(x, y)


    def delete_blank_buttons(self, x, y):
                
        for func in self.neighbors:
                    
            try:
                        
                xN, yN = func(x, y)

                if xN < 0 or yN < 0:
                        
                    raise IndexError
                        
                if self.matrix[xN][yN] != 'M':
                            
                    if self.matrixButtons[xN][yN] not in self.deletedButtons:
                                
                        self.matrixButtons[xN][yN].destroy()
                        self.deletedButtons.append(self.matrixButtons[xN][yN])
                            
                        if self.matrix[xN][yN] == 0:
                                    
                            self.delete_blank_buttons(xN, yN)

            except IndexError:
                        
                pass


    def right_click(self, button, event):

        if button['state'] == 'normal':

            button.config(image = self.flag)
            button['state'] = 'disabled'

        else:

            button.config(image = self.bgButton)
            button['state'] = 'normal',


    def victory(self, button):

        self.flags.append(button)

        for x in self.flags:

            if x not in self.flags:
                return

        if len(self.flags) == len(self.mines):
            
            showinfo("Victory!", "You won")

            self.window.destroy()


    def game_over(self, button):

        button.destroy()

        showinfo("Game Over!", "Game Over")

        self.window.destroy()


if __name__ == '__main__':

    while True:

        rows = int(input("Type number of rows: "))
        columns = int(input("Type number of columns: "))
        mines = int(input("Type number of mines: "))

        window = Tk()
        matrix = Matrix(rows, columns, mines).main()
        Minesweeper(window, matrix)

        r = str(input("Continue? ")).upper()
        if r[0] == 'N':
            break
