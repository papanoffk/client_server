import customtkinter as CTk
import tkinter
import threading
from client import Client

class Window_chat(CTk.CTk):
    def __init__(self):
        #create window
        super().__init__()
        self.geometry('{}x{}'.format(int(self.winfo_screenwidth()*0.4), int(self.winfo_screenheight()*0.6)))
        self.title("ЧАТ")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=2)
        self.columnconfigure(2, weight=1)

        self.window = None
        self.client = None
        self.chat_frame = None

        #add label for important message
        self.label = CTk.CTkLabel(self, text = 'Подключение')
        self.label.grid(row=0, column=1)

        #add entry for text message
        self.entry = CTk.CTkEntry(self, placeholder_text="Entry text")
        self.entry.grid(row=1, column=1, padx=20, pady=20)

        #create menu
        self.screen_of_input_name()

        #close window
        def on_closing():
            print("Выводится при попытке закрытия окна")
            #проверка на существование объектов
            if self.chat_frame is not None:
                 self.chat_frame.destroy()
            if self.client is not None:
                self.client.__del__()
            self.destroy()  # Закрыть окно
        self.protocol("WM_DELETE_WINDOW", on_closing)

    # scree with start input name
    def screen_of_input_name(self):
        def button_command():
            #проверка ввода имени and start server
            _name = self.entry.get()
            if ' ' in _name or _name == '':
                self.label.configure(text = "Имя не подходит")
            else:
                self.run_speak_with_server(_name)
                button.destroy()

        button = CTk.CTkButton(self, text = 'Подключиться', command = button_command)
        button.grid(row=0, column=2, padx=20, pady=20)

    # start work client server
    def run_speak_with_server(self, name):
        self.label.configure(text = "CHAT")

        #client
        self.client = Client(name)
        conn = self.client.connect()
        if conn:
            self.label.configure(text = "Успешное подключение")
        else:
            self.label.configure(text = "Это имя уже занято!")
            self.screen_of_input_name()
            return

        # add scroll char
        self.chat_frame = Chat_frame(master=self, client = self.client, label = self.label, _func = self.run_speak_with_server, width=300, height=200)
        self.chat_frame.grid(row=0, column=0, padx=20, pady=20)

        #add button for send message
        def button_command():
            self.client.new_message('message', self.entry.get())
        self.button = CTk.CTkButton(self, text = 'Send', command = button_command)
        self.button.grid(row=0, column=2, padx=20, pady=20)

class Chat_frame(CTk.CTkScrollableFrame):
    def __init__(self, master, client, label, _func, **kwargs):
        super().__init__(master, **kwargs)
        func = _func
        self.label = label
        self.client = client

        #thread for chat print
        t = threading.Thread(target=self.print_message)
        t.start()

    def print_message(self):
        message = []
        lenght_chat = 10
        quit = False
        i = 1
        while not quit:
            try:
                # recive message
                quit, _text = self.client.listen()
                if quit:
                    self.label.configure(text = _text)
                    break
                #pozition in chat frame
                _len = len(message)
                message.append(CTk.CTkLabel(self, text = _text))
                message[_len].grid(row=i, column=0, padx=20)
                if(_len == lenght_chat):
                    message.pop(0).destroy()
                i+=1
            except Exception as e:
                print('Работа закончена!', e)
                break

if __name__ == '__main__':
    app = Window_chat()
    app.mainloop()
