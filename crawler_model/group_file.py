import json
import os
import time


def group_ip_dataset(dataset_path, save_folder):
    print('清空' + save_folder + ', 下的所有文件')
    for filename in os.listdir(save_folder):
        os.remove(os.path.join(save_folder, filename))

    with open(dataset_path, 'r') as fp:
        content = json.load(fp)
        for i, line in enumerate(content):
            ip = content[line]['ip']
            timestamp = content[line]['timestamp']
            request = content[line]['request'] if 'request' in content[line] and '' != content[line]['request'] else 'CHENRUI'
            referrer = content[line]['referrer'] if 'referrer' in content[line] and '' != content[line]['referrer'] else 'CHENRUI'
            method = content[line]['method'] if 'method' in content[line] and '' != content[line]['method'] else 'CHENRUI'
            resource = content[line]['resource'] if 'resource' in content[line] and '' != content[line]['resource'] else 'CHENRUI'
            response = content[line]['response'] if 'response' in content[line] and '' != content[line]['response'] else '600' #不可能有600这个数，所以用这个来代替
            if response == '408':
                continue
            bytes = content[line]['bytes'] if 'bytes' in content[line] and '' != content[line]['bytes'] else '0'
            useragent = content[line]['useragent'] if 'useragent' in content[line] and '' != content[line]['useragent'] else 'CHENRUI'
            time_mk = str(time.mktime(time.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.000Z')))

            print(f'i:{i + 1}, ip:{ip}, timestamp:{timestamp}, time_mk:{time_mk}')
            with open(save_folder + "/" + ip + ".csv", 'a') as writefile:
                save_line = [ip, time_mk, timestamp, method, resource, referrer, response, useragent, bytes, request]
                writefile.writelines('\t'.join(save_line) + '\n')


def check_ip_dataset(dataset_path):
    ip_set = []
    ua_set = []
    resource_set = []
    with open(dataset_path, 'r') as fp:
        content = json.load(fp)
        for i, line in enumerate(content):
            if content[line]['response'] == '408':
                continue
            ip = content[line]['ip']
            ua = content[line]['useragent']
            if 'resource' in content[line]:
                resource_set.append(content[line]['resource'])

            ip_set.append(ip)
            ua_set.append(ua)
            print(i)

    print(f'请求流量数：{len(ip_set)}')
    ip_list = list(set(ip_set))
    ua_list = list(set(ua_set))
    resource_list = list(set(resource_set))
    print(f'独立的IP数目：{len(ip_list)}')
    print(f'独立的ua数目：{len(ua_list)}')
    print(f'独立的resource数目：{len(resource_list)}')


# 加载根据ip分好组的所有文件
def load_ip_data(save_folder):
    file_path_list = []
    for filename in os.listdir(save_folder):
        file_path_list.append(os.path.join(save_folder, filename))

    for file_path in file_path_list:
        with open(file_path, 'r+') as file_read:
            file_content = file_read.readlines()

            file_read.seek(0)
            file_read.truncate()  # 首先清空该文件

            timestamp = 0
            referrer = ''
            for i, data_line in enumerate(file_content):
                line_arr = data_line.replace('\n', '').split('\t')
                date_split = 0
                if i > 0:
                    date_split = float(line_arr[1]) - timestamp
                line_arr.insert(2, str(date_split)) # 插入一行duration，这个方法后面的列表扩充了一列
                writeline = '\t'.join(line_arr) + '\n'
                timestamp = float(line_arr[1])
                if date_split >= 1800 and referrer != line_arr[6]:  # 时间间隔超过30分钟
                    writeline = '\n' + writeline
                    # print(i)
                referrer = line_arr[6]
                file_read.writelines(writeline)
