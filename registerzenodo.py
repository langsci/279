import sys

try:
    import zenodo
except ImportError:
    from langsci import zenodo

glottolog = False
from pyglottolog import Glottolog
try:
    glottolog = Glottolog('.')
except ValueError:
    print("Glottolog tree directory not found. Glottocodes will not work. Please symlink the directories glottolog/languoids and glottolog/references")

"""
usage: > python3 zenodo.py 7
The script looks for all include'd files from the folder chapters/ in main.tex
It will ignore the first n files, where n is the argument of the script
If no argument is given, processing will start with the first file. 
For each file, the script will extract metadata from the file itself 
and from the file collection_tmp.bib generated by biber. 
The metadata is collected and a corresponding entry is created on Zenodo. 
The DOI assigned by Zenodo is collected and inserted into the file. 
"""

offset = 0
try:
    offset = int(sys.argv[1])
except IndexError:
    pass
extracommunities = []
try:
    extracommunities = sys.argv[2]
except IndexError:
    pass

book = zenodo.Book(extracommunities=extracommunities, glottolog=glottolog)
# for c in book.chapters:
# pprint.pprint(c.metadata)
try:
    tokenfile = open("zenodo.token")
except FileNotFoundError:
    print(
        "Token file not found. Please create a file 'zenodo.token', which must be readable.\nExiting"
    )
    raise SystemExit
token = open("zenodo.token").read().strip()
tokenfile.close()
# print(token)
# bookdoi = book.register(token)
# print("BookDOI{%s}"%bookdoi)


for i, ch in enumerate(
    book.chapters[offset:]
):  # for continuation if program stops in the middle of a book
    chapterf = open("chapters/%s.tex" % ch.path)
    chapterlines = chapterf.readlines()
    chapterf.close()
    for line in chapterlines:
        if "ChapterDOI" in line:
            print("DOI already present in %s" % ch.path)
            raise IOError
    try:
        chapterDOI = ch.register(token)
    except IndexError:
        print(
            "%s at position %i from offset %i could not be registered"
            % (ch.path, i, offset)
        )
        break
    insertstring = "\\ChapterDOI{%s}\n" % chapterDOI
    chapterf = open("chapters/%s.tex" % ch.path, "w")
    chapterf.write(chapterlines[0])
    chapterf.write(insertstring)
    chapterf.write("".join(chapterlines[1:]))
    chapterf.close()