# Plant Management System

## Overview

The Plant Management System is a comprehensive application that enables users to manage a plant store efficiently. The system provides functionalities for plant inventory management, user authentication, order processing, and data tracking. Built with Python and MySQL, it ensures seamless interactions for both customers and administrators.

## Features

## 1. User Authentication & Roles

- Users can sign up and log in with unique credentials.

- Two user roles:

  - Admin: Can manage plant inventory and view orders.

  - Customer: Can browse available plants and place orders.

## 2. Plant Inventory Management (Admin)

- Add New Plants: Input details like name, flower color, lifespan, plant type, bloom time, height, leaf type, and price.

- Update Plant Details: Modify specific attributes such as price or bloom time.

- Delete Plants: Remove plants from the inventory.

- View Available Plants: Display all plants in a structured table format.

## 3. Order Processing (Customer)

- Place Orders: Select plants, specify quantity, and confirm payment mode.

- Generate Unique Transaction IDs for order tracking.

- Automatic ID Assignment for seamless order management.

- Order Data Logging in a MySQL database and CSV file.

## 4. Data Storage & Logging

- MySQL Database Integration:

  - plants table stores plant details.

  - users table manages user accounts.

  - orders table logs customer purchases.

- CSV & Binary File Logging:

  - users.csv stores registered users.

  - plants.csv maintains plant inventory.

  - orders.csv logs all customer purchases.

  - activity_log.bin records system actions.

## Technologies Used

- Programming Language: Python

- Database: MySQL

- Libraries:

  - mysql-connector-python (MySQL connectivity)

  - tabulate (Formatted table display)

  - csv (Data export)

  - pickle (Binary file logging)

## Installation & Setup

### Prerequisites

Ensure the following software is installed:

  - Python 3.10+

  - MySQL Server & MySQL Workbench

  - Required Python libraries:

      #### pip install mysql-connector-python tabulate

### Database Setup

#### 1. Create the database:

CREATE DATABASE plantstore;
USE plantstore;

#### 2. Create tables:

CREATE TABLE plants (
  Plant_ID INT AUTO_INCREMENT PRIMARY KEY,
  Plant_Name VARCHAR(50),
  Flower_Color VARCHAR(50),
  Lifespan VARCHAR(50),
  Plant_Type VARCHAR(50),
  Bloom_Time VARCHAR(50),
  Avg_Plant_Height_cm INT,
  Leaf_Type VARCHAR(50),
  Price_INR INT
);

CREATE TABLE users (
  user_id VARCHAR(255) PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(255) NOT NULL,
  role VARCHAR(10) DEFAULT 'customer'
);

CREATE TABLE orders (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL,
  transaction_id VARCHAR(50) UNIQUE NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  pay_mode ENUM('Cash', 'Credit Card', 'Debit Card', 'Online') NOT NULL,
  address TEXT NOT NULL,
  order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (username) REFERENCES users(username)
);

## Running the Application

#### 1. Clone the repository:

git clone [https://github.com/khanfaraz334/plant-management-system](https://github.com/khanfaraz334/SQL-PYTHON-PROJECT).git
cd SQL-PYTHON-PROJECT

#### 2. Run the script:

python FINAL_CS_PROJECT.py

## Usage

## User Flow

1. New users must sign up before logging in.

2. Admins can manage plant data, while customers can browse plants and place orders.

3. Orders are stored in the database and logged in orders.csv.

4. Admins can view and manage all orders.

## Example Admin Actions

### - Adding a plant:

Enter Plant Name: Aloe Vera
Enter Flower Color: Yellow
Enter Lifespan: Perennial
Enter Plant Type: Herb
Enter Bloom Time: Summer
Enter Average Plant Height (in cm): 60
Enter Leaf Type: Evergreen
Enter Price (in INR): 200

### - Updating plant details:

Enter the Plant ID to update: 3
Enter the column to update: Price_INR
Enter the new value: 250

### - Deleting a plant:

Enter the Plant ID to delete: 5

## Example Customer Actions

### - Placing an order:

Enter the Plant ID you want to purchase: 2
Enter the quantity: 3
Enter payment mode (Credit Card, Cash): Online
Enter your delivery address: 123 Green Street, City

(Order details saved in orders.csv)

## Screenshots

Below are some screenshots demonstrating key functionalities of the system:

1. **Welcome Screen** - Displays a greeting message when the program starts.
                    ![image](https://github.com/user-attachments/assets/2af94bda-21c7-4ec6-941f-b6be98598534)

2. **Login & Sign-up Screens** - Allows users to authenticate and create new accounts.
                    ![image](https://github.com/user-attachments/assets/97fe248c-cf04-4bf0-8568-c2bca313001b)

3. **Admin Panel** - Shows options to manage plants and view orders.
                    ![image](https://github.com/user-attachments/assets/89cc8745-83af-4934-b351-9508fd314d35)

4. **Customer Panel** - Enables customers to view available plants and place orders.
                    ![image](https://github.com/user-attachments/assets/4f7a72d3-a24e-46a9-89cb-8bf458985661)

5. **Order Placement** - Displays order confirmation with transaction ID.
                    ![image](https://github.com/user-attachments/assets/0fb1ee16-fd21-4629-80f2-ab9ef83cc5e7)
                    ![image](https://github.com/user-attachments/assets/41a1102f-bc5b-4138-ac7c-f5b8569324d0)
                    ![image](https://github.com/user-attachments/assets/bde76bb3-e76c-4969-a73c-84fc96dc6382)

6. **Database Table Views** - Screenshots of MySQL tables (plants, users, orders).
                    ![image](https://github.com/user-attachments/assets/68750802-0746-4585-afdc-0e08fab074b2)
                    ![image](https://github.com/user-attachments/assets/bf142978-c86c-459e-b0ab-1293a37598a3)
                    ![image](https://github.com/user-attachments/assets/78942451-0f5b-4471-8e2e-7edd8c36195a)

7. **CSV File Logs** - Demonstrates successful storage of users, plants, and orders in CSV files.
                    ![image](https://github.com/user-attachments/assets/b1b588c2-8ca9-430f-b86c-e3dabb1a5a9e)
                    ![image](https://github.com/user-attachments/assets/b2333edd-c982-4841-bb28-91fb0c370c5a)
                    ![image](https://github.com/user-attachments/assets/20480cbd-4f03-40be-a5bc-7a82d61981f0)

## Future Enhancements

- GUI Development: Integrate a web or desktop UI.

- Online Payments: Implement real-time payment processing.

- Email Notifications: Send order confirmations via email.

- Advanced Analytics: Generate sales reports and inventory insights.

## Contributors

- Faraz Khan – [My GitHub](https://github.com/khanfaraz334/)

