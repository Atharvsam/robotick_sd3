import sqlite3
import random

# Create an object for the required database
database = sqlite3.connect("college_rooms.db")

# Create a cursor object, used to make changes to the database
cur = database.cursor()

# A function to create a table, pass if it already exists
def CreateTable(command):
    try:
        global cur
        cur.execute(command)
        print("Table created successfully")
    except Exception as err:
        pass

# A function to check if a room is available
def CheckAvailability(roomId):
    try:
        global cur
        command = "SELECT Availability FROM rooms WHERE Location = " + roomId
        # print(command)
        availabilityStatus = cur.execute(command).fetchone() [0]
        return availabilityStatus
    except TypeError as err:
        # print(err)
        print("The requested room does not exist in the database.")

# A function to add a new entry to both the tables
def AddEntry(Location, Type):
    global cur
    command = "INSERT INTO rooms VALUES (" + Location + ", 1, " + Type + ")"
    print(command)
    cur.execute(command)

# Function to initialize the database with values for all classrooms
def InitDatabase(Buildings, Floors, Rooms):
    try:
        global cur
        roomTypeArray = ["'Classroom'", "'Seminar Hall'", "'Lab'"]
        for i in range(0, Buildings):
            for j in range(0, Floors):
                for k in range(0, Rooms):
                    roomType = random.choice(roomTypeArray)
                    command = "INSERT INTO rooms VALUES (" + "'B" + str(i+1) + "F" + str(j+1) + "R" + str(k+1) + "', " + "1, " + roomType + ")"
                    cur.execute(command)
    except Exception as err:
        pass
                
# A function which allows the user to book a particular room at a certain date / time for a particular duration
def BookRoom(Building, RoomType, StartTime, Duration):
    try:
        global cur
        
        # Select a random available room of the requested type
        roomSelectionCommand = "SELECT Location from rooms WHERE Type = " + RoomType + " AND Availability = 1"
        availableRooms = cur.execute(roomSelectionCommand).fetchall()
        assignedRoom = random.choice(availableRooms) [0]

        # Execute the commands to insert booking information into both the tables
        command = "INSERT INTO timetable VALUES ('" + assignedRoom + "', " + StartTime + ", " + Duration + ")"
        notavailable = "UPDATE rooms SET Availability = 0 WHERE Location = '" + assignedRoom + "'"
        cur.execute(command)
        cur.execute(notavailable)
        return assignedRoom
    except Exception as err:
        print("No more rooms of the seleccted type are are available!")
        return -1


# Create the table which will store information about rooms.
# This table contains the room's location, its availability status and the type (i.e. capacity)
CreateTable("CREATE TABLE rooms (Location varchar(10) PRIMARY KEY, Availability int, Type varchar(20))")
CreateTable("CREATE TABLE timetable (Location varchar(10) PRIMARY KEY, Initiation_Time smalldatetime, Duration time, FOREIGN KEY (Location) REFERENCES rooms(Location))")

InitDatabase(6, 5, 10)

print(BookRoom("1", "'Classroom'", "'2022-01-14 12:00:00'", "'01:00:00'"))

database.commit()