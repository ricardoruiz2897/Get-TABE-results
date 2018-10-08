import cleaner

#This function takes all the lines representing an individual, and will return the lines needed to process that individual.
def preProcess_individual(lines):
    #Clean, and get only the information part.
    for i in range(len(lines)):
        if not cleaner.non_section2(lines[i]):
            lines[i] = []

    return lines

def handle_columns(lines):

    #Output array, is the ordered array that will be read, and will contain all the section information for the person linearly.
    out_list = []

    # Since the first line is a always name section, just skip it
    j = 1

    #For each line after the first one.
    while j < len(lines):

        if len(lines[j]) == 0:
            j = j+1
            continue

        elif len(lines) != 0 and cleaner.start_name_section(lines[j]):
            j = j+1
            continue

        elif len(lines[j]) != 0 and not cleaner.start_name_section(lines[j]):

            # Two columns.
            if cleaner.second_column_exists(lines[j]):

                # Init arrays. We are separating into two columns.
                column1 = []
                column2 = []

                x1 = 0  # counter for index column1
                x2 = 0  # counter for index column2

                while not cleaner.start_name_section(lines[j]) and j < len(lines):

                    if len(lines[j]) == 0:
                        j = j + 1

                    elif (len(lines[j]) != 0):

                        # If we found one of those weird lines which is only a column, then we check for the next line to see in which array put it.
                        if (len(lines[j]) < 5 and cleaner.is_number(lines[j][0]) and not cleaner.found_section(lines[j])):

                            column1.append([])
                            column2.append([])

                            x1 = len(column1) - 1
                            x2 = len(column2) - 1

                            # First column
                            if (len(lines[j + 1]) == 0):

                                # Append element by element.
                                for element in lines[j]:
                                    column1[x1].append(element)

                            # This means is in second column.
                            elif (cleaner.found_section(lines[j + 1][:2])):

                                # Append element by element.
                                for element in lines[j]:
                                    column2[x2].append(element)

                            # First column again.
                            else:

                                # Append element by element.
                                for element in lines[j]:
                                    column1[x1].append(element)
                                    # print(column2)

                            # We must delete the empty lists on both columns, and get the next index.
                            column1 = cleaner.remove_empty_list(column1)
                            column2 = cleaner.remove_empty_list(column2)
                            # print(lines[j])

                        if len(lines[j]) > 4 or (len(lines[j]) == 4 and cleaner.found_section(lines[j])):

                            column1 = cleaner.remove_empty_list(column1)
                            column2 = cleaner.remove_empty_list(column2)

                            column1.append([])
                            column2.append([])

                            x1 = len(column1) - 1
                            x2 = len(column2) - 1

                            section_elements = ["Reading", "Language", "Math", "Compu", "Applied", "Math"]
                            # print(lines[j])
                            #Case 1: Section found on one column and there are numbers on the other.
                            if cleaner.found_section(lines[j][:2]) and (
                                cleaner.is_number(lines[j][2]) or cleaner.is_number(lines[j][3])):

                                if cleaner.get_section(lines[j][:2]) == "Language":
                                    column1[x1].append("Language")
                                    column2[x2] = lines[j][2:len(lines[j])]

                                elif cleaner.get_section(lines[j][:2]) == "Reading":
                                    column1[x1].append("Reading")
                                    column2[x2] = lines[j][2:len(lines[j])]

                                elif cleaner.get_section(lines[j][:2]) == "Math Compu":
                                    column1[x1].append("Math")
                                    column1[x1].append("Compu")
                                    column2[x2] = lines[j][2:len(lines[j])]

                                elif cleaner.get_section(lines[j][:2]) == "Applied Math":
                                    # print("section:number" + " " +str(lines[j]))
                                    column1[x1].append("Applied")
                                    column1[x1].append("Math")
                                    column2[x2] = lines[j][2:len(lines[j])]

                            # Case 2: Numbers found in one column and section on the other.
                            elif cleaner.is_number(lines[j][0]) and (
                                        cleaner.found_section(lines[j][3:]) or cleaner.found_section(
                                        lines[j][4:]) or cleaner.found_section(lines[j][2:])):

                                # print("number:section" + " " + str(lines[j]))
                                temp = 0
                                t = 0

                                # Append all elements while a section hasn't been reached.
                                for element in lines[j]:
                                    if element not in section_elements:
                                        column1[x1].append(element)
                                        t = + 1
                                    else:
                                        temp = t

                                if cleaner.get_section(lines[j][2:]) == "Language":
                                    column2[x2].append("Language")

                                elif cleaner.get_section(lines[j][temp:]) == "Reading":
                                    column2[x2].append("Reading")

                                elif cleaner.get_section(lines[j][temp:]) == "Math Compu":
                                    column2[x2].append("Math")
                                    column2[x2].append("Compu")

                                else:
                                    column2[x2].append("Applied")
                                    column2[x2].append("Math")

                            # Case 3: Numbers found both columns.
                            elif cleaner.is_number(lines[j][0]) and (
                                    cleaner.is_number(lines[j][3]) or cleaner.is_number(lines[j][4])):

                                # print("number:number" + " " + str(lines[j]))

                                first = 0

                                for k in range(len(lines[j])):

                                    if lines[j][k] == "+" or lines[j][k] == "-":

                                        if first == 0:
                                            column1[x1].append(lines[j][k])
                                            first = first + 1

                                        else:
                                            column2[x2].append(lines[j][k])

                                    else:
                                        if first == 0:
                                            column1[x1].append(lines[j][k])

                                        else:
                                            column2[x2].append(lines[j][k])


                            # Case 4: Numbers found on column one and trash in the other.
                            elif cleaner.is_number(lines[j][0]) and not (
                                cleaner.is_number(lines[j][3]) or cleaner.is_number(lines[j][4])) and not (
                                cleaner.found_section(lines[j][3:]) or cleaner.found_section(lines[j][4:])):

                                # print("number:trash" + " " + str(lines[j]))

                                k = 0
                                l = 0

                                for element in lines[j]:

                                    if element != "+" and element != "-":
                                        column1[x1].append(lines[j][k])
                                        k = k + 1

                                    else:
                                        l = k
                                        break

                                # Append the last one.
                                column1[x1].append(lines[j][l])

                            # Case 5: Trash found on column one and numbers or section on the other.
                            # This means it started with trash
                            elif (not cleaner.is_number(lines[j][0]) and not cleaner.found_section(lines[j][:2])):

                                # print("trash:number/section" + " " + str(lines[j]))

                                for k in range(len(lines[j]) - 1):

                                    # If found section on a side.
                                    if cleaner.found_section(lines[j][k:k + 2]):

                                        if cleaner.get_section(lines[j][k:k + 2]) == "Language":
                                            column2[x2].append("Language")

                                        elif cleaner.get_section(lines[j][k:k + 2]) == "Reading":
                                            column2[x2].append("Reading")

                                        elif cleaner.get_section(lines[j][k:k + 2]) == "Math Compu":
                                            column2[x2].append("Math")
                                            column2[x2].append("Compu")

                                        else:
                                            column2[x2].append("Applied")
                                            column2[x2].append("Math")

                                    if cleaner.is_number(lines[j][k]):
                                        l = k
                                        for l in range(k, len(lines[j])):
                                            column2[x2].append(lines[j][l])
                                        break

                            # Case 6: Section found in column one and trash on column 2.
                            elif cleaner.found_section(lines[j][:2]) and not cleaner.is_number(
                                lines[j][2]) and not cleaner.is_number(lines[j][3]):

                                if cleaner.get_section(lines[j][:2]) == "Applied Math":
                                    # We know by testint that it only happens for "Applied Math".
                                    column1[x1].append(["Applied", "Math"])

                                elif cleaner.get_section(lines[j][:2]) == "Math Compu":
                                    column1[x1].append(["Math, Compu"])

                            else:
                                print("trash:trash")

                        # Go to the next lines
                        j = j + 1

                #Here we know another column section section has started.
                out_list = out_list + column1 + column2

            #Only one column
            elif not cleaner.second_column_exists(lines[j]):

                column = []
                column = cleaner.remove_empty_list(column)
                x = 0

                while j < len(lines) and not cleaner.start_name_section(lines[j]):
                    column.append([])
                    x = len(column) - 1

                    if len(lines[j]) == 0:
                        j = j+1

                    elif cleaner.found_section(lines[j]) or cleaner.is_number(lines[j][0]):
                        for element in lines[j]:
                            column[x].append(element)
                        j = j + 1

                    else:
                        j = j+1

                out_list = out_list + column

    return out_list







