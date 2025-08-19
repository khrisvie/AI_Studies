import csv

def add_entry():
    with open("data.csv", mode="a", newline="") as data_csv:
        fieldnames = ["Date","Category","Description","Amount"]
        writer = csv.DictWriter(data_csv, fieldnames=fieldnames)

        date = input("Enter date: ")
        category = input("Enter category: ")
        description = input("Enter description: ")
        amount = input("Enter amount: ")

        writer.writerow({"Date": date,
                         "Category": category,
                         "Description": description,
                         "Amount": amount})
    print("Added!")

add_entry()