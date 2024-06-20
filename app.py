from db import init_db

if init_db():
    print("Database initialized.")
else:
    print("Something was wrong in database initialization.")
