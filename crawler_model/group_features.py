import io
import os
import pickle
import time
from datetime import datetime

import pandas as pd


# 组合每个请求的特征
def group_features(dataset_path, session_features_save_folder):
    dataflow_list = {}
    session_flow = []
    with open(dataset_path, 'r') as fp:
        all_lines = fp.readlines()
        for i, line in enumerate(all_lines):
            if line == '\n' and i > 1:
                dataflow_list[f'{i}'] = session_flow
                session_flow = []
                continue
            session_flow.append(line)

    # 处理csv文件，将多个session放到列表里去
    flows_df = []
    for dataflows in dataflow_list:
        flows_df.append(
            pd.read_csv(io.StringIO('\n'.join(dataflow_list[dataflows])), sep='\t', lineterminator='\n', header=None))
    flows_df.append(pd.read_csv(io.StringIO('\n'.join(session_flow)), sep='\t', lineterminator='\n', header=None))

    # 加载labels
    ua_lable_dict = load_ua_dict()

    # 提取每个会话中的请求信息
    for session_index, session_flows in enumerate(flows_df):
        session_flows = session_flows.fillna(0)  # 对nan的数字填0

        session_flows_size = len(session_flows[0].tolist())

        session_features = {}

        session_features['NUMBER_OF_REQUESTS'] = len(session_flows)
        session_features['TOTAL_DURATION'] = session_flows[2].sum()
        session_features['AVERAGE_TIME'] = session_flows[2].mean()
        session_features['STANDARD_DEVIATION'] = session_flows[2].std() if session_flows_size > 1 else 0
        session_features['DATA'] = session_flows[9].sum()

        # 识别请求资源情况 请求html总数、css总数、image总数、js总数
        requests_df = session_flows.groupby(5).size()
        html_sum, css_sum, image_sum, js_sum, others_sum = get_request_type(requests_df)
        session_features['HTML_RATE'] = html_sum / session_flows_size
        session_features['CSS_RATE'] = css_sum / session_flows_size
        session_features['IMAGE_RATE'] = image_sum / session_flows_size
        session_features['JS_RATE'] = js_sum / session_flows_size
        session_features['OTHERS_RATE'] = others_sum / session_flows_size

        # repeated request
        session_features['REPEATED_REQUESTS'] = requests_df.apply(lambda x: x > 1).sum() / len(session_flows)

        # http method
        http_method_df = session_flows.groupby(4).size()
        get_sum, post_sum, head_sum, other_sum = get_method_type(http_method_df)
        session_features['METHOD_GET_RATE'] = get_sum / session_flows_size
        session_features['METHOD_POST_RATE'] = post_sum / session_flows_size
        session_features['METHOD_HEAD_RATE'] = head_sum / session_flows_size
        session_features['METHOD_OTHER_RATE'] = other_sum / session_flows_size

        # response code，下标没有错，在分组的时候，多插入一列的duration
        reponse_df = session_flows.groupby(7).size()
        sum_2xx, sum_3xx, sum_4xx, sum_5xx = get_response_code(reponse_df)
        session_features['SUM_2XX_RATE'] = sum_2xx / session_flows_size
        session_features['SUM_3XX_RATE'] = sum_3xx / session_flows_size
        session_features['SUM_4XX_RATE'] = sum_4xx / session_flows_size
        session_features['SUM_5XX_RATE'] = sum_5xx / session_flows_size

        # 用户的访问的时间序列
        user_time_series = session_flows[2].tolist()
        user_time_series[0] = 0.0
        session_features['USER_TIME_SERIES'] = ','.join(map(str, user_time_series))

        # 是否是周末
        weekend_day_rate,  deep_night_rate, resttime_rate, worktime_rate = get_weekend(session_flows[1])
        # print(str(weekend_day_rate))
        session_features['WEEKEND_DAY_RATE'] = weekend_day_rate
        session_features['DEEP_NIGHT_RATE'] = deep_night_rate
        session_features['RESTTIME_RATE'] = resttime_rate
        session_features['WORKTIME_RATE'] = worktime_rate

        # 绘制http的请求链（可以求出：width、depth，几个连续的请求），重点关注对象
        visit_link_tree, single_resource = get_visit_link(session_flows[5].tolist(), session_flows[6].tolist())
        # print(f'visit_link_tree: {visit_link_tree}')
        # print(f'单独访问的请求 single_resource: {single_resource}')

        width_max_rate, consecutive_size, single_flow_rate = get_visti_tree_type(session_flows_size, visit_link_tree,
                                                                                 single_resource)
        session_features['WIDTH_MAX_RATE'] = str(width_max_rate)
        session_features['CONSECUTIVE_SIZE'] = str(consecutive_size)
        session_features['SINGLE_FLOW_RATE'] = str(single_flow_rate)

        # 请求序列
        session_features['REQUEST_RESOURCE'] = ','.join(map(str, session_flows[5].tolist()))

        session_features['ROBOT'] = get_labels_from_ua(ua_lable_dict,
                                                       session_flows.groupby(8).size(), session_flows[5].tolist())

        dump_session_ip_file = session_features_save_folder + session_flows[0][0] + '-' + str(session_index)
        with open(dump_session_ip_file, 'wb') as dump_file:
            pickle.dump(session_features, dump_file)

        # print(session_features)
        print(dump_session_ip_file, session_features['ROBOT'])


