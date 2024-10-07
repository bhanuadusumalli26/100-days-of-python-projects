
import pandas
student_data_frame = pandas.read_csv("C:\\100days_python\day26.py\\nato_phonetic_alphabet.csv")
data_dic={row.letter:row.code for (index,row) in student_data_frame.iterrows()}
def genenerate_phonetic():
    word=input("Enter a word:").upper()
    try:
        output_list=[data_dic[letter] for letter in word]
    except KeyError:
        print("Sorry ,only letters in the alphabet please.")
        genenerate_phonetic()
    else:
        print(output_list)
genenerate_phonetic()