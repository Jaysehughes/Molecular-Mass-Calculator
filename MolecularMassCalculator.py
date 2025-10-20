#Import required libraries
import re
import os
import sys

#Dictionary defining elements and their mass values
#Mass values based on the IUPAC periodic table
# iupac.org/what-we-do/periodic-table-of-elements
element_dict = {
    "H": 1.0080, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81,
    "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
    "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974,
    "S": 32.06, "Cl": 35.45, "Ar": 39.95, "K": 39.098, "Ca": 40.078,
    "Sc": 44.956, "Ti": 47.867, "V": 50.942, "Cr": 51.996, "Mn": 54.938,
    "Fe": 55.845, "Co": 58.933, "Ni": 58.693, "Cu": 63.546, "Zn": 65.38,
    "Ga": 69.723, "Ge": 72.630, "As": 74.922, "Se": 78.971, "Br": 79.904,
    "Kr": 83.798, "Rb": 85.468, "Sr": 87.62, "Y": 88.906, "Zr": 91.224,
    "Nb": 92.906, "Mo": 95.95, "Tc": 97, "Ru": 101.07, "Rh": 102.91,
    "Pd": 106.42, "Ag": 107.87, "Cd": 112.41, "In": 114.82, "Sn": 118.71,
    "Sb": 121.76, "Te": 127.60, "I": 126.90, "Xe": 131.29, "Cs": 132.91,
    "Ba": 137.33, "La": 138.91, "Ce": 140.12, "Pr": 140.91, "Nd": 144.24,
    "Pm": 145, "Sm": 150.36, "Eu": 151.96, "Gd": 157.25, "Tb": 158.93,
    "Dy": 162.50, "Ho": 164.93, "Er": 167.26, "Tm": 168.93, "Yb": 173.05,
    "Lu": 174.97, "Hf": 178.49, "Ta": 180.95, "W": 183.84, "Re": 186.21,
    "Os": 190.23, "Ir": 192.22, "Pt": 195.08, "Au": 196.97, "Hg": 200.59,
    "Tl": 204.38, "Pb": 207.2, "Bi": 208.98, "Po": 209, "At": 210,
    "Rn": 222, "Fr": 223, "Ra": 226, "Ac": 227, "Th": 232.04,
    "Pa": 231.04, "U": 238.03, "Np": 237, "Pu": 244, "Am": 243,
    "Cm": 247, "Bk": 247, "Cf": 251, "Es": 252, "Fm": 257,
    "Md": 258, "No": 259, "Lr": 262, "Rf": 267, "Db": 268,
    "Sg": 269, "Bh": 270, "Hs": 269, "Mt": 277, "Ds": 281,
    "Rg": 281, "Cn": 285, "Nh": 286, "Fl": 290, "Mc": 290,
    "Lv": 293, "Ts": 294, "Og": 294,
}

#Store instructions to be displayed to the user
instructions = "Instructions\nEnter molecules using element symbols and subscripts\nExamples: H2O, CO2, C6H12O6\nUse parentheses for molecules with a coefficient\nExample: 2(H2O)\nUse parentheses for nested molecules\nExamples: Ca(NO3)2, Al2(SO4)3\nInvalid inputs will show an error message\nType clear to clear the terminal\nType exit to exit the calculator\nType help to display this message\n"

#Function to calculate molar mass, assuming no errors and no parentheses
def get_total(molecule):
    total = 0
    fake_element = []

    element_list = re.findall(r"([A-Z][a-z]?)(\d*)", molecule)      #Finds all matches in the string where a capital letter is optionally followed by a lowercase letter and then numbers Ex. H2O -> [('H', '2'), ('O', '')]
    for symbol, num_string in element_list:
        subscript = int(num_string) if num_string else 1
        if symbol in element_dict:
            total += element_dict[symbol] * subscript
        else:
            fake_element.append(f"Error: '{symbol}' is not a valid element.")
    return total, fake_element

#Function to throw an error if an element is comprised of only lowercase letters
def check_invalid_lowercase_letters(molecule):
    invalid_lowercase_letters = re.findall(r"(?<![A-Z])[a-z]", molecule)      #Finds all matches in the string where a lowercase letter is not preceded by a capital one Ex. h2o -> ['h', 'o']
    if not invalid_lowercase_letters:
        return []
    if len(invalid_lowercase_letters) == 1:
        return [f"Error: '{', '.join(invalid_lowercase_letters)}' is not a valid element."]
    else:
        return [f"Error: '{', '.join(invalid_lowercase_letters)}' are not valid elements."]

#Function to throw an error if any characters except for A-Z, a-z, 0-9, and () are entered
def check_special_characters(molecule):
    special_characters = re.findall(r"[^A-Za-z0-9()]", molecule)        #Finds all matches in the string that do not match any letters, numbers, or parentheses Ex. H2O! -> ['!']
    if not special_characters:
        return []
    if len(special_characters) == 1:
        return [f"Error: '{', '.join(special_characters)}' is not a valid input."]
    else:
        return [f"Error: '{', '.join(special_characters)}' are not valid inputs."]
    
#Function to throw an error if only numbers and no elements are entered
def check_numbers_only(molecule):
    numbers_only = re.fullmatch(r"\d+", molecule)       #Only matches if the entire string is made of numbers Ex. 2 -> ['2']
    return ["Error: Molecule must contain elements."] if numbers_only else []

#Function to throw an error if numbers are entered before an element without using parentheses
def check_numbers_before_symbol(molecule):
    numbers_before_symbol = re.findall(r"(\A[0-9]+[A-Z])", molecule)        #Finds all matches in the string where a number precedes an element without parentheses Ex. 2H2O -> ['2H']
    return ["Error: Missing parentheses."] if numbers_before_symbol else []

