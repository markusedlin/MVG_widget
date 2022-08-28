import os

def new_file(filename):
    file = open(filename, 'x')
    file.close()

def remove_file(filename):
    import os
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(f"The '{filename}' does not exist") 

#reads line by line, adds them to a list, returns list of strings
def read_lines_to_list(filename):
    text_list = []
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        text_list.append(line.strip())
    return text_list

#appends text to end of line
def add_text(text, filename):
    with open(filename, 'a') as f:
        f.write(text+'\n')
        f.close()

def remove_text(text, filename):
    with open(filename, 'r') as fr:
        with open("temp.txt", 'w') as fw:
            for line in fr:
                if text != line.strip("\n"):
                    fw.write(line)
    os.replace("temp.txt",filename)

def delete_all_lines(filename):
    with open(filename,'r') as f:
        f.truncate()

def containsLine(line, filename):
    with open(filename) as f:
        lines = f.readlines()
        for l in lines:
            if l.strip() == line:
                return True
    return False

def printContents(filename):
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            print(line.strip())