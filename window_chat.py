import customtkinter as CTk
import tkinter
import threading
from client import Client

class Window_chat(CTk.CTk):
    def __init__(self):
        #create window
        super().__init__()
        self.geometry('{}x{}'.format(int(self.winfo_screenwidth()*0.6), int(self.winfo_screenheight()*0.6)))
        self.title("ЧАТ")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=2)
        self.columnconfigure(2, weight=1)
        self.client = Client()

        # add scroll char
        self.chat_frame = MyFrame(master=self, client = self.client, width=300, height=200)
        self.chat_frame.grid(row=0, column=0, padx=20, pady=20)

        #add entry for text message
        self.entry = CTk.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=0, column=1, padx=20, pady=20)

        #add button for send message
        def button_command():
            self.client.new_message(self.entry.get())
        self.button = CTk.CTkButton(self, text = 'Send', command = button_command)
        self.button.grid(row=0, column=2, padx=20, pady=20)

        def on_closing():
            print("Выводится при попытке закрытия окна")
            self.chat_frame.close()
            self.client.__del__()
            self.destroy()  # Закрыть окно
        self.protocol("WM_DELETE_WINDOW", on_closing)

class MyFrame(CTk.CTkScrollableFrame):
    def __init__(self, master, client, **kwargs):
        super().__init__(master, **kwargs)
        self.client = client

        # add widgets onto the frame...
        self.label = CTk.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)
        #thread for chat print
        t = threading.Thread(target=self.print_message)
        t.start()

    def close(self):
        self.destroy()


    def print_message(self):
        message = []
        lenght_chat = 10
        while True:
            try:
                _text = self.client.listen()
                _len = len(message)
                message.append(CTk.CTkLabel(self, text = _text))
                message[_len].grid(row=_len, column=0, padx=20)
                if(_len == lenght_chat):
                    message.pop(0).destroy()
            except Exception as e:
                print('Err (print_message): ', e)
                break


if __name__ == '__main__':
    app = Window_chat()
    app.mainloop()
