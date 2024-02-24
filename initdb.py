import sqlite3
import os

# Create a new database

if os.path.exists('app.db'):
    os.remove('app.db')
    print("\t---> Old database removed")

conn = sqlite3.connect('app.db')

# Create a new table
conn.execute(f'''
    CREATE TABLE users
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL);
''')


# Add default test user
conn.execute(f'''
    INSERT INTO users (username, password)
    VALUES ('test', 'test');
''')

# Commit the changes
conn.commit()

# Close the connection

conn.close()

print("\t---> New database created successfully")