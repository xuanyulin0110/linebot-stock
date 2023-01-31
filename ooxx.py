import random
import file_open
from linebot.models import FlexSendMessage

ooxx_address_original = '  |   |   \n-------  \n  |   |   \n-------  \n  |   |  '


def flexsendmessage(ooxx_address):
    flex_point = []
    for i in [1, 2, 3]:
        for j in [1, 2, 3]:
            flex_point.append(ooxx_address[point_address(i, j)])

    # print("flex_point= "+str(flex_point))
    return FlexSendMessage(
        alt_text='hello',
        contents={
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": flex_point[0],
                                    "text": "put o 1-1"
                                },
                                "margin": "none",
                                "style": "secondary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": flex_point[1],
                                    "text": "put o 1-2"
                                },
                                "margin": "none",
                                "style": "secondary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": flex_point[2],
                                    "text": "put o 1-3"
                                },
                                "margin": "none",
                                "style": "secondary"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": flex_point[3],
                                    "text": "put o 2-1"
                                },
                                "margin": "none",
                                "style": "secondary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": flex_point[4],
                                    "text": "put o 2-2"
                                },
                                "margin": "none",
                                "style": "secondary"

                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": flex_point[5],
                                    "text": "put o 2-3"
                                },
                                "margin": "none",
                                "style": "secondary"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": flex_point[6],
                                    "text": "put o 3-1"
                                },
                                "margin": "none",
                                "style": "secondary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": flex_point[7],
                                    "text": "put o 3-2"
                                },
                                "margin": "none",
                                "style": "secondary"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": flex_point[8],
                                    "text": "put o 3-3"
                                },
                                "margin": "none",
                                "style": "secondary"
                            }
                        ]
                    }
                ]
            }
        }
    )


def point_address(a, b):
    return (a - 1) * 21 + 4 * b - 4


# def ooxx_gameover():
#     for a, b in [1,2,3], [1,2,3]:
#         point_address(a,b)


def ooxx_room(filename):
    mode = file_open.file_reed(filename)
    if mode[0:3] == '房間一':
        return '房間一'
    else:
        return filename + 'ooxx'


def ooxx_gamestart(filename, mode):
    file_open.file_write(filename, mode)
    filename_ = ooxx_room(filename)
    file_open.file_write(filename_, ooxx_address_original)
    return ooxx_refrash(filename)


def ooxx_refrash(filename):
    filename = ooxx_room(filename)
    ooxx_address = file_open.file_reed(filename)
    return [flexsendmessage(ooxx_address), ooxx_address[:52], gamecheck(ooxx_address)]


