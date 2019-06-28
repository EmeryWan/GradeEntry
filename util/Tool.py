import inspect

from singleton.AboutViewSingleton import AboutViewSingle


def is_num(num):
    try:
        float(num)
        return True
    except BaseException:
        return False


def colname_to_colnum(colname):
    if type(colname) is not str:
        return colname
    col = 0
    power = 1
    for i in range(len(colname) - 1, -1, -1):
        ch = colname[i]
        col += (ord(ch) - ord('A') + 1) * power
        power *= 26
    return col


def colnum_to_colname(colnum):
    if not str(colnum).isdigit():
        return colnum
    colnum = int(colnum)
    result = ''
    while not (colnum // 26 == 0 and colnum % 26 == 0):
        temp = 25
        if colnum % 26 == 0:
            result += chr(temp + ord('A'))
        else:
            result += chr(colnum % 26 - 1 + ord('A'))
        if colnum % 26 == 0:
            colnum //= 26
            colnum -= 1
        else:
            colnum //= 26
    # 倒序输出拼写的字符串
    return result[::-1]


def get_current_fun_name():
    return inspect.stack()[1][3]


def show_error_page():
    AboutViewSingle.instance().show()
    AboutViewSingle.instance().show_error()
