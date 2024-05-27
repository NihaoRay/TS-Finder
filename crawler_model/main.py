import os

from group_file import group_ip_dataset, check_ip_dataset, load_ip_data
from group_features import group_features, check_features, transfer_session_pickle_csv


# 步骤：
# 1. 统计public_v2.json中有多少个独立的ip，独立的ua，独立的resource。
# 2. 调用group_ip_dataset方法，根据ip进行分组，同一个IP的流量保存在同一个文件中。
# 3. 对分组ip后的流量数据进行session分割。
# 4. 调用group_features，读取第3步中的文件，然后读取每个不同的session，计算每个session中相关的特征值，
# 每个session的特征值作为一个文件，使用pickle对dump硬盘中。
# 5. 调用transfer_session_pickle_csv，读取硬盘中dump的session特征值，进行整理转换成汇聚成一个csv文件，该csv文件里面包含所有session特征数据。
if __name__ == '__main__':
    group_file_save_folder = '/home/chenrui/localworkspace/ml_dataset/ml_dataflow/data/'
    session_features_save_folder = '/home/chenrui/localworkspace/ml_dataset/ml_dataflow/features/'
    dataset_path = '/home/chenrui/localworkspace/ml_dataset/ml_dataflow/public_v2.json'



    # file_name = '155.207.49806.csv'
    # group_features(session_features_save_folder + file_name, session_features_save_folder)
    # compute_features(save_folder, save_folder + file_name)

    # dataset_path = 'C:\\workspace\\ml_dataset\\test.json'
    # session_features_save_folder = 'C:\\workspace\\ml_dataset\\data_save\\'

    # 1. 统计public_v2.json中有多少个独立的ip，独立的ua，独立的resource。
    # check_ip_dataset(dataset_path)

    # 2. 调用group_ip_dataset方法，根据ip进行分组，同一个IP的流量保存在同一个文件中。
    # group_ip_dataset(dataset_path, group_file_save_folder)
    # 3. 对分组ip后的流量数据进行session分割。
    # load_ip_data(group_file_save_folder)

    ##### 这一步中间需要进行session_label操作

    # 4. 调用group_features，读取第3步中的文件 以及 session_label产生的 ua 标注文件，然后读取每个不同的session，
    # 计算每个session中相关的特征值，每个session的特征值作为一个文件，使用pickle dump到硬盘中。
    # ua_counter_labels = '/home/chenrui/localworkspace/ml_dataset/ml_dataflow/ua_counter_labels.txt'
    #
    # for filename in os.listdir(group_file_save_folder):
    #     datase_filename = os.path.join(group_file_save_folder, filename)
    #     print(datase_filename)
    #     group_features(datase_filename, session_features_save_folder)


    # 5.调用 transfer_session_pickle_csv 方法，读取第4步 每个session的dump pickle中的文件 进行整理转换成汇聚成一个 csv数据集合文件，该csv文件里面包含所有session特征数据。
    out_csv_save_folder = '/home/chenrui/localworkspace/ml_dataset/ml_dataflow'
    transfer_session_pickle_csv(session_features_save_folder, out_csv_save_folder)


    # 测试dump的dict
    # with open("/home/chenrui/localworkspace/ml_dataset/ml_dataflow/features/62.74.38624-0", "rb") as tf:
    #     new_dict = pickle.load(tf)

    # print(new_dict.items())
    # save_folder = 'C:/workspace/ml_dataset/'
    # for filename in os.listdir(save_folder):
    #     datase_filename = os.path.join(save_folder, filename)
    #     print(datase_filename)
    # group_features(datase_filename)

    # 测试将dump出来的pickle转成csv存储
    # session_pickle_path = ['C:/workspace/ml_dataset/features/1.239.59134-0',
    #                        'C:/workspace/ml_dataset/features/2.84.37443-1']
    #
    # session_pickle_path = 'C:/workspace/ml_dataset/features/'

    # for filename in os.listdir(save_folder):
    #     datase_filename = os.path.join(save_folder, filename)
    #     # print(datase_filename)
    #     check_features(datase_filename)