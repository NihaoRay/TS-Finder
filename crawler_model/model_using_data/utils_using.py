import numpy as np
import pandas as pd
from sklearn.metrics import f1_score


def read_data(path):
    df_chunk = pd.read_csv(path, chunksize=1e6, iterator=True, header=0)
    data = pd.concat([chunk for chunk in df_chunk]).fillna(0)
    data_label_postive = data[data['ROBOT'] == 1].copy()
    data_label_negtive = data[data['ROBOT'] == 0].copy()

    # 对阳性数据增加冗余处理
    duplicate_poitive_data = data_label_postive[data_label_postive['NUMBER_OF_REQUESTS'] > 2].copy()
    selected_duplicated_positive_data = duplicate_poitive_data.sample(n = (len(duplicate_poitive_data) // 5) * 3, axis=0)
    data_label_postive = data_label_postive.append(selected_duplicated_positive_data)
    data_label_postive_size = len(data_label_postive)

    # mean_colounm = data[data['NUMBER_OF_REQUESTS'] > 1]
    # size_number = mean_colounm['NUMBER_OF_REQUESTS'].mean(axis=0)
    data_negtive_sample = data_label_negtive.sample(n = data_label_postive_size*3, replace=False, axis=0)

    new_data = data_label_postive.append(data_negtive_sample)
    new_data = new_data.sample(frac=1)

    features = new_data.drop(data.columns[0], axis=1).drop(['REQUEST_RESOURCE', 'ROBOT', 'ID'], axis=1)
    time_series = features['USER_TIME_SERIES']
    features = features.drop(['USER_TIME_SERIES'], axis=1)
    return features.values, new_data['ROBOT'].apply(int).values, time_series.values


def read_test_data(path, label = 1):
    df_chunk = pd.read_csv(path, chunksize=1e6, iterator=True, header=0)
    data = pd.concat([chunk for chunk in df_chunk]).fillna(0)
    data = data[data['ROBOT'] == label]

    features = data.drop(data.columns[0], axis=1).drop(['REQUEST_RESOURCE', 'ROBOT', 'ID'], axis=1)
    time_series = features['USER_TIME_SERIES']
    features = features.drop(['USER_TIME_SERIES'], axis=1)

    return features.values, data['ROBOT'].values, time_series.values

def rand_mask(x, p=0.1):
    # 保留id，剩下部分按概率p随机mask掉一部分特征
    ids_mask = [True, True]
    ids_mask.extend(np.random.rand(152) > p)
    return x * np.array(ids_mask)


def evaluate_score(res_csv_path, truth_csv_path):
    # "/root/tianchi_entry/result.csv"
    df_pred = pd.read_csv(res_csv_path, names=[
                          'uuid', 'time_in', 'time_out', 'pred'])
    df_truth = pd.read_csv(truth_csv_path, names=['uuid', 'label'])
    time_diff = (df_pred['time_out'] - df_pred['time_in'])
    time_mask = time_diff <= 500
    f1 = f1_score(df_truth['label'][time_mask], df_pred['pred'][time_mask])
    ratio = time_mask.mean()
    print(f'avg time: {time_diff.mean()}')
    print(f'f1 score: {f1}')
    print(f'ratio   : {ratio}')
    print(f'score   : {f1 * ratio}')


def find_best_threshold(y_true, y_pred, l=0.1, r=0.6, p=0.01):
    thresholds = np.arange(l, r, p)
    print(f"以精度为{p}在[{thresholds[0]},{thresholds[-1]}]范围内搜索F1最佳阈值", end=">>")
    fscore = np.zeros(shape=(len(thresholds)))
    for index, elem in enumerate(thresholds):
        thr2sub = np.vectorize(lambda x: 1 if x > elem else 0)
        y_preds = thr2sub(y_pred)
        fscore[index] = f1_score(y_true, y_preds)
    index = np.argmax(fscore)
    thresholdOpt = thresholds[index]
    fscoreOpt = round(fscore[index], ndigits=8)
    print(f'最佳阈值:={thresholdOpt}->F1={fscoreOpt}')
    return thresholdOpt, fscoreOpt


def get_optimal_Fscore(model, x, y):
    # 由粗到细查找会比较快
    pred = model.predict(x)
    p = 0.1
    thr, best_fscore = find_best_threshold(y, pred, 0.1, 0.9, p)
    p /= 5
    thr, best_fscore = find_best_threshold(
        y, pred, round(thr-0.1, 4), round(thr+0.1, 4), p)
    p /= 5
    thr_optimal, best_fscore = find_best_threshold(
        y, pred, round(thr - 0.05, 4), round(thr + 0.05, 4), p)
    return thr_optimal, best_fscore


def reduce_mem_usage(df):
    # start_mem = df.memory_usage().sum()
    # print(f'压缩内存>>{start_mem:.2f}', end="->")
    for col in df.columns:
        col_type = df[col].dtype

        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)

    # end_mem = df.memory_usage().sum()
    # print(f'{end_mem:.2f} MB', end=" ")
    # print(f'- {(100*(start_mem - end_mem) / start_mem):.1f}%', end=" -> ")
    return df


def plot_model_history_curve(model_history):
    import matplotlib.pyplot as plt
    plt.plot(model_history.history['auprc'])
    plt.plot(model_history.history['val_auprc'])
    plt.title('ali_model auprc')
    plt.ylabel('auprc')
    plt.xlabel('epoch')
    plt.legend(['train-auprc', 'val-auprc'], loc='best')
    plt.show()

    plt.plot(model_history.history['loss'])
    plt.plot(model_history.history['val_loss'])
    plt.title('ali_model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train-loss', 'val-loss'], loc='best')
    plt.show()

    plt.plot(model_history.history['auc'])
    plt.plot(model_history.history['val_auc'])
    plt.title('ali_model auc')
    plt.ylabel('auc')
    plt.xlabel('epoch')
    plt.legend(['train-auc', 'val-auc'], loc='best')
    plt.show()

    plt.plot(model_history.history['batchwise_avg_f1'])
    plt.plot(model_history.history['val_batchwise_avg_f1'])
    plt.title('ali_model batchwise_avg_f1')
    plt.ylabel('batchwise_avg_f1')
    plt.xlabel('epoch')
    plt.legend(['train-f1', 'val-f1'], loc='best')
    plt.show()
