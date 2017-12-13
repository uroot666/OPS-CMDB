#encoding=UTF-8
import json
import gconf

#读出用户数据，并转换成列表返回
def get_users():
    fh = open(gconf.USER_DATA_PATH, 'r')
    users = json.loads(fh.read())
    print(users)
    fh.close()
    return users

#循环验证用户数据中用户及密码
def validate_login(username, password):
    users = get_users()
    for user in users:
        if  user.get('username') == username and user.get('password') == password:
            return user
    return None

#分析log文件并返回倒数topn行
def gethtml(src, topn=10):
    stat_dict = {}
    fhandler = open(src, "r")
    for line in fhandler:
        line_list = line.split()
        key = (line_list[0], line_list[6], line_list[8])
        stat_dict[key] = stat_dict.setdefault(key, 0) + 1
    fhandler.close()

    result = sorted(stat_dict.items(), key=lambda x:x[1])
    print(topn)
    return result[: -topn - 1:-1]
    print(topn)

def user_del(id):
    users = get_users()
    index = 0
    for user_dict in users:
        if user_dict.get('id') == id:
            users.pop(index)
            users = json.dumps(users)
            fh = open(gconf.USER_DATA_PATH, 'w')
            fh.write(users)
            fh.close
            return True, user_dict.get("username")
        else:
            index = index + 1
    return None


def userEditSave(id, username, password):
    users = get_users()
    index = 0
    for user_dict in users:
        if user_dict.get('id') == id:
            users[index]["username"] = username
            users[index]["password"] = password
            fh = open(gconf.USER_DATA_PATH, 'w')
            users = json.dumps(users)
            fh.write(users)
            fh.close
            return True
        else:
            index = index + 1
    return  None
    


#将添加的用户信息写入到json文件中
def user_create(username, password):
    temp_user_all = get_users()
    add_user = {"id":temp_user_all[len(temp_user_all) - 1].get('id') + 1, "username":username, "password":password}
    temp_user_all.append(add_user)
    user_all = json.dumps(temp_user_all)
    fh = open(gconf.USER_DATA_PATH, 'w')
    fh.write(user_all)
    fh.close
