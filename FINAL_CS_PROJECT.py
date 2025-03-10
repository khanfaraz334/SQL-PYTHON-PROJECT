import mysql.connector    
import random
import string
from tabulate import tabulate
import csv
import pickle

# Establish connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="plantstore"
)
cursor = connection.cursor()

# Write a welcome message to 'welcome.txt' file
with open("welcome.txt", "w") as welcome_file:
    welcome_file.write("Welcome to Flora-Flow! Your go-to plant store.")

# Function to check if the user exists in the database
def user_exists(username, user_id=None):
    if user_id:
        cursor.execute("SELECT * FROM users WHERE username = %s AND user_id = %s", (username, user_id))
    else:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone()

# Function to log activities in binary format to 'activity_log.bin'
def log_activity_binary(activity):
    with open("activity_log.bin", "ab") as f:
        pickle.dump(activity, f)

# Function to sign up a new user and automatically assign the 'customer' role
def sign_up():
    print("\n--- Creating Account ---\n")
    username = input("Enter a new username: ")
    user_id = input("Enter your user_id: ")  # Ask for user_id during sign-up
    if user_exists(username, user_id):
        print("Username and user_id combination already exists! Please choose a different username or user_id.")
        return None, None, None  # Return None for both username, user_id, and role if account exists
    
    password = input("Enter a new password: ")

    # Insert the new user with role set to "customer"
    cursor.execute("INSERT INTO users (user_id, username, password, role) VALUES (%s, %s, %s, %s)", 
                   (user_id, username, password, "customer"))
    connection.commit()
    
    # Log the account creation activity
    log_activity_binary(f"New account created for username: {username} with role 'customer' and user_id {user_id}")
    print("Account created successfully!")

    # Update user details in CSV file
    update_users_csv()  # This will save the latest user details

    return username, user_id, "customer"  # Return both the username, user_id, and 'customer' role


# Function to export user details to a CSV file
def update_users_csv():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    with open("users.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User_ID", "Username", "Password", "Role"])  # Define the headers
        writer.writerows(users)
    print("User details saved in users.csv.")

# Function to log in an existing user
def log_in():
    print("\n--- Logging In ---\n")
    username = input("Enter your username: ")
    user_id = input("Enter your user_id: ")  # Ask for user_id during log-in
    password = input("Enter your password: ")
    if user_exists(username, user_id):
        cursor.execute("SELECT * FROM users WHERE username = %s AND user_id = %s AND password = %s", 
                       (username, user_id, password))
        user = cursor.fetchone()
        if user:
            print("Login successful!")
            log_activity_binary(f"User {username} logged in with user_id {user_id}.")
            return username, user_id, user[3]  # Return the username, user_id, and role (role is in the 4th column)
        else:
            print("Invalid credentials. Please try again.")
            return None, None, None
    else:
        print("Invalid credentials. Please try again.")
        return None, None, None
# Function to fetch and display available plants
def show_plants():
    print("\n--- Available Plants ---\n")
    cursor.execute("SELECT * FROM plants")
    plants = cursor.fetchall()
    if plants:
        headers = ["Plant_ID", "Plant_Name", "Flower_Color", "Lifespan", "Plant_Type", "Bloom_Time", "Avg_Plant_Height_cm", "Leaf_Type", "Price_INR"]
        print(tabulate(plants, headers=headers, tablefmt="grid"))
    else:
        print("No plants available in the database.")

# Function to update plant information
def update_plant():
    plant_id = int(input("\nEnter the Plant ID to update: "))
    column = input("Enter the column to update (e.g., Price_INR): ")
    new_value = input("Enter the new value: ")
    cursor.execute(f"UPDATE plants SET {column} = %s WHERE Plant_ID = %s", (new_value, plant_id))
    connection.commit()
    print("Plant information updated successfully!")
    update_plants_csv()
    log_activity_binary(f"Plant ID {plant_id} updated. Changed {column} to {new_value}.")

# Function to delete a plant
def delete_plant():
    plant_id = int(input("\nEnter the Plant ID to delete: "))
    cursor.execute("DELETE FROM plants WHERE Plant_ID = %s", (plant_id,))
    connection.commit()
    print("Plant deleted successfully!")
    update_plants_csv()
    log_activity_binary(f"Plant ID {plant_id} deleted.")

