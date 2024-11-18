import smtplib
import datetime as dt
import random

my_email = "bhanuadusumalli3@gmail.com"
password = "pqqdxbxteivcpagb"  # Ensure this is your app password

now = dt.datetime.now()
weekday = now.weekday()

if weekday == 0:  # Check if today is Monday
    try:
        with open("C:\\100days_python\\day32.py\\quotes.txt") as quote_file:
            all_quotes = quote_file.readlines()
            quote = random.choice(all_quotes)
           
        
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()  # Encrypt the connection
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="bhanuadusumalli3@yahoo.com",
                msg=f"Subject: Monday Motivation\n\n{quote}"
            )
        print("Email sent successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")
