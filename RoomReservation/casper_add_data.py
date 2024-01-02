import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Retrieve a list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print the table names
for table in tables:
    print(table[0])

# Prepare SQL query to INSERT a record into the database.
query = """
INSERT INTO room_room (id, name, description, capacity, size, location, price_per_hour, image, created_at, updated_at, created_by_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""
data = (0, 401, "None", 10, 36.0, "NSYSU Library", 10, 0, 0, 0, 666)  # Replace with the actual data values

# Execute the SQL command
cursor.execute(query, data)

# Commit your changes in the database
conn.commit()

# Close the database connection
conn.close()

import sqlite3





