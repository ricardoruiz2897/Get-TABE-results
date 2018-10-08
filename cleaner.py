#This function will return true if it finds a section, and false if it doesn't.
def found_section(line):

    #Sections of the test.
    sections1 = ["Reading", "Language"]
    sections2 = ["Math", "Compu", "Applied", "Math"]

    if (sections1[0] in line) or (sections1[1] in line) or (sections2[0] in line and sections2[1] in line) or (sections2[2] in line and sections2[3]):
        return True
    else:
        return False

def get_section(line):
    
    #Sections of the test.
    sections1 = ["Reading", "Language"]
    sections2 = ["Math", "Compu", "Applied", "Math"]

    for section in sections1:
        if section in line:
            return section
        
    if (sections2[0] in line) and (sections2[1] in line):
        return "Math Compu"

    if (sections2[2] in line) and (sections2[3] in line):
        return "Applied Math"



#This function tells if a column exists. ()
def second_column_exists(line):

    if(len(line) >= 4):
        return True
    else:
        return False

#This function will tell if a new section for a person has been started (It can be repeated, or not.)
def start_name_section(line):

    if(len(line) == 0):
        return False

    if(("Item" in line) and ("Analysis" in line) and ("for" in line)):
        return True
    else:
        return False

#This function will retrun a name and should only be called if start_name_section was true, and is still in the same.
def get_name(line):
    return str(line[len(line)-2]) + " " + str(line[len(line)-1])

#This function will tell you if a string is number or not.
def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

#This function will tell if we have reached the end of the document.
def end_document(length_file, current_line):
    if current_line >= length_file:
        return True
    else:
        return False

#This function will remove any duplicated lists.
def removeDuplicated(old):
    new = []
    for o in old:
        if o in new:
            continue
        else:
            new.append(o)
    return new

def remove_empty_list(list_):
    new = [l for l in list_ if l]
    return new

def multiple_sorting(reference_list, list_a, list_b, which):

    for i in range(len(reference_list)):
        for j in range(len(reference_list)):

            # Swap in all lists.
            if int(reference_list[i]) < int(reference_list[j]):
                reference_list[i], reference_list[j] = reference_list[j], reference_list[i]
                list_a[i], list_a[j] = list_a[j], list_a[i]
                list_b[i], list_b[j] = list_b[j], list_b[i]

    if which == "reference":
        return reference_list

    elif which == "a":
        return list_a

    elif which == "b":
        return list_b

    else:
        print("Error: please specify return value.")
        return

def non_section(line):

    pivots = ["Item", "Group", "Date", "ID"]

    if len(line) == 0:
        return False

    for p in pivots:
        if p in line:
            return False

    return True

def non_section2(line):

    pivots = ["Group:", "Date:", "ID", "Group"]

    if len(line) == 0:
        return False

    for p in pivots:
        if p in line:
            return False

    return True

def first_M(line):

    if len(line) == 0:
        return False

    if line[0][0] == "M" :
        return True
    else:
        return False


def valid_column(line):

    if len(line) >= 3:
        return True
    return False