#Function to throw an error if an element subscript includes zeros before the actual subscript number
def check_leading_zeros(molecule):
    leading_zeros = re.findall(r"[A-Z][a-z]?0\d*", molecule)        #Finds all matches in the string where a subscript is preceded by a zero Ex. H02O -> ['H02']
    return ["Error: Leading zeros are invalid."] if leading_zeros else []

#Function to throw an error if only () are entered
def check_lone_parentheses(molecule):
    lone_parentheses = re.fullmatch(r"[()]+", molecule)     #Only matches if the entire string is made of parentheses Ex. () -> ['()']
    if lone_parentheses:
        return [f"Error: '{lone_parentheses.group()}' is not a valid input."]
    else:
        return []

#Function to check if there are matching numbers of ( and )
def check_matching_parentheses(molecule):
    balance = 0
    for i, character in enumerate(molecule):
        if character == "(":
            balance += 1
        if character == ")":
            if balance == 0:
                return [f"Error: Unmatched closing parentheses at position {i + 1}."]
            else:
                balance -= 1
    if balance > 0:
        return ["Error: Missing closing parentheses."]
    else:
        return []

#Function to calculate molar mass when parentheses are entered
def get_total_parentheses(molecule):
    total = 0
    fake_element = []
    
    nested_parentheses = re.findall(r"\(+\w*\(", molecule)      #Finds all matches in the string where a parentheses is followed by a number or letter and then another parentheses Ex. (H2(O)) -> ['(H2(']
    if nested_parentheses:
        fake_element.append("Error: Nested parentheses are not supported. Simplify your formula.")
        return total, fake_element

    coefficient_match = re.match(r"^(\d+)\((.+)\)$", molecule)      #Finds all matches in the string where a number is followed by a parentheses Ex. 2(H2O) -> 2(
    if coefficient_match:
        coefficient = int(coefficient_match.group(1))
        molecule = coefficient_match.group(2)
    else:
        coefficient = 1

    while True:
        matches = re.findall(r"\(([^()]*)\)(\d*)", molecule)        #Finds all matches inside of parentheses and the subscripts, does not find molecules with coeffiecients Ex. (H2O)2 -> [('H2O', '2')]
        if not matches:
            break
        for content, num_string in matches:
            subscript = int(num_string) if num_string else 1
            element_list = re.findall(r"([A-Z][a-z]?)(\d*)", content)      #Finds all matches in the string where a capital letter is optionally followed by a lowercase letter and then numbers Ex. H2O -> [('H', '2'), ('O', '')]
            subtotal = 0
            for symbol, num_string2 in element_list:
                subscript2 = int(num_string2) if num_string2 else 1
                if symbol in element_dict:
                    subtotal += element_dict[symbol] * subscript2
                else:
                    fake_element.append(f"Error: '{symbol}' is not a valid element.")
            subtotal *= subscript
            total += subtotal
            molecule = molecule.replace(f"({content}){num_string}", "", 1)
    element_list = re.findall(r"([A-Z][a-z]?)(\d*)", molecule)      #Finds all matches in the string where a capital letter is optionally followed by a lowercase letter and then numbers Ex. H2O -> [('H', '2'), ('O', '')]
    for symbol, num_string in element_list:
        subscript = int(num_string) if num_string else 1
        if symbol in element_dict:
            total += element_dict[symbol] * subscript
        else:
            fake_element.append(f"Error: '{symbol}' is not a valid element.")
    total *= coefficient
    return total, fake_element

#Function to throw an error if an element in parentheses is placed before another element
def check_invalid_parentheses_order(molecule):
    invalid_parentheses_order = re.findall(r"\)\d*[A-Z]", molecule)     #Finds all matches in the string where a parentheses is followed by an element Ex. (H2O)H2O -> [')H']
    if invalid_parentheses_order:
        return ["Error: Molecules inside of parentheses must be placed last."]
    else:
        return []

#Main code loop
#Prints instructions for the user
#Waits for user input
#If the user inputs exit, clear, or help, execute the respective action
#Otherwise, calculate molar mass and run through all error checks
#Prints errors if any or prints total molar mass if no errors
def loop():
    print()
    print(instructions)
    while True:
        errors = []
        print("\nMolecular Mass Calculator")
        molecule = input("Enter Molecule: ")

        if molecule.lower() == "help":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(instructions)
            continue

        if molecule.lower() == "exit":
            sys.exit("Exiting")

        if molecule.lower() == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        
        if "(" not in molecule and ")" not in molecule:
            total, fake_element = get_total(molecule)
        else:
            total, fake_element = get_total_parentheses(molecule)

        invalid_lowercase_letters = check_invalid_lowercase_letters(molecule)
        special_characters = check_special_characters(molecule)
        numbers_only = check_numbers_only(molecule)
        numbers_before_symbol = check_numbers_before_symbol(molecule)
        leading_zeros = check_leading_zeros(molecule)
        lone_parentheses = check_lone_parentheses(molecule)
        matching_parentheses = check_matching_parentheses(molecule)
        invalid_parentheses_order = check_invalid_parentheses_order(molecule)

        errors.extend(fake_element)
        errors.extend(invalid_lowercase_letters)
        errors.extend(special_characters)
        errors.extend(numbers_only)
        errors.extend(numbers_before_symbol)
        errors.extend(leading_zeros)
        errors.extend(lone_parentheses)
        errors.extend(matching_parentheses)
        errors.extend(invalid_parentheses_order)

        if errors:
           print()
           for msg in errors:
               print(msg)
        else:
            print(f"\n{total:.4f}".rstrip("0").rstrip("."),"g/mol")

if __name__ == '__main__':
    loop()
