import random
Word_list=['Apple','banana','grapes','mango']
chosen_word=random.choice(Word_list)
guess=input("guess a letter").lower()
for letter in chosen_word:
    if letter==guess:
        print("right")

    else:
       print("wrong")  
display=[]
for _ in range(len(chosen_word)):
    display+='_'
print(display)      
for position in range(len(chosen_word)):
    letter=chosen_word[position]
    if letter==guess:
        display[position]=letter  
print(display)