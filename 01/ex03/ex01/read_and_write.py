def read_and_write(in_file, out_file):
    with open(out_file, 'w') as outfile:
        for line in my_readline(in_file):
            outfile.write(parse_line(line))
        return

def my_readline(in_file):
    with open(in_file, "r") as infile:
        return infile.readlines()
    

def parse_line(in_line):
    index = 1
    out_line = in_line[0]
    quoted = True if (in_line[0] == '"') else False
    for char in in_line[1:]:
        if char == ',':
            if not quoted:
                out_line += '\t'
            elif quoted:
                out_line += char
        elif char == '"':
            if in_line[index-1] == '"':
                pass
            else:
                quoted = not quoted
            out_line += char
        else:
            out_line += char
            index += 1
    return out_line
    

if __name__ == '__main__':
    input_file = "ds.csv"
    output_file = "ds.tsv"
    read_and_write(input_file, output_file)
    