def ooxx(filename, textinput):
    mode = file_open.file_reed(filename)
    if mode[0:2] == '房間':
        flagAI = False
        if mode[3] == 'o':
            flag = 'o'
        else:
            flag = 'x'
    else:
        flagAI = True
        flag = 'o'
    filename = ooxx_room(filename)
    ooxx_address = file_open.file_reed(filename)
    # print(ooxx_address)
    # print(ooxx_address)
    # print('*' * 10)
    if len(textinput) == 9:
        if textinput[0:3] == 'put':
            if textinput[4] == 'o':
                x = int(textinput[6])
                y = int(textinput[8])
                if 0 < x <= 3 and 0 < y <= 3:

                    # 放入o位置
                    if ooxx_address[point_address(x, y)] != 'x' and ooxx_address[point_address(x, y)] != 'o':
                        ooxx_address = ooxx_address[0:point_address(x, y)] + flag + ooxx_address[
                                                                                    point_address(x, y) + 1:]
                    else:
                        return [flexsendmessage(ooxx_address), ooxx_address[:52], gamecheck(ooxx_address)]

                    file_open.file_write(filename, ooxx_address)

                    if flagAI == True:
                        for i in range(3):
                            for j in range(3):
                                # print('i=' + str(i+1) + ',j=' + str(j+1))
                                if ooxx_address[point_address(i + 1, j + 1)] == ' ':
                                    state = True
                                    break
                                else:
                                    state = False
                            if state == True:
                                break

                        if state == True:
                            pass  # print('True')
                        else:
                            # print('False')
                            return [flexsendmessage(ooxx_address), ooxx_address[:52], gamecheck(ooxx_address)]
                        # print(ooxx_address)
                        # print('*'*10)

                        # 橫向
                        for a in [1, 2, 3]:
                            temp = 0
                            for b in [1, 2, 3]:
                                point = point_address(a, b)
                                if ooxx_address[point] == 'x':
                                    temp += 1
                                elif ooxx_address[point] == 'o':
                                    temp -= 1
                                # print('temp = '+str(temp))
                            if temp == -2 or temp == 2:
                                for i in [1, 2, 3]:
                                    if ooxx_address[point_address(a, i)] == ' ':
                                        ooxx_address = ooxx_address[0:point_address(a, i)] + 'x' + ooxx_address[
                                                                                                   point_address(a,
                                                                                                                 i) + 1:]
                                        file_open.file_write(filename, ooxx_address)
                                        return [flexsendmessage(ooxx_address), ooxx_address[:52],
                                                gamecheck(ooxx_address)]
                        # 縱向
                        for b in [1, 2, 3]:
                            temp = 0
                            for a in [1, 2, 3]:
                                point = point_address(a, b)
                                if ooxx_address[point] == 'x':
                                    temp += 1
                                elif ooxx_address[point] == 'o':
                                    temp -= 1
                                # print('temp = '+str(temp))
                            if temp == -2 or temp == 2:
                                for i in [1, 2, 3]:
                                    if ooxx_address[point_address(i, b)] == ' ':
                                        ooxx_address = ooxx_address[0:point_address(i, b)] + 'x' + ooxx_address[
                                                                                                   point_address(i,
                                                                                                                 b) + 1:]
                                        file_open.file_write(filename, ooxx_address)
                                        return [flexsendmessage(ooxx_address), ooxx_address[:52],
                                                gamecheck(ooxx_address)]
                        # 斜向
                        temp = 0
                        for a in [1, 2, 3]:
                            point = point_address(a, a)
                            if ooxx_address[point] == 'x':
                                temp += 1
                            elif ooxx_address[point] == 'o':
                                temp -= 1
                        if temp == -2 or temp == 2:
                            for i in [1, 2, 3]:
                                if ooxx_address[point_address(i, i)] == ' ':
                                    ooxx_address = ooxx_address[0:point_address(i, i)] + 'x' + ooxx_address[
                                                                                               point_address(i, i) + 1:]
                                    file_open.file_write(filename, ooxx_address)
                                    return [flexsendmessage(ooxx_address), ooxx_address[:52], gamecheck(ooxx_address)]
                        temp = 0
                        for a in [1, 2, 3]:
                            point = point_address(a, 4 - a)
                            if ooxx_address[point] == 'x':
                                temp += 1
                            elif ooxx_address[point] == 'o':
                                temp -= 1
                        if temp == -2 or temp == 2:
                            for i in [1, 2, 3]:
                                if ooxx_address[point_address(i, 4 - i)] == ' ':
                                    ooxx_address = ooxx_address[0:point_address(i, 4 - i)] + 'x' + ooxx_address[
                                                                                                   point_address(i,
                                                                                                                 4 - i) + 1:]
                                    file_open.file_write(filename, ooxx_address)
                                    return [flexsendmessage(ooxx_address), ooxx_address[:52], gamecheck(ooxx_address)]

                        x_ = random.randint(1, 3)
                        y_ = random.randint(1, 3)
                        while ooxx_address[point_address(x_, y_)] == 'o' or ooxx_address[point_address(x_, y_)] == 'x':
                            x_ = random.randint(1, 3)
                            y_ = random.randint(1, 3)

                        # if ooxx_address[point_address(x, y)] == ooxx_address[point_address(x, y + 1)] and ooxx_address[point_address(x, y + 2)] != 'x':
                        #    x_ = x
                        #    y_ = y + 2

                        ooxx_address = ooxx_address[0:point_address(x_, y_)] + 'x' + ooxx_address[
                                                                                     point_address(x_, y_) + 1:]
                        # print(ooxx_address)
                        file_open.file_write(filename, ooxx_address)
                    return [flexsendmessage(ooxx_address), ooxx_address[:52], gamecheck(ooxx_address)]
                    # game判斷


def gamecheck(ooxx_address):
    for a in [1, 2, 3]:
        temp = 0
        for b in [1, 2, 3]:
            point = point_address(a, b)
            # print("point="+str(point))
            # print("ooxx_address="+str(ooxx_address))
            if ooxx_address[point] == 'x':
                temp += 1
            elif ooxx_address[point] == 'o':
                temp -= 1
        if temp == 3:
            return "x win"
        elif temp == -3:
            return "o win"

        for b in [1, 2, 3]:
            temp = 0
            for a in [1, 2, 3]:
                point = point_address(a, b)
                if ooxx_address[point] == 'x':
                    temp += 1
                elif ooxx_address[point] == 'o':
                    temp -= 1
            # print("\n\ntemp="+str(temp))
            if temp == 3:
                return "x win"
            elif temp == -3:
                return "o win"
        temp = 0
        for a in [1, 2, 3]:
            point = point_address(a, a)
            if ooxx_address[point] == 'x':
                temp += 1
            elif ooxx_address[point] == 'o':
                temp -= 1
        if temp == 3:
            return "x win"
        elif temp == -3:
            return "o win"
        temp = 0
        for a in [1, 2, 3]:
            point = point_address(a, 4 - a)
            if ooxx_address[point] == 'x':
                temp += 1
            elif ooxx_address[point] == 'o':
                temp -= 1
        if temp == 3:
            return "x win"
        elif temp == -3:
            return "o win"
        else:
            return '再來啊！🤪'