PLACEHOLDER = "[name]"


with open("C:\\100days_python\\day24.py\\Mail Merge Project Completed\\Input\\Names\\invited_names.txt") as names_file:
    names = names_file.readlines()

with open("C:\\python\\day24.py\\Mail Merge Project Completed\\Input\\Letters\\starting_letter.txt") as letter_file:
    letter_contents = letter_file.read()
    for name in names:
        stripped_name = name.strip()
        new_letter = letter_contents.replace(PLACEHOLDER, stripped_name)
        with open(f"C:\\100days_python\\day24.py\\Mail Merge Project Completed\\Output\\ReadyToSend\\{stripped_name}.txt", mode="w") as completed_letter:
            completed_letter.write(new_letter)

