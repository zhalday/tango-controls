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
            # check current line starts with the glossary signature
            if line.startswith(key):
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
                    if filename == "index":
                        filename = filelink.split("/")[-2]
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
            if line.startswith("%"):
                #ignore comments in definition file
                continue
            if line.find(generated) != -1:
                output = output + generated + text + " ```\n"
                break
            elif line_count == len(lines):
                output = output + generated + text + " ```\n"
                break
            else:
                output = output + line

    with open("source/Reference/glossary.md", 'w+') as fp:
        fp.write("% !!!! This is the auto-generated glossary file. Do not manually add defintions\
 here as they will be overwritten the next time the documentation is built! Instead add them\
 in the relevant section using the '%[glossary_term][<term_name>]' label or in\
 glossary_definitions.md file.\n")
        fp.write(output)
