import random
import  file_open

ooxx_address_original = '_ | _ | _ \n-------  \n_ | _ | _ \n-------  \n_ | _ | _ '


def point_address(a, b):
    return (a - 1) * 21 + 4 * b - 4


def ooxx_gamestart(filename):
    file_open.file_write(filename, ooxx_address_original)

def ooxx(filename, textinput):
    print('1')

    ooxx_address = file_open.file_reed(filename)
    #print(ooxx_address)
    #print(ooxx_address)
    #print('*' * 10)
    if len(textinput) == 9:
        if textinput[0:3] == 'put':
            if textinput[4] == 'o':
                x = int(textinput[6])
                y = int(textinput[8])
                if 0 < x <= 3 and 0 < y <= 3:
                    #放入o位置
                    if ooxx_address[point_address(x, y)] != 'x' and ooxx_address[point_address(x, y)] != 'o':
                        ooxx_address = ooxx_address[0:point_address(x, y)] + 'o' + ooxx_address[point_address(x, y) + 1:]
                    else:
                        return ooxx_address[:52]
                    file_open.file_write(filename,ooxx_address)
                    print('2')
                    for i in range(3):
                        for j in range(3):
                            print('i=' + str(i+1) + ',j=' + str(j+1))
                            if ooxx_address[point_address(i+1, j+1)] == '_':
                                state = True
                                break
                            else:
                                state = False
                        if state == True:
                            break

                    if state == True:
                        print('True')
                    else:
                        print('False')
                        return ooxx_address[:52]
                    #print(ooxx_address)
                    #print('*'*10)
                    x_ = random.randint(1, 3)
                    y_ = random.randint(1, 3)
                    while ooxx_address[point_address(x_, y_)] == 'o' or ooxx_address[point_address(x_, y_)] == 'x':
                        x_ = random.randint(1, 3)
                        y_ = random.randint(1, 3)

                    #if ooxx_address[point_address(x, y)] == ooxx_address[point_address(x, y + 1)] and ooxx_address[point_address(x, y + 2)] != 'x':
                    #    x_ = x
                    #    y_ = y + 2

                    ooxx_address = ooxx_address[0:point_address(x_, y_)] + 'x' + ooxx_address[point_address(x_, y_) + 1:]
                    #print(ooxx_address)
                    file_open.file_write(filename,ooxx_address)
                    return ooxx_address[:52]
