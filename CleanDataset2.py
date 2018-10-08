sections = ["Language", "Reading","Applied Math", "Math Compu"]

#Helper functions are stored in cleaner.py and should be in the same folder as this file is.
import cleaner
import individual

#Specify the name of the file to read.
FILE = open("20180913_SUBTEST(1).txt", "r")

#####################
#Main data structure#
#####################

#Array of all Names (will be keys in the table dictionary)
list_names = []

#This is Just a reference to the elements each dictionary will have but NEVER USE it.
section = {
    "Number": [],
    "Answers": [], #Answer that the test taker responded.
    "isCorrect": []
    }

#This is Just a reference to the elements each dictionary will have but NEVER USE it.
info = {
        "Name": "",
        "Group Name": "",
        "ID": "",
        "Test Date": "",
        "Run Date": "",
        "Group": "",
        "Reading": section,
        "Math Compu": section,
        "Applied Math": section,
        "Language": section
    }

#Full form. Each new name will be a key.
table = dict()

#Array of all lines.
lines = []

length_FILE = 0

#Get file into an array of arrays.
for line in FILE:
    lines.append(line.split())
    length_FILE = length_FILE + 1

#Know if we have a new person or we can edit one.
new_person = False

#Initialize data structure.
for line in lines:
    if cleaner.start_name_section(line):
         Name = cleaner.get_name(line)

         if Name not in list_names:
             table[Name] = {}

             for s in sections:
                 table[Name][s] = {
                                   "Number": [],
                                   "Answers": [], #Answer that the test taker responded.
                                   "isCorrect": []
                                   }

#Get all Names and other info in the first iteration.
# Each element in line contains an array from the words in the file.
for i in range(len(lines)):
    line = lines[i]

    # Check if the line contains a Name.
    if cleaner.start_name_section(line):

        # Get Full Name
        Name = cleaner.get_name(line)

        # If currently we are in a new person.
        if Name not in list_names:
            list_names.append(Name)
            key = Name
            table[key]["Name"] = Name
            new_person = True

        else:
            new_person = False

    # Check if the this fields are already there with the name, if no append it.
    if ("ID" in line):
        ID = str(line[2])

        if new_person:
            table[key]["ID"] = ID

    if (("Test" in line) and ("Date:" in line)):
        Test_Date = str(line[2])

        if new_person:
            table[key]["Test Date"] = Test_Date

    if (("Run" in line) and ("Date:" in line)):
        Run_Date = str(line[2])

        if new_person:
            table[key]["Run Date"] = Run_Date


#Iterate throught the whole document again for each name.
for name in table.keys():

    i= 0
    n = 0

    #Find the name in the document
    while i < length_FILE:
        if cleaner.start_name_section(lines[i]):
            if cleaner.get_name(lines[i]) == name:
                    n = i
                    i = length_FILE

        i = i+1

        current_person = []

        while n < length_FILE:
            if cleaner.start_name_section(lines[n]):
                if cleaner.get_name(lines[n]) != name:
                    n = length_FILE
                else:
                    current_person.append(lines[n])
                    n = n+1
            else:
                current_person.append(lines[n])
                n = n+1

        processed = individual.preProcess_individual(current_person)
        final_list = individual.handle_columns(current_person)

        #Initialize the section.
        current_section = "Reading"

        final_list = cleaner.remove_empty_list(final_list)

        #Test Individual.
        if name == "Z JULIETA":
            f = open("TestingNew.txt", "w")
            for s in final_list:
                f.write(str(s) + "\n")
            f.close()

        for element in final_list:
            #Unlist element[0] if comes as a list
            if type(element[0]) is list:
                element = element[0]

            if cleaner.found_section(element):

                # If there was a section found, set the new current section.
                current_section = cleaner.get_section(element)

            if cleaner.is_number(element[0]):

                # Handle when they did not respond to an answer.
                if (len(element) == 4):

                    # Append to Data structure.
                    table[name][current_section]["Number"].append(element[0])
                    table[name][current_section]["Answers"].append(element[1])  # Index 2 has the correct answer, so we jump to three.
                    table[name][current_section]["isCorrect"].append(element[3])

                else:

                    # In this case since the person did not respond then just put NA and got to index 2.
                    table[name][current_section]["Number"].append(element[0])
                    table[name][current_section]["Answers"].append("NA")
                    table[name][current_section]["isCorrect"].append(element[2])

# Open file to write.
f1 = open("SUBSET_READING.txt", "w+")
f2 = open("SUBSET_LANGUAGE.txt", "w+")
f3 = open("SUBSET_MATHAPPLIED.txt", "w+")
f4 = open("SUBSET_MATHCOMPU.txt", "w+")

#Printing to files.
#Print to files.
for key in table.keys():

    f1.write("\n")
    f2.write("\n")
    f3.write("\n")
    f4.write("\n")

    for s in sections:

        r = table[key][s]["Number"]
        a = table[key][s]["isCorrect"]
        b = table[key][s]["Answers"]

        table[key][s]["Number"] = cleaner.multiple_sorting(r, a, b, "reference")
        table[key][s]["isCorrect"] = cleaner.multiple_sorting(r, a, b, "a")
        table[key][s]["Answers"] = cleaner.multiple_sorting(r, a, b, "b")


    f1.write(str(table[key]["Name"]) + ",  " + str(table[key]["ID"]) + ",  " + str(table[key]["Test Date"]) + ",  " +
            str(table[key]["Run Date"]) + ",  " +
             "Number: " + str(table[key]["Reading"]["Number"]) + ", " +
             "Answer: " + str(table[key]["Reading"]["Answers"]) + ", " +
            "IsCorrect: " + str(table[key]["Reading"]["isCorrect"]))

    f2.write(str(table[key]["Name"]) + ",  " + str(table[key]["ID"]) + ",  " + str(table[key]["Test Date"]) + ",  " +
            str(table[key]["Run Date"]) + ",  " +
             "Number: " + str(table[key]["Language"]["Number"]) + ", " +
             "Answer: " + str(table[key]["Language"]["Answers"]) + ", " +
            "IsCorrect: " + str(table[key]["Language"]["isCorrect"]))

    f3.write(str(table[key]["Name"]) + ",  " + str(table[key]["ID"]) + ",  " + str(table[key]["Test Date"]) + ",  " +
            str(table[key]["Run Date"]) + ",  " +
             "Number: " + str(table[key]["Applied Math"]["Number"]) + ", " +
             "Answer: " + str(table[key]["Applied Math"]["Answers"]) + ", " +
            "IsCorrect: " + str(table[key]["Applied Math"]["isCorrect"]))

    f4.write(str(table[key]["Name"]) + ",  " + str(table[key]["ID"]) + ",  " + str(table[key]["Test Date"]) + ",  " +
            str(table[key]["Run Date"]) + ",  " +
             "Number: " + str(table[key]["Math Compu"]["Number"]) + ", " +
             "Answer: " + str(table[key]["Math Compu"]["Answers"]) + ", " +
             "IsCorrect: " + str(table[key]["Math Compu"]["isCorrect"]))

              #"  " + str(table[key]["Language"]) + "  " + str(table[key]["Applied Math"]) + "  " + str(table[key]["Math Compu"]))


f1.close()
f2.close()
f3.close()
f4.close()

FILE.close()








