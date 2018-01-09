#encoding=UTF-8

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

if __name__ == '__main__':
    access_file_path = "access.log"
    result = gethtml(access_file_path)

    tbody = ''
    for line in result:
        tbody = tbody +\
        '''
            <tr>
                <th>{ip}</th>
                <th>{url}</th>
                <th>{code}</th>
                <th>{count}</th>
            </tr>
        '''.format(ip=line[0][0], url=line[0][1], code=line[0][2], count=line[1])

    html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>test</title>
            </head>
            <body>
                uroot test
                <table border="1">
                    <thead>
                        <tr>
                            <th>IP</th>
                            <th>URL</th>
                            <th>code</th>
                            <th>count</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tbody}
                    </tbody>
                </table>
            </body>
            </html>
            '''.format(tbody=tbody)
    fhandle = open('test.html', 'w',)
    fhandle.write(html)
    fhandle.close()