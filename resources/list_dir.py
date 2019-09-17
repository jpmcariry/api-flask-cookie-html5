import os


files = []
# r=root, d=directories, f = files
def list_in_file(path='C:\\Users\\capit\\PycharmProjects\\flask\\static\\img'):
    coisa=[]

    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if ('.jpg') in file:

                text=os.path.join(r, file)
                start=text.find("img", )+4
                end=text.find('.')
                name=text[start:end]
                coisa+=[text[start:]]
                files.append(os.path.join(r, file))
            if ('.pdf') in file:
                text = os.path.join(r, file)
                start = text.find("img", ) + 4
                end = text.find('.')
                name = text[start:end]
                coisa += [text[start:]]
                files.append(os.path.join(r, file))
            if ('.png') in file:
                text = os.path.join(r, file)
                start = text.find("img", ) + 4
                end = text.find('.')
                name = text[start:end]
                coisa += [text[start:]]
                files.append(os.path.join(r, file))
            if ('.jpeg') in file:
                text = os.path.join(r, file)
                start = text.find("img", ) + 4
                end = text.find('.')
                name = text[start:end]
                coisa += [text[start:]]
                files.append(os.path.join(r, file))
            if ('.json') in file:
                text = os.path.join(r, file)
                start = text.find("img", ) + 4
                end = text.find('.')
                name = text[start:end]
                coisa += [text[start:]]
                files.append(os.path.join(r, file))
    print(files, coisa)
    return files, coisa
list_in_file()