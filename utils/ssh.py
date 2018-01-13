#encoding: utf-8

import os
import paramiko
import traceback

# 远程执行命令
def exec_cmds(host, port, username, password, cmds=[]):
    client = paramiko.SSHClient()
    rt_list = []
    try:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port, username, password)
        for cmd in cmds:
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.readline()
            error = stderr.readline()
            rt_list.append([output, error])
    except paramiko.AuthenticationException as e:
        print("连接凭证错误")
        print(e)
        print(traceback.format_exc())
    except BaseException as e:
        print("未知错误")
        print(e)
        print(traceback.format_exc())

    
    client.close()
    return rt_list

# 上传文件
def upload_files(host, port, username, password, files=[]):
    t = paramiko.Transport((host, port))
    rt_list = []
    try:
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        for local, remote in files:
            sftp.put(local, remote)
            rt_list.append([local, remote])
    except paramiko.AuthenticationException as e:
        print("用户凭证错误")
        print(e)
    except BaseException as e:
        print("未知错误")
        print(traceback.format_exc())
    t.close()
    return rt_list


if __name__ == "__main__":
    files = [(r'''C:\Users\Administrator\Documents\GitHub\cmdb\agent\cmdb_agent.py''', "/tmp/")]
    print(upload_files("192.168.174.131", 22, "root", "liangbiao-1", files))
    cmds = ["id", "who", "who"]
    print(exec_cmds("192.168.174.131", 22, "root", "liangbiao-1", cmds))
=