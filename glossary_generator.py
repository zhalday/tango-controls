import glob

path = "source/**/*.md"
files = glob.glob(path, recursive=True)

key = "%[glossary_term]"
text = ""
save = False
for f in files:
    with open(f, 'r') as fp:
        # read all lines in a list
        lines = fp.readlines()
        for line in lines:
            # check if string present on a current line
            if line.find(key) != -1:
                save = True
                name = line.replace(key,"")
                name = name.replace("[","")
                name = name.replace("]","")
                text = text + name
            elif save:
                if line in ["\n", "\r\n"]:
                    filelink = f.replace("source/", "")
                    filelink = filelink.replace(".md", "")
                    filename = filelink.split("/")[-1]
                    text = text + " For more details please see the {doc}`"+filename+" <../" +filelink + ">` section.\n\n"
                    save = False
                else:
                    line = line.replace("%","")
                    text = text + "\t" + line


if text:
    output = ""
    generated = ".. [GENERATED]\n"
    with open("source/Reference/glossary_definitions.md", 'r') as fp:
        lines = fp.readlines()
        line_count = 0
        for line in lines:
            line_count+=1
            if line.find(generated) != -1:
                output = output + generated + text + " ```\n"
                break
            elif line_count == len(lines):
                output = output + generated + text + " ```\n"
                break
            else:
                output = output + line

    with open("source/Reference/glossary.md", 'w+') as fp:
        fp.write(output)
