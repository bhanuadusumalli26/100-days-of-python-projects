
import pandas
data=pandas.read_csv("C:\\100days_python\\day25.py\\2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
grey_squirrels_count=len(data[data["Primary Fur Color"]=="Gray"])
red_squirrels_count=len(data[data["Primary Fur Color"]=="Cinnamon"])
black_squirrels_count=len(data[data["Primary Fur Color"]=="Black"])
print(grey_squirrels_count)
print(red_squirrels_count)
print(black_squirrels_count)
data_dic={
    "Fur Color":["Gray","Cinnamon","Black"],
    "Count":[grey_squirrels_count,red_squirrels_count,black_squirrels_count]
}
df=pandas.DataFrame(data_dic)
df.to_csv("squirrel_count.csv")