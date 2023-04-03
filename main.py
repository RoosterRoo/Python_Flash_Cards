from tkinter import *
import pandas as pd
import random
import os

BACKGROUND_COLOR = "#B1DDC6"
flash_card_word = {}

try:
    to_learn = pd.read_csv('data/words_to_learn.csv').to_dict(orient='records')
except FileNotFoundError:
    # print(2)
    flash_cards_data = pd.read_csv('data/french_words.csv').to_dict(orient='records')
else:
    # print(1)
    flash_cards_data = to_learn


def next_card():
    global flash_card_word, flip_timer
    if not len(flash_cards_data):
        # print("You have learnt all the words...")
        canvas.itemconfig(title, text="Congratulations!!!")
        canvas.itemconfig(word, text="You have learnt all the words")
        wrong_button['state'] = 'disabled'
        right_button['state'] = 'disabled'
        flash_card_word = ''
        os.remove('data/words_to_learn.csv')
    else:
        flash_card_word = random.choice(flash_cards_data)
        canvas.itemconfig(title, text="French")
        canvas.itemconfig(word, text=f"{flash_card_word['French']}")
        flip_timer = window.after(3000, func=flip_card)


def flip_card():
    window.after_cancel(flip_timer)
    global flash_card_word
    if flash_card_word:
        canvas.itemconfig(title, text="English")
        canvas.itemconfig(word, text=f"{flash_card_word['English']}")


def create_word_file():
    pd.DataFrame(flash_cards_data).to_csv('data/words_to_learn.csv', index=False)


def remove_card():
    flash_cards_data.remove(flash_card_word)
    create_word_file()
    next_card()


def back_to_deck():
    global flash_cards_data, flash_card_word
    create_word_file()
    next_card()


window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
canvas.create_image(400, 263, image=card_front_img)
title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image, highlightthickness=0, command=back_to_deck)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_image, highlightthickness=0, command=remove_card)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()


