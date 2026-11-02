import tkinter as tk
from tkinter import scrolledtext
import eliza


class ElizaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Eliza Chatbot")
        self.root.geometry("550x650")

        # Loading Eliza chatbot
        self.bot = eliza.Eliza()
        self.bot.load("doctor.txt")

        # Creating a scrollable text area
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', font=("Arial", 12))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Creating a frame area for input box and send button
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=10, fill=tk.X)

        # The input field (Place where user types their message)
        self.input_field = tk.Entry(input_frame, font=("Arial", 12))
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Allowing pressing the "Enter" key to send messages
        self.input_field.bind("<Return>", self.send_message)

        # The send button
        self.send_button = tk.Button(input_frame, text="Send", font=("Arial", 12), command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        # This displays the initial message from Eliza
        self.display_message("Eliza: " + self.bot.initial())

    def display_message(self, message):
        # A helper method to display messages in the chat area
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def send_message(self, event=None):
        # Sending a message to Eliza
        user_text = self.input_field.get().strip()
        if not user_text:
            return

        # Displays the users message
        self.display_message("You: " + user_text)
        self.input_field.delete(0, tk.END)
        # Get response from Eliza
        response = self.bot.respond(user_text)

        # Checks if user has access after offensive language
        if response and "ACCESS DENIED" in response:
            self.display_message("Eliza: " + response)
            self.input_field.config(state='disabled')
            self.send_button.config(state='disabled')
            return

        # Checking if the user triggered a quit command
        if response is None:
            self.display_message("Eliza: " + self.bot.final())
            self.input_field.config(state='disabled')
            self.send_button.config(state='disabled')
        else:
            self.display_message("Eliza: " + response)

if __name__ == "__main__":
    root = tk.Tk()
    app = ElizaGUI(root)
    root.mainloop()