# 获取请求类型的数量占比
def get_request_type(requests_df):
    html_sum = 0
    css_sum = 0
    image_sum = 0
    js_sum = 0
    for requests_key in requests_df.keys():
        # requests_key = str(requests_key)
        # 统计html
        if not isinstance(requests_key, str):
            html_sum = html_sum + requests_df[requests_key]
            continue

        requests_key_params = requests_key.split('?')
        if '.' not in requests_key or requests_key == '/':
            # print(f'requests_key:{requests_key}, keys:{requests_df.keys()}')
            html_sum = html_sum + requests_df[requests_key]
            continue

        # 统计image
        if len(requests_key_params) > 1 and (requests_key_params[1].endswith('.jpg')
                                             or requests_key_params[1].endswith('.gif')
                                             or requests_key_params[1].endswith('.png')):
            image_sum = image_sum + 1
            continue
        html_show = requests_key.startswith('/Cover/Show')
        html_jpg = '.jpg' in requests_key
        html_png = '.png' in requests_key
        html_images = '/images/' in requests_key
        if html_show or html_jpg or html_png or html_images:
            image_sum = image_sum + requests_df[requests_key]
            continue

        # 统计css
        if len(requests_key_params) > 1 and (requests_key_params[1].endswith('.css')
                                             or requests_key_params[0].endswith('.css')):
            css_sum = css_sum + requests_df[requests_key]
            continue
        if requests_key_params[0].endswith('.css') or '/css' in requests_key:
            css_sum = css_sum + requests_df[requests_key]
            continue

        # 统计js
        if len(requests_key_params) > 1 and (requests_key_params[1].endswith('.js')
                                             or requests_key_params[0].endswith('.js')):
            js_sum = js_sum + requests_df[requests_key]
            continue
        if requests_key_params[0].endswith('.js'):
            js_sum = js_sum + requests_df[requests_key]
            continue

        # print(f'============requests source: {requests_key}===============')

    others_sum = requests_df.sum() - (html_sum + css_sum + image_sum + js_sum)
    return html_sum, css_sum, image_sum, js_sum, others_sum


# 获取http method的数量占比
def get_method_type(http_method_df):
    get_sum = 0
    post_sum = 0
    head_sum = 0
    for http_method_key in http_method_df.keys():
        http_method_key = str(http_method_key)
        if 'get' == http_method_key.lower():
            get_sum = get_sum + http_method_df[http_method_key]
            continue
        if 'post' == http_method_key.lower():
            post_sum = post_sum + http_method_df[http_method_key]
            continue
        if 'head' == http_method_key.lower():
            head_sum = head_sum + http_method_df[http_method_key]
            continue
        # print(f'=============http_method: {http_method_key}=============')

    other_sum = http_method_df.sum() - (get_sum + post_sum + head_sum)
    return get_sum, post_sum, head_sum, other_sum


# 获的response code的数量占比
def get_response_code(reponse_df):
    sum_2xx = 0
    sum_3xx = 0
    sum_4xx = 0
    sum_5xx = 0
    for code in reponse_df.keys():
        if 200 <= int(code) < 300:
            sum_2xx = sum_2xx + reponse_df[code]
            continue
        if 300 <= int(code) < 400:
            sum_3xx = sum_3xx + reponse_df[code]
            continue
        if 400 <= int(code) < 500:
            sum_4xx = sum_4xx + reponse_df[code]
            continue
        sum_5xx = sum_5xx + reponse_df[code]
        # print(f'=============response_code: {code}=============')
    return sum_2xx, sum_3xx, sum_4xx, sum_5xx


# 计算weekend day，深夜访问、7到12点之间的访问时间、工作访问时间 占比
def get_weekend(time_df):
    series_len = len(time_df)

    weekend_day_sum = 0
    deep_night_time_sum = 0
    worktime_sum = 0
    resttime_sum = 0

    for timestamp_item in time_df.tolist():
        ltime = time.localtime(int(float(timestamp_item)))
        dateymd = time.strftime("%Y-%m-%d", ltime)
        weekday = datetime.strptime(dateymd, "%Y-%m-%d").weekday()

        if 5 <= weekday <= 6:
            weekend_day_sum = weekend_day_sum + 1

        if 0 <= ltime.tm_hour <= 7:
            deep_night_time_sum = deep_night_time_sum + 1

        if 19 <= ltime.tm_hour:
            resttime_sum = resttime_sum + 1

        if 7 < ltime.tm_hour < 19:
            worktime_sum = worktime_sum + 1

    return weekend_day_sum / series_len, deep_night_time_sum / series_len, resttime_sum / series_len, worktime_sum / series_len


