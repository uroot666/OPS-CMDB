#encoding: utf-8

def analysis(src, dest, topn=10):
    stat_dict = {}
    fhandler = open(src, "r")
    for line in fhandler:
        line_list = line.split()
        key = (line_list[0], line_list[6], line_list[8])
        stat_dict[key] = stat_dict.setdefault(key, 0) + 1
    fhandler.close()

    result = sorted(stat_dict.items(), key=lambda x:x[1])
    fhandler = open(dest, "w")
    for line in result[0:11]:
        fhandler.write('%s %s\n' % (' '.join(line[0]), str(line[1])))
    fhandler.close()

if __name__ == '__main__':
    access_file_path = "access.log"
    dest_path = "result.txt"
    analysis(access_file_path, dest_path)