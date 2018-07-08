"""
    A graphical user interface which opens the COM4 port for communication with Arduino
    Author: Th. Housiadas
    Date: 06 - Jul - 2018
    Version: 0.1.1

"""
import tkinter as tk
from multiprocessing import Queue
from tkinter import ttk
import serial
import threading


class SerialCommunication:

    def __init__(self, root):
        self.root = root
        self.queue = Queue()
        self.run = True
        try:
            self.ser = serial.Serial(port='COM4', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS, timeout=0)
            self.gui = App(self.root, self.queue, self.ser)
            self.thread1 = threading.Thread(target=self.data_input)
            self.thread1.start()
        except serial.SerialException:
            self.error = tk.Frame(self.root, bg='lightgrey')
            self.error.pack()
            self.lab = tk.Label(self.error, text='COM not found', font='Consolas 20', bg='lightgrey')
            self.lab.pack()



    def data_input(self):
        seq = []
        count = 1
        while self.run:
            for c in self.ser.read_until('\n'):
                stream = seq.append(chr(c))
                joined_seq = ''.join(str(v) for v in seq)  # Make a string from array
                if chr(c) == '\n':
                    self.queue.put(joined_seq[:len(joined_seq) - 1])
                    seq = []
                    count += 1
                    break

    def close_app(self):
        self.run = False


class App:
    '''
        This is the main app for GUI application
    '''
    def __init__(self, root, queue, ser):
        self.root = root
        self.ser = ser
        self.root.title("Serial Monitor")
        self.queue = queue
        self.create_widgets()
        self.periodic_call()

    def create_widgets(self):
        """ make the main panel """
        # upload the widgets
        self.style_widgets()
        # The first frame up in the window
        self.f0 = tk.Frame(self.root, padx=3, pady=3, bg='lightgrey')
        self.f0.pack(side='top', fill='x')

        self.entry = ttk.Entry(self.f0, font='Consolas 10', width=83)
        self.entry.pack(side='left', fill='both', expand=1)
        self.send = ttk.Button(self.f0, text='Send')
        self.send.pack(side='left', fill='x', expand=0)
        self.entry.bind('<Return>', self.get_entry)
        self.send.bind('<1>', self.get_entry)

        self.f1 = tk.Frame(self.root, padx=1, pady=1)
        self.f1.pack(side='top', fill='both', expand=1)
        self.sbar = tk.Scrollbar(self.f1)
        self.text = tk.Text(self.f1, relief='raised', font='Consolas 10')
        self.sbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.sbar.set)
        self.sbar.pack(side='right', fill='y')
        self.text.pack(side='left', expand=1, fill='both')

        self.f2 = tk.Frame(self.root, padx=3, pady=3, bg='lightgrey')
        self.f2.pack(side='top', fill='x')
        self.checkscroll = ttk.Checkbutton(self.f2, text='Autoscroll')
        self.checkscroll.pack(side='left')

        self.clear = ttk.Button(self.f2, text='Clear')
        self.clear.pack(side='right')
        self.clear.bind('<1>', self.clear_text)

        # BaudRate OptionMenu
        self.baudopt = tk.StringVar()
        self.baudopt.set('9600')
        baud = ttk.OptionMenu(self.f2, self.baudopt, '9600', '300', '1200', '2400', '4800', '9600', '19200',
                              '38400', '57600', '74880', '115200', '230400', '250000', '500000', '1000000', '2000000',
                              style='B.TMenubutton')
        baud.pack(side='right')
        opt = tk.StringVar()
        opt.set('Both NL  &  CL')
        menu_btn = ttk.OptionMenu(self.f2, opt, 'Both NL  &  CL', 'No line ending',
                                  'Newline', 'Carriage Return', 'Both NL  &  CL')
        menu_btn.pack(side='right')

    def style_widgets(self):
        """
            This method configures the style of the top widgets
        """
        self.s = ttk.Style(self.root)
        #s.theme_use('clam')
        self.s.configure('TMenubutton', background='lightgrey', font=('Consolas', 11))
        self.s.configure('B.TMenubutton', background='lightgrey', font=('Consolas', 11), width=10)
        self.s.configure('TButton', background='lightgrey', font=('Consolas', 11))
        self.s.configure('TCheckbutton', background='lightgrey', font=('Consolas', 11))

    def clear_text(self, events):
        self.text.delete('1.0', 'end')

    def periodic_call(self):
        """
            Checks every 200 ms if there is something new in the queue
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)

                self.text.insert(tk.END, msg)
                self.text.insert(tk.END, '\n')
            except Queue.empty():
                pass
        self.root.after(200, self.periodic_call)

    def get_entry(self, events):
        ind = self.entry.get() + '\n'            # I have added the newline character because in the arduino code
        ind_bytes = str.encode(ind)              # i have implemented like this
        self.ser.write(ind_bytes)
        print(ind_bytes)
        self.entry.delete('0', 'end')


if __name__ == '__main__':
    root = tk.Tk()
    serA = SerialCommunication(root)
    root.mainloop()
    serA.close_app()
    import sys
    sys.exit(0)


