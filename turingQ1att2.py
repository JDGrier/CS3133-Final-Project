def print_with_marker(string, position, state):
    marked_string = "_" + ''.join(string[:position]) + 'q' + str(state) + ''.join(string[position:]) 
    marked_string += "_"
    print(marked_string)

def turing(substring, fullstring):
    string_string = substring + "#" + fullstring
    string = list(string_string)
    position = 0
    state = 1

    print_with_marker(string, position, state)
    while(True):
        match state:
            case 1:
                if(string[position] == "0"):
                    string[position] = "a"
                    position += 1
                    state = 2
                elif(string[position] == "1"):
                    string[position] = "b"
                    position += 1
                    state = 3
                elif(string[position] == "#"):
                    position += 1
                    state = 8
            case 2:
                if(string[position] == "0" or string[position] == "1"):
                    position += 1
                elif(string[position] == "#"):
                    position += 1
                    state = 4
            case 3:
                if(string[position] == "0" or string[position] == "1"):
                    position += 1
                elif(string[position] == "#"):
                    position += 1
                    state = 5
            case 4:
                if (position > len(string)-1):
                    state = 13
                elif(string[position] == "x" or
                   string[position] == "a" or
                   string[position] == "b"):
                    position += 1
                elif(string[position] == "0"):
                    string[position] = "a"
                    position -= 1
                    state = 6
                elif(string[position] == "1"):
                    position -= 1
                    state = 9
            case 5:
                if (position > len(string)-1):
                    state = 13
                elif(string[position] == "x" or
                   string[position] == "a" or
                   string[position] == "b"):
                    position += 1
                elif(string[position] == "1"):
                    string[position] = "b"
                    position -= 1
                    state = 6
                elif(string[position] == "0"):
                    position -= 1
                    state = 9
            case 6:
                if(string[position] == "0" or
                    string[position] == "1" or
                    string[position] == "a" or
                    string[position] == "b" or
                    string[position] == "x"):
                    position -= 1
                elif(string[position] == "#"):
                    position -= 1
                    state = 7
            case 7:
                if(string[position] == "0" or string[position] == "1"):
                    position -= 1
                elif(string[position] == "a" or string[position] == "b" or position < 0):
                    position += 1
                    state = 1
            case 8:
                if(position > len(string)-1):
                    position += 1
                    state = 12
                elif(string[position] == "0" or
                    string[position] == "1" or
                    string[position] == "a" or
                    string[position] == "b" or
                    string[position] == "x"):
                    position += 1
            case 9:
                if(string[position] == "a"):
                    string[position] = "0"
                    position -= 1
                elif(string[position] == "b"):
                    string[position] = "1"
                    position -= 1
                elif(string[position] == "0" or string[position] == "1"):
                    position -= 1
                elif(string[position] == "#" or string[position] == "x"):
                    position += 1
                    state = 10
            case 10:
                if(string[position] == "0" or string[position] == "1"):
                    string[position] = "x"
                    position -= 1
                    state = 11
            case 11:
                if(string[position] == "a"):
                    string[position] = "0"
                    position -= 1
                elif(string[position] == "b"):
                    string[position] = "1"
                    position -= 1
                elif(string[position] == "0" or string[position] == "1"):
                    position -= 1
                elif(string[position] == "#" or string[position] == "x"):
                    position -= 1
                if(position < 0):
                    position += 1
                    state = 1
            case 12:
                prt_string = "_" + ''.join(string)
                prt_string += '1q'
                prt_string += str(state)
                print(prt_string)
                print("x is a substring of y")
                exit()
            case 13:
                print("x is not a substring of y")
                exit()
        print_with_marker(string, position, state)

turing("00", "100")