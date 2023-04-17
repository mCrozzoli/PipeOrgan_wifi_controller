import install_requirements

# ---DETECT SERIAL PORT---
import sys
import glob
import serial

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

results = serial_ports()
com_esp = str(results[-1])

# ---OSC BUILDER and SENDER---
from pythonosc import osc_message_builder
import serial
import threading
from threading import Thread

def build_osc_message(address, tempo, data):
    msg = osc_message_builder.OscMessageBuilder(address=address)
    msg.add_arg(tempo)
    for i, row in enumerate(data):
        #row_id = "id:"+str(i)
        open_close = int('9'+''.join(map(str, row)))
        msg.add_arg(open_close)
    return msg.build()

def send_msg(msg, port, bau):
    # Configure serial port
    ser = serial.Serial(port, bau, timeout=None)
    
    print('Sending message...')
    # Define function to receive confirmation message
    def receive_confirmation():
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().strip().decode('utf-8')
                if data == 'OK':
                    print(data)
                    print('Confirmation received from ESP32')
                    return  # Exit thread when confirmation is received

    # Start thread to receive confirmation message
    print('Starting confirmation thread...')
    confirmation_thread = threading.Thread(target=receive_confirmation)
    confirmation_thread.start()

    # Send message over serial
    print('Writing message to serial port...')
    ser.write(msg.dgram)

    # Wait for confirmation thread to finish
    print('Waiting for confirmation...')
    confirmation_thread.join()
    
    # Close serial port
    print('Closing serial port...')
    ser.close()

# ---SERIAL COMMUNICATION CONFIG---
com_port= com_esp
bau = 115200

# ---UI---
import tkinter as tk

class GridCreationScreen:
    def __init__(self, master):
        self.master = master
        self.rows_label = tk.Label(self.master, text='Number of rows:')
        self.rows_label.grid(row=0, column=0)
        self.rows_input = tk.Entry(self.master)
        self.rows_input.grid(row=0, column=1)
        self.columns_label = tk.Label(self.master, text='Number of columns:')
        self.columns_label.grid(row=1, column=0)
        self.columns_input = tk.Entry(self.master)
        self.columns_input.grid(row=1, column=1)
        self.create_button = tk.Button(self.master, text='Create Grid', command=self.create_grid)
        self.create_button.grid(row=2, column=0, columnspan=2)

    def create_grid(self):
        rows = int(self.rows_input.get())
        columns = int(self.columns_input.get())
        self.master.destroy()
        root = tk.Tk()
        app = App(root, rows, columns)
        root.mainloop()

class App:
    def __init__(self, master, rows, columns):
        self.master = master
        self.buttons = []
        self.data = [[0]*columns for _ in range(rows)]
        self.draw_grid(rows, columns)
        self.tempo_input.insert(0, "50")  # set default tempo input to 50
                
    def draw_grid(self, rows, columns):
        # Draw buttons grid
        for i in range(rows):
            row = []
            for j in range(columns):
                btn = tk.Button(self.master, width=5, height=2, bg='white', bd=0, relief='flat', command=lambda i=i, j=j: self.toggle(i, j))
                btn.grid(row=i, column=j*2)
                row.append(btn)
                if j < columns-1:
                    sep = tk.Frame(self.master, width=10, height=2, bg='black')
                    sep.grid(row=i, column=j*2+1)
            self.buttons.append(row)

        # Draw tempo input field
        tempo_label = tk.Label(self.master, text='Tempo')
        tempo_label.grid(row=0, column=columns*2, padx=(20,0))
        self.tempo_input = tk.Entry(self.master, width=5)
        self.tempo_input.grid(row=1, column=columns*2, pady=(0,10))

        # Draw on/off button
        self.save_button = tk.Button(self.master, text='Save', bg='green', fg='white', command=self.save_data)
        self.save_button.grid(row=2, column=columns*2, pady=(0,10))
    
    def toggle(self, i, j):
        self.data[i][j] ^= 1
        if self.data[i][j] == 1:
            self.buttons[i][j].configure(bg='black')
        else:
            self.buttons[i][j].configure(bg='white')

    def save_data(self):
        
        row_data = self.data
        tempo_data = int(self.tempo_input.get())
        print(f"Row Data:\n{row_data}\n")
        print(f"Tempo Data: {tempo_data}")
        
        # Create the OSC message
        osc_address = "/grid"
        osc_message = build_osc_message(osc_address, tempo_data, row_data)

        # Send the message
        send_msg(osc_message, com_port, bau)


if __name__ == "__main__":
    root = tk.Tk()
    grid_creation_screen = GridCreationScreen(root)
    root.mainloop()