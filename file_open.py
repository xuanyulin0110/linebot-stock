def file_write(filename, content):
    file = open(filename, 'w+')
    # for i in range(len(num)):
    #    file.write(str(num[i]))
    file.write(content)
    file.close()


def file_reed(filename):
    file = open(filename, 'r')
    content = file.read()
#    print(content)
    file.close()
    return content


def file_create(filename, content):
    file = open(filename, 'a')
    file.write(content)
    file.close()
