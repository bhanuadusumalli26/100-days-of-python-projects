from datetime import datetime
import pandas as pd
import random
import smtplib

# Avoid hardcoding credentials for security purposes.
my_email = "bhanuadusumalli3@gmail.com"
password = "pqqdxbxteivcpagb"

today = datetime.now()
today_tuple = (today.month, today.day)

# Assuming the CSV has columns: name, month, day, email
data = pd.read_csv("C:\\100days_python\\day32.py\\birthday-wisher-normal-start\\birthdays.csv")
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}

if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
    
    # Randomly select a letter template
    file_path = f"C:\\100days_python\\day32.py\\birthday-wisher-normal-start\\letter_templates\\letter_{random.randint(1,3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()  # Encrypt the connection
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=birthday_person["email"],  # Using recipient's actual email
            msg=f"Subject: Happy Birthday!\n\n{contents}"  # Append letter contents
        )
