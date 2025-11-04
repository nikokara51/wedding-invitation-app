import sqlite3

conn = sqlite3.connect("invites.db")
cursor = conn.cursor()

# All responses
cursor.execute("SELECT name, rsvp FROM guests")
for name, rsvp in cursor.fetchall():
    print(name, rsvp)

# Only YES
cursor.execute("SELECT name FROM guests WHERE rsvp='yes'")
print("Attending:")
for (name,) in cursor.fetchall():
    print(name)

# Only NO
cursor.execute("SELECT name FROM guests WHERE rsvp='no'")
print("Not attending:")
for (name,) in cursor.fetchall():
    print(name)

conn.close()
