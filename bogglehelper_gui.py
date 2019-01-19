"""
gui for bogglehelper

@gschnaars
"""

import bogglehelper as bh
import ReadTime as rt
import tkinter as tk

import time


class BoggleHelperGUI(tk.Tk):
    def __init__(self, matrix_size):
        super().__init__()

        # shape of window in pixels
        # window is resizeable with mouse so this isn't permanent
        self.geometry("950x1000")
        self.resizable(True, True)

        # window title
        self.title('Boggle Helper')

        ############################

        # create frame to hold the Label
        header_frame = tk.Frame(self, pady = 5)
        header_frame.pack()

        lbl = tk.Label(header_frame, text = "Boggle Helper", 
                                font = ('helvetica', 24))
        lbl.pack()

        ############################

        # create scrollbar
        yscroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        xscroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)

        # create canvas for hold matrix
        # must be canvas, as this is one of few Tkinter objects that is compatible w/ scrollbar
        self.matrix_canvas = tk.Canvas(self)
        self.matrix_canvas.pack(fill=tk.BOTH, expand=True)  
        self.matrix_canvas['yscrollcommand'] = yscroll.set
        self.matrix_canvas['xscrollcommand'] = xscroll.set
        yscroll['command'] = self.matrix_canvas.yview
        xscroll['command'] = self.matrix_canvas.xview     


        # create frame within canvas
        matrix_frame = tk.Frame(self.matrix_canvas)
        self.matrix_canvas.create_window(4, 4, window = matrix_frame, anchor = 'nw') 
        matrix_frame.bind("<Configure>", self._on_frame_configure)

        # iteratively create matrix cells
        self.cell_frames = []
        for i in range(matrix_size):
            temp = []
            for j in range(matrix_size):
                cell = CellFrame(matrix_frame)
                cell.grid(column = j, row = i)
                temp.append(cell)
            self.cell_frames.append(temp)

        ############################

        # frame for button
        self.button_frame = tk.Frame(self, pady = 10)
        self.button_frame.pack()

        self.button = tk.Button(self.button_frame, text = 'Solve', 
                                font = ('helvetica', 16), command = self._callback)
        self.button.pack()
   
        ############################


    # callback function to bind scrollbar action
    def _on_frame_configure(self, event = None):
        self.matrix_canvas.configure(scrollregion = self.matrix_canvas.bbox("all"))

    # callback function for button
    def _callback(self):
        # gather inputs, convert to Elements, place in list of lists to pass to Matrix
        start = time.time()
        cells = []
        for i, lst in enumerate(self.cell_frames):
            temp = []
            for j, item in enumerate(lst):
                elem = bh.Element(letter = item.letter,
                                        position = (i, j),
                                        letter_multiplier = item.letter_mult,
                                        word_multiplier = item.word_mult)
                temp.append(elem)
            cells.append(temp)

        # pass Elements to Matrix, solve for words and print
        print('Matrix:')
        m = bh.Matrix(cells)
        print(m)
        print('Working...')
        print(m.find_paths())

        print(rt.read_time(time.time() - start), 'to complete')


class CellFrame(tk.Frame):
    # subclass Frame for identical boggle cells
    def __init__(self, *args):
        # column and row (ints) to be passed for placement in parent frame
        super().__init__(*args)
        # separate cells and 'raise' them
        self.config(borderwidth = 20, relief = 'raised')

        #########################

        self.letter_input        = CellInput(self, title = 'Letter')
        self.letter_input.pack()
        self.letter_mult_input   = CellInput(self, title = 'Letter Mult',
                                            value = 1)
        self.letter_mult_input.pack()
        self.word_mult_input     = CellInput(self, title = 'Word Mult',
                                            value = 1)
        self.word_mult_input.pack()

    @property
    def letter(self):
        # get letter from entry 
        # already string
        return self.letter_input.input

    @property
    def letter_mult(self):
        # get letter multiplier from entry 
        # converted to int
        return int(self.letter_mult_input.input)

    @property
    def word_mult(self):
        # get word multiplier from entry 
        # converted to int
        return int(self.word_mult_input.input)


class CellInput(tk.Frame):
    # subbclass Frame to create identical Input + Entry companions
    def __init__(self, *args, title, value = ''):
        super().__init__(*args)
        # title Label
        label = tk.Label(self, text = title)
        label.pack()
        # create string var for entry field
        self.var = tk.StringVar(value = value)
        # entry field
        entry_input = tk.Entry(self, textvariable = self.var)
        entry_input.pack()

    @property
    def input(self):
        # return value in the entry field
        return self.var.get()
    

if __name__ == '__main__':

    window = BoggleHelperGUI(matrix_size = 4)
    window.mainloop()