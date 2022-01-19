import sqlite3
import random

# Create an object for the required database
database = sqlite3.connect("college_rooms.db")

# Create a cursor object, used to make changes to the database
cur = database.cursor()

# A function to create a table, skip if it already exists
def CreateTable(command):
    try:
        global cur
        cur.execute(command)
        print("Table created successfully")
    except Exception as err:
        pass

# A function to check if a room is available
# Returns 0 if the room is not available, 1 if it is available
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

# A function to add a new room to the database
# Requires the location and the type of room
def AddEntry(Location, Type):
    global cur
    command = "INSERT INTO rooms VALUES (" + Location + ", 1, " + Type + ")"
    print(command)
    cur.execute(command)

# Function to initialize the database with values for all classrooms
# Requires the number of buildings, floors and rooms
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
# Returns the location of the chosen room if successful, else if all rooms of the required type are booked, returns -1
def BookRoom(Building, RoomType, StartTime, Duration):
    try:
        global cur
        
        # Select a random available room of the requested type in a particular building
        roomSelectionCommand = "SELECT Location from rooms WHERE Type = '" + RoomType + "' AND Availability = 1 AND Location LIKE 'B" + str(Building) + "%'"
        availableRooms = cur.execute(roomSelectionCommand).fetchall()
        assignedRoom = random.choice(availableRooms) [0]

        # Execute the commands to insert booking information into both the tables
        command = "INSERT INTO timetable VALUES ('" + assignedRoom + "', '" + StartTime + "', '" + Duration + "')"
        notavailable = "UPDATE rooms SET Availability = 0 WHERE Location = '" + assignedRoom + "'"
        cur.execute(command)
        cur.execute(notavailable)
        return assignedRoom
    except Exception as err:
        print("No more rooms of the selected type in the selected building are are available!")
        return -1

# A function to return all available rooms of a particular type
# Returns available rooms as a list, -1 if there are no available rooms
def AvailableRooms(RoomType):
    try:
        global cur
        roomSelectionCommand = "SELECT Location from rooms WHERE Type = '" + RoomType + "' AND Availability = 1"
        availableRoomsString = cur.execute(roomSelectionCommand).fetchall()
        availableRooms = []
        for i in range(0, len(availableRoomsString)):
            availableRooms.append (availableRoomsString[i][0])
        
        # Check if the list is empty, i.e. no available rooms
        if len(availableRooms) == 0:
            return -1
        else:
            return availableRooms
    except:
        pass

# Create the table which will store information about rooms
# This table contains the room's location, its availability status and the type (i.e. capacity)
CreateTable("CREATE TABLE rooms (Location varchar(10) PRIMARY KEY, Availability int, Type varchar(20))")

# Create the table which will store the list of booked rooms and their timings
CreateTable("CREATE TABLE timetable (Location varchar(10) PRIMARY KEY, Initiation_Time smalldatetime, Duration time, FOREIGN KEY (Location) REFERENCES rooms(Location))")

# Initialzing the database with all available classrooms in the campus
# The first argument is the number of buildings, the second is the number of floors on each building and third is the number of rooms on each floor
# The type of each room is assigned randomly, but would be filled out manually in a real-life scenario
InitDatabase(4, 3, 4)

print(BookRoom("2", "Classroom", "2022-01-14 12:00:00", "01:00:00"))
print(AvailableRooms("Classroom"))

database.commit()