# 绘制访问链接树
def get_visit_link(resource_list, referrer_list):
    assert len(resource_list) == len(referrer_list)

    referrer_list_copy = referrer_list.copy()
    resource_list_copy = resource_list.copy()

    visit_link_tree = {}
    resource_list_len = len(resource_list)
    source_index = 0
    while source_index < resource_list_len and len(referrer_list_copy) > 0:
        referrer_list, referrer_index_arr, ret_resource_list = check_index_list(resource_list[source_index],
                                                                                referrer_list_copy, resource_list_copy)

        next_source = []
        for referrer_index in referrer_index_arr:
            next_source.append(resource_list_copy[referrer_index])

        for referrer_item, resource_item in zip(referrer_list, ret_resource_list):
            referrer_list_copy.remove(referrer_item)
            resource_list_copy.remove(resource_item)

        if len(referrer_list):
            visit_link_tree[resource_list[source_index]] = next_source

        source_index = source_index + 1
    return visit_link_tree, resource_list_copy  # 单独访问的请求，不在树节点之内


# 当前访问的资源是否出现在已被精简的referer中
def check_index_list(item, referer_list, resource_list):
    assert len(referer_list) == len(resource_list)
    item = str(item)

    ret_referer_list = []
    ret_referer_index_list = []
    ret_resource_list = []
    for i, source in enumerate(referer_list):
        if item != '/' and item in source:
            ret_referer_list.append(source)
            ret_referer_index_list.append(i)
            ret_resource_list.append(resource_list[i])
    return ret_referer_list, ret_referer_index_list, ret_resource_list


# 统计visit_tree的最长的连续请求占总数比，连续请求的个数，单独请求的占总数比
def get_visti_tree_type(session_flows_size, visit_link_tree, single_resource):
    width_max = 0
    for i, item_key in enumerate(visit_link_tree):
        width = len(visit_link_tree[item_key])
        if width > width_max:
            width_max = width

    consecutive_size = len(visit_link_tree)
    width_max_rate = width_max / session_flows_size
    single_flow_rate = len(single_resource) / session_flows_size

    return width_max_rate, consecutive_size, single_flow_rate


# 将dump出来的pickle转成csv存储
def transfer_session_pickle_csv(session_pickle_path, save_folder):
    df_total = pd.DataFrame()
    for i, filename in enumerate(os.listdir(session_pickle_path)):
        datase_filename = os.path.join(session_pickle_path, filename)
        with open(datase_filename, "rb") as tf:
            df = pd.DataFrame(pickle.load(tf), index=[0])
            print(f'i:{i}, datase_filename:{datase_filename}, df_size:{len(df)}')
            df['ID'] = filename
            df_total = df_total.append(df)

    df_total.to_csv(os.path.join(save_folder, 'out.csv'))


# 加载ua_label
def load_ua_dict():
    ua_counter_labels = '/home/chenrui/localworkspace/ml_dataset/ml_dataflow/ua_counter_labels.txt'

    with open(ua_counter_labels, 'r') as ua_file:
        ua_dict_content = ua_file.readlines()

    ua_dict = {}
    for ua_item in ua_dict_content:
        ua_arr = ua_item.replace('\n', '').split('\t')
        ua_dict[ua_arr[0]] = ua_arr[1]

    return ua_dict

# 获取labels
def get_labels_from_ua(ua_dict, ua_df, resource_list):
    if 'robots.txt' in resource_list:
        return '1'
    if 'CHENRUI' in ua_df and ua_df['CHENRUI'] / ua_df.sum() > 0.05:
        return '1'
    for ua in ua_df.keys():
        if ua in ua_dict and ua_dict[ua] == '1' and ua != 'CHENRUI':
            return '1'
    return '0'


# 组合每个请求的特征
def check_features(dataset_path):
    dataflow_list = {}
    session_flow = []
    with open(dataset_path, 'r') as fp:
        all_lines = fp.readlines()
        for i, line in enumerate(all_lines):
            if line == '\n' and i > 1:
                dataflow_list[f'{i}'] = session_flow
                session_flow = []
                continue
            session_flow.append(line)

    # 处理csv文件，将多个session放到列表里去
    flows_df = []
    for dataflows in dataflow_list:
        flows_df.append(
            pd.read_csv(io.StringIO('\n'.join(dataflow_list[dataflows])), sep='\t', lineterminator='\n', header=None))
    flows_df.append(pd.read_csv(io.StringIO('\n'.join(session_flow)), sep='\t', lineterminator='\n', header=None))

    # 提取每个会话中的请求信息
    for session_index, session_flows in enumerate(flows_df):
        if len(session_flows.columns) != 11:
            print(dataset_path, len(session_flows.columns))
