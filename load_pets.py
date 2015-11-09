import sqlite3

__author__ = "Patrick Abejar"

'''This script connects to a database file, pets.db, and then stores pet and
person information as stated in the assignment. The second part asks for the
user for an ID, where information will be queried back into the database to
receive information regarding the person with the associated ID number and
their associated pets.
'''


def main():

    # Connect to the database pets.db as per the assignment requirements
    conn = sqlite3.connect("pets.db")
    c = conn.cursor()

    # These three execute statements will remove tables if they exist. Without
    # these three statements, create table executions below will not operate
    # well if the tables exist.
    c.execute('''DROP TABLE IF EXISTS person''')
    c.execute('''DROP TABLE IF EXISTS pet''')
    c.execute('''DROP TABLE IF EXISTS person_pet''')

    # The next six execute statements were data retrieved from the assignment.
    c.execute('''CREATE TABLE person (
                     id INTEGER PRIMARY KEY,
                     first_name TEXT,
                     last_name TEXT,
                     age INTEGER )
              ''')
    c.execute('''CREATE TABLE pet (
                     id INTEGER PRIMARY KEY,
                     name TEXT,
                     breed TEXT,
                     age INTEGER,
                     dead INTEGER );
              ''')
    c.execute('''CREATE TABLE person_pet (
                     person_id INTEGER,
                     pet_id INTEGER );
              ''')
    c.execute('''INSERT INTO person
                     (id, first_name, last_name, age)
                 VALUES
                     (1, "James", "Smith", 41),
                     (2, "Diana", "Greene", 23),
                     (3, "Sara", "White", 27),
                     (4, "William", "Gibson", 23)
              ''')
    c.execute('''INSERT INTO pet
                     (id, name, breed, age, dead)
                 VALUES
                     (1, "Rusty", "Dalmation", 4, 1),
                     (2, "Bella", "Alaskan Malamute", 3, 0),
                     (3, "Max", "Cocker Spaniel", 1, 0),
                     (4, "Rocky", "Beagle", 7, 0),
                     (5, "Rufus", "Cocker Spaniel", 1, 0),
                     (6, "Spot", "Bloodhound", 2, 1)
              ''')

    # QUESTION: What is the purpose of the person_pet table?
    # ANSWER: This table illustrates the owner-pet relationship between
    # person and pets. This is applicable for a one-to-many relationship
    # as the owner to pet relationship is. This allows the future joins
    # on the data of the person and pet tables to be established in the
    # code following. A relational table such as this below also allows
    # for easy changes and deletions to be made to relations without
    # needing to modify person or pet entries in the person and pet
    # tables.
    c.execute('''INSERT INTO person_pet
                     (person_id, pet_id)
                 VALUES
                     (1, 1),
                     (1, 2),
                     (2, 3),
                     (2, 4),
                     (3, 5),
                     (4, 6)
              ''')

    # Commits all database changes to the database
    conn.commit()

    # This variable will keep track of what person_id is inputted at the
    # current moment.
    person_id = 0

    # Keep executing ID number information retrieval as well as database
    # information fetching until user enters -1 where the exit() will occur.
    while person_id != -1:
        try:
            # Stores ID number requested in person_id
            person_id = int(raw_input("\nPlease enter an ID number: "))

            # Searches for the requested person_id
            c.execute('''SELECT first_name, last_name, age FROM person WHERE
             id = %i''' % person_id)

            # Retrieves ands separates the information obtained from the
            # SELECT statement for printing on the last line.
            person_data = c.fetchone()
            person_name = "%s %s" % (person_data[0], person_data[1])
            person_age = person_data[2]
            print " %s, %i years old" % (person_name, person_age)

            # Execute statements that will retrieve all information on pets.
            # Two left joins are done to merge pets and persons table via
            # the person_pet table. Joins were done on equivalent id num-
            # bers of the pets on both pet and person_pet data. The same was
            # done for ids on person and person_pet table with regard to
            # person_id in person_pet this time. The left joins form one
            # table with one row representing one pet and then lists the
            # owners name beside that information. The SELECT statement
            # chose to return the persons' first and last name along with
            # all the pet information. The WHERE clause below filters the
            # pets associated with the person_id inputted by the user and
            # leaves out the remainder of the pets.
            c.execute('''SELECT person.first_name, person.last_name, pet.name,
                          pet.breed, pet.age, pet.dead
                         FROM pet
                         LEFT JOIN person_pet
                         ON pet.id = person_pet.pet_id
                         LEFT JOIN person
                         ON person_pet.person_id = person.id
                         WHERE person.id = %i
                      ''' % person_id)

            # Retrieves all rows representing one pet and stores it in a list
            # of lists, where the first dimension represents one pet presently
            # or formerly owned by the person in person_id.
            pet_list = c.fetchall()

            # Repeats the procedure for all rows (representing all pets)
            for pet in pet_list:

                # Store the information retrieved by the SELECT statement. The
                # columns shown are numbered as follows (identical to the
                # SELECT clause executed above:
                # 0 --> Person's First Name
                # 1 --> Person's Last Name
                # 2 --> Pet's Name
                # 3 --> Pet's Breed
                # 4 --> Pet's Age
                # 5 --> 0 represents the pet is alive; 1 represents a dead pet
                pet_name = pet[2]
                pet_breed = pet[3]
                pet_age = pet[4]
                pet_dead = pet[5]

                # Different grammar is required whether a pet or not is alive.
                # Otherwise all information with regards to the pet is print-
                # ed below in both cases of death or living.
                if pet_dead == 0:
                    print " %s owns %s, a %s, that is %s" % \
                          (person_name, pet_name, pet_breed, pet_age)
                elif pet_dead == 1:
                    print " %s owned %s, a %s, that was %s" % \
                          (person_name, pet_name, pet_breed, pet_age)

        # In the event the user enters an integer that cannot be processed
        # without raising an exception in int().
        except ValueError:
            print " Enter only integers."

        # In the event there is no corresponding person_id in the person
        # table established above.
        except TypeError:

            # An input of -1 will exit the program as per the assignment
            # requirements. Closes the connection to database.
            if person_id == -1:
                conn.close()
                print " Now exiting program."
                exit(-1)
            print " There is no data associated with that ID number."

if __name__ == "__main__":
    main()
