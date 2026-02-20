import mysql.connector

# DATABASE CONNECTION
DB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",   # <-- Change if needed
    database="book_store"
)

C = DB.cursor()

# ================= ADMIN FUNCTIONS ================= #

def ADD():
    book = input("Enter Book Name: ")
    genre = input("Genre: ")
    quantity = int(input("Enter quantity: "))
    author = input("Enter author name: ")
    publication = input("Enter publication house: ")
    price = int(input("Enter the price: "))

    C.execute("INSERT INTO available_books VALUES (%s,%s,%s,%s,%s,%s)",
              (book, genre, quantity, author, publication, price))
    DB.commit()

    print("++++ SUCCESSFULLY ADDED ++++")

    n = int(input("1. Continue\n2. Back\nEnter: "))
    if n == 1:
        ADD()
    else:
        Staff()


def NewStaff():
    fname = input("Enter Fullname: ")
    gender = input("Gender(M/F/O): ")
    age = int(input("Age: "))
    phno = input("Staff phone no.: ")
    add = input("Address: ")

    C.execute("INSERT INTO staff_details VALUES (%s,%s,%s,%s,%s)",
              (fname, gender, age, phno, add))
    DB.commit()

    print("++++ STAFF SUCCESSFULLY ADDED ++++")

    n = int(input("1. Continue\n2. Back\nEnter: "))
    if n == 1:
        NewStaff()
    else:
        Staff()


def RemoveStaff():
    name = input("Staff Name to Remove: ")

    C.execute("DELETE FROM staff_details WHERE Name=%s", (name,))
    DB.commit()

    print("Staff Removed")

    n = int(input("1. Continue\n2. Back\nEnter: "))
    if n == 1:
        RemoveStaff()
    else:
        Staff()


def StaffDetail():
    C.execute("SELECT * FROM staff_details")
    data = C.fetchall()

    for x in data:
        print("Name:", x[0])
        print("Gender:", x[1])
        print("Age:", x[2])
        print("Phone:", x[3])
        print("Address:", x[4])
        print("-----------------------------")

    input("Press Enter to go back...")
    Staff()


def AvailableBooks():
    C.execute("SELECT * FROM available_books")
    data = C.fetchall()

    for x in data:
        print("Book:", x[0])
        print("Genre:", x[1])
        print("Quantity:", x[2])
        print("Author:", x[3])
        print("Publication:", x[4])
        print("Price:", x[5])
        print("-----------------------------")

    input("Press Enter to go back...")
    Staff()


def SellRec():
    C.execute("SELECT * FROM sell_rec")
    data = C.fetchall()

    for x in data:
        print("Customer:", x[0])
        print("Phone:", x[1])
        print("Book:", x[2])
        print("Quantity:", x[3])
        print("Price:", x[4])
        print("-----------------------------")

    input("Press Enter to go back...")
    Staff()


def TotalIncome():
    C.execute("SELECT SUM(price) FROM sell_rec")
    total = C.fetchone()
    print("Total Income:", total[0])

    input("Press Enter to go back...")
    Staff()


# ================= BUYER FUNCTIONS ================= #

def Purchase():
    C.execute("SELECT * FROM available_books")
    books = C.fetchall()

    for x in books:
        print(x)

    cusname = input("Enter customer name: ")
    phno = input("Enter phone number: ")
    book = input("Enter Book Name: ")
    quantity = int(input("Enter quantity: "))

    C.execute("SELECT quantity, price FROM available_books WHERE bookname=%s", (book,))
    result = C.fetchone()

    if result is None:
        print("Book not available!")
        Buyer()
        return

    available_qty, price = result

    if available_qty < quantity:
        print("Not enough stock!")
        Buyer()
        return

    total_price = price * quantity

    C.execute("INSERT INTO sell_rec VALUES (%s,%s,%s,%s,%s)",
              (cusname, phno, book, quantity, total_price))

    C.execute("UPDATE available_books SET quantity=quantity-%s WHERE bookname=%s",
              (quantity, book))

    DB.commit()

    print("++++ BOOK SOLD SUCCESSFULLY ++++")
    Buyer()


def Buyer():
    print("""
1. Purchase Book
2. Available Books
3. Exit
""")

    choice = int(input("Enter choice: "))

    if choice == 1:
        Purchase()
    elif choice == 2:
        C.execute("SELECT * FROM available_books")
        for x in C.fetchall():
            print(x)
        Buyer()
    else:
        return


# ================= STAFF MENU ================= #

def Staff():
    print("""
1. Add Books
2. Add Staff
3. Remove Staff
4. View Staff
5. Sell Record
6. Total Income
7. View Available Books
8. Exit
""")

    choice = int(input("Enter choice: "))

    if choice == 1:
        ADD()
    elif choice == 2:
        NewStaff()
    elif choice == 3:
        RemoveStaff()
    elif choice == 4:
        StaffDetail()
    elif choice == 5:
        SellRec()
    elif choice == 6:
        TotalIncome()
    elif choice == 7:
        AvailableBooks()
    else:
        return


# ================= MAIN PROGRAM ================= #

print("******** WELCOME TO BOOK STORE ********")

while True:
    print("""
1. Employee
2. User
3. Exit
""")

    main_choice = int(input("Enter choice: "))

    if main_choice == 1:
        Staff()
    elif main_choice == 2:
        Buyer()
    else:
        break