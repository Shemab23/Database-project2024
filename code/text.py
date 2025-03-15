from database import retrieve_application

rows = retrieve_application()

for row in rows:
    print(row)