# Function to add a new plant
def add_plant():
    print("\n--- Add New Plant ---\n")
    
    # Get details of the new plant from the user
    plant_name = input("Enter Plant Name: ")
    flower_color = input("Enter Flower Color: ")
    lifespan = input("Enter Lifespan (e.g., Perennial, Annual): ")
    plant_type = input("Enter Plant Type (e.g., Herb, Shrub, Tree): ")
    bloom_time = input("Enter Bloom Time (e.g., Spring, Summer, Fall): ")
    avg_height = input("Enter Average Plant Height (in cm): ")
    leaf_type = input("Enter Leaf Type (e.g., Evergreen, Deciduous): ")
    price_inr = input("Enter Price (in INR): ")

    # Fetch all existing Plant_IDs
    cursor.execute("SELECT Plant_ID FROM plants ORDER BY Plant_ID ASC")
    plant_ids = cursor.fetchall()
    plant_ids = [plant[0] for plant in plant_ids]

    # Identify gaps in Plant_ID sequence and reuse the first available missing ID
    missing_plant_ids = [i for i in range(1, len(plant_ids) + 2) if i not in plant_ids]
    new_plant_id = missing_plant_ids[0] if missing_plant_ids else plant_ids[-1] + 1

    # Insert the new plant into the database with the determined Plant_ID
    cursor.execute(""" 
        INSERT INTO plants (Plant_ID, Plant_Name, Flower_Color, Lifespan, Plant_Type, Bloom_Time, 
                            Avg_Plant_Height_cm, Leaf_Type, Price_INR)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (new_plant_id, plant_name, flower_color, lifespan, plant_type, bloom_time, avg_height, leaf_type, price_inr))
    
    connection.commit()
    print("New plant added successfully!")
    update_plants_csv()
    log_activity_binary(f"New plant added: {plant_name}, {plant_type}, {price_inr} INR.")

# Function to place an order
def place_order(username):
    print("\n--- Buying Plants ---\n")
    show_plants()
    plant_id = int(input("Enter the Plant ID you want to purchase: "))
    cursor.execute("SELECT Price_INR FROM plants WHERE Plant_ID = %s", (plant_id,))
    result = cursor.fetchone()
    if result:
        price = result[0]
        quantity = int(input("Enter the quantity: "))
        total_price = price * quantity
        print(f"\nTotal Price: {total_price} INR\n")
    else:
        print("Invalid Plant ID.")
        return
    
    transaction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    payment_mode = input("\nEnter payment mode (e.g., Credit Card, Cash): ")
    delivery_address = input("Enter your delivery address: ")

    # Fetch all existing order_id values and find gaps
    cursor.execute("SELECT order_id FROM orders ORDER BY order_id ASC")
    order_ids = [order[0] for order in cursor.fetchall()]
    
    # Find the first missing order_id in the sequence for the new order_id
    missing_order_ids = [i for i in range(1, len(order_ids) + 2) if i not in order_ids]
    new_order_id = missing_order_ids[0] if missing_order_ids else (order_ids[-1] + 1 if order_ids else 1)

    # Insert the new order into the orders table with the new_order_id
    cursor.execute(""" 
        INSERT INTO orders (order_id, username, transaction_id, total_price, payment_mode, delivery_address, order_date)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """, (new_order_id, username, transaction_id, total_price, payment_mode, delivery_address))
    connection.commit()

    print("Order placed successfully! Thank you for shopping with Flora-Flow!")
    log_activity_binary(f"Order placed by {username} with order_id: {new_order_id}, Transaction ID: {transaction_id}, Total Price: {total_price}")

    # Save the order details to orders.csv (only once)
    update_orders_csv()
    print("Order details saved successfully in orders.csv.")  # Only one print message here

# Function to export plant details to a CSV file
def update_plants_csv():
    cursor.execute("SELECT * FROM plants")
    plants = cursor.fetchall()
    with open("plants.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Plant_ID", "Plant_Name", "Flower_Color", "Lifespan", "Plant_Type", "Bloom_Time", "Avg_Plant_Height_cm", "Leaf_Type", "Price_INR"])
        writer.writerows(plants)
    print("Plant details saved in plants.csv.")
    
# Function to update orders.csv
def update_orders_csv():
    # Logic to update orders.csv
    with open('orders.csv', 'w', newline='') as csvfile:
        fieldnames = ['order_id', 'username', 'transaction_id', 'total_price', 'payment_mode', 'delivery_address', 'order_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Fetch rows from the database
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        
        # Write each row as a dictionary matching fieldnames
        for row in rows:
            # Creating a dictionary from the row tuple
            row_dict = dict(zip(fieldnames, row))
            writer.writerow(row_dict)


# Main program flow
username = None
user_id = None
role = None

while True:
    if username is None:
        print("\n--- Main Menu ---")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            username, user_id, role = sign_up()  # Get username, user_id, and role after sign-up
            if username and user_id and role:
                print("\n--- Customer Menu ---")  # Automatically show the customer menu after sign-up
                print("1. Show Plants")
                print("2. Place Order")
                print("3. Log Out")
                choice = input("Select an option: ")
                if choice == "1":
                    show_plants()
                elif choice == "2":
                    place_order(username)
                elif choice == "3":
                    print("Logging out...")
                    username = None
                    user_id = None
                    role = None
                else:
                    print("Invalid option! Please try again.")
        elif choice == "2":
            username, user_id, role = log_in()  # Log in with username, user_id, and password
        elif choice == "3":
            print("Thanks for visiting Flora-Flow! Visit Again!")
            break
        else:
            print("Invalid option! Please try again.")
    else:
        if role == "admin":
            print("\n--- Admin Menu ---")
            print("1. Show Plants")
            print("2. Add Plant")
            print("3. Update Plant")
            print("4. Delete Plant")
            print("5. View Orders")
            print("6. Log Out")
            choice = input("Select an option: ")
            if choice == "1":
                show_plants()
            elif choice == "2":
                add_plant()
            elif choice == "3":
                update_plant()
            elif choice == "4":
                delete_plant()
            elif choice == "5":
                cursor.execute("SELECT * FROM orders")
                orders = cursor.fetchall()
                print(tabulate(orders, headers=["Order_ID", "Username", "Transaction_ID", "Total_Price", "Payment_Mode", "Delivery_Address", "Order_Date"], tablefmt="grid"))
            elif choice == "6":
                print("Logging out...")
                username = None
                user_id = None
                role = None
            else:
                print("Invalid option! Please try again.")
        elif role == "customer":
            print("\n--- Customer Menu ---")
            print("1. Show Plants")
            print("2. Place Order")
            print("3. Log Out")
            choice = input("Select an option: ")
            if choice == "1":
                show_plants()
            elif choice == "2":
                place_order(username)
            elif choice == "3":
                print("Logging out...")
                username = None
                user_id = None
                role = None
            else:
                print("Invalid option! Please try again.")
