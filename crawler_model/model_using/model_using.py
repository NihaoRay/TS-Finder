import numpy as np
import pandas as pd
import torch
from d2l import torch as d2l
from torch import nn
from torch.utils import data
from sklearn.metrics import f1_score, roc_auc_score, recall_score, precision_score

from utils_using import reduce_mem_usage, read_data


def init_gru_state(batch_size, num_hiddens, device):
    return (torch.zeros((batch_size, num_hiddens), device=device), )

class DetectionModel(nn.Module):
    def __init__(self, input_size, num_hiddens):
        super(DetectionModel, self).__init__()

        self.rnn = nn.LSTM(input_size, num_hiddens, num_layers=3, dropout=0.3)
        self.attention = d2l.AdditiveAttention(num_hiddens, num_hiddens, num_hiddens, dropout=0.3)
        self.dense = nn.Linear(num_hiddens, 1)

        self.bn1 = nn.BatchNorm1d(26)
        self.linear1 = nn.Linear(42, 128)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.5)

        self.linear2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)
        # self.bn2 = nn.LayerNorm(64)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.3)

        self.linear3 = nn.Linear(64, 32)
        self.bn3 = nn.BatchNorm1d(32)
        self.relu3 = nn.ReLU()
        self.dropout3 = nn.Dropout(0.3)

        self.linear4 = nn.Linear(32, 8)
        self.bn4 = nn.BatchNorm1d(8)
        self.relu4 = nn.ReLU()
        self.dropout4 = nn.Dropout(0.3)

        self.output = nn.Linear(8, 2)

    def forward(self, inputs, time_series_feature):
        # rnn训练访问时间序列，得到每个时间步骤的结果与时间序列
        enc_ouputs, (state, _) = self.rnn(time_series_feature)
        query = torch.unsqueeze(state[-1], dim=1)
        rnn_outpus = enc_ouputs.permute(1, 0, 2)
        # 使用注意力融合 最后的隐藏层输出与每个时间步骤的RNN输出
        context = self.attention(query, rnn_outpus, rnn_outpus, None)

        x = self.bn1(inputs)

        x = torch.cat((context, torch.unsqueeze(x, dim = 1)), dim=-1).squeeze(1)
        # torch.cat((context, torch.unsqueeze(x, dim=1)), dim=-1).squeeze(1)

        x = self.linear1(x)
        x = self.relu1(x)
        x_res = self.dropout1(x)
        x = x_res + x

        x = self.linear2(x)
        x = self.relu2(x)
        x = self.bn2(x)
        x_res = self.dropout2(x)
        x = x_res + x

        x = self.linear3(x)
        x = self.relu3(x)
        x_res = self.dropout3(x)
        x = x_res + x

        x = self.linear4(x)
        x = self.relu4(x)
        x_res = self.dropout4(x)
        x = x_res + x

        return self.output(x)


class DataSet(torch.utils.data.Dataset):
    def __init__(self, features, labels, time_series):
        assert len(features) == len(labels) == len(time_series)
        self.features = features
        self.labels = labels
        self.time_series = time_series

    def __getitem__(self, index):
        return (self.features[index], self.labels[index], self.time_series[index])

    def __len__(self):
        return len(self.features)


def train(train_path):
    features, labels, time_series = read_data(train_path)
    features = torch.tensor(features, dtype=torch.float32)
    labels = torch.tensor(labels)

    time_series_arr = torch.tensor([])
    time_series_valid_length = []
    num_steps = 180 #rnn步长的长度
    for time_item in time_series: # 对访问时间序列 进行填充 使得其符合rnn计算格式
        time_item_arr = np.array(time_item.split(','), dtype=float)
        arr = truncate_pad(time_item_arr, num_steps, 0)
        time_series_arr = torch.cat((time_series_arr, torch.tensor(arr, dtype=torch.float32).unsqueeze(0)), 0)

        time_item_arr_length = len(time_item_arr) + 1
        if len(time_item_arr) > num_steps:
            time_item_arr_length = num_steps
        time_series_valid_length.append(time_item_arr_length)

    spilt_len = len(features) // 10
    x_train = features[0:spilt_len * 7]
    y_train = labels[0:spilt_len * 7]
    time_series_train = time_series_arr[0:spilt_len * 7]

    x_test = features[spilt_len * 7:]
    y_test = labels[spilt_len * 7:]
    time_series_test = time_series_arr[spilt_len * 7:]

    loss = nn.CrossEntropyLoss()
    devices = d2l.try_all_gpus()

    net = DetectionModel(1, 16)

    trainer = torch.optim.Adam(net.parameters(), lr=0.0025) # 0.001 学习率的设置

    batch_size = 128
    num_epochs = 240

    # 加载训练数据集合
    train_dataset = DataSet(x_train, y_train, time_series_train)
    test_dataset = DataSet(x_test, y_test, time_series_test)

    train_iter = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=True, num_workers=4)
    test_iter = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=True, drop_last=True, num_workers=4)


    net.to(devices[0])
    for epoch in range(num_epochs):
        metric = d2l.Accumulator(4)
        pred_all = []
        label_all = []
        for i, (features, labels, series) in enumerate(train_iter):
            # 修改时间序列的维度，使其适应rnn模型的
            time_series_feature = series.unsqueeze(-1).permute(1, 0, 2)
            l, acc, pred, y = train_batch_ch13(net, features, labels, time_series_feature, loss, trainer, devices)
            pred_all.extend(pred.cpu().numpy())  # 要将这个数据转移到cpu上
            label_all.extend(y.cpu().numpy())  # 要将这个数据转移到cpu上
            metric.add(l, acc, labels.shape[0], labels.numel())

            # if (i + 1) % (num_batches // 5) == 0 or i == num_batches - 1:
            #     animator.add(epoch + (i + 1) / num_batches,
            #                  (metric[0] / metric[2], metric[1] / metric[3],
            #                   None))

        test_acc = evaluate_accuracy_gpu(net, test_iter)
        # animator.add(epoch + 1, (None, None, test_acc))

        print(f'epoch {epoch + 1}, loss {metric[0] / metric[2]:.5f}, train acc '
              f'{metric[1] / metric[3]:.3f}, test acc {test_acc:.3f}')
        # 计算F1_score, AUC, Recall
        # print(f'epoch {epoch + 1}')
        print("F1-Score:{:.4f}".format(f1_score(label_all, pred_all)),
              "AUC:{:.4f}".format(roc_auc_score(label_all, pred_all)),
              "Recall:{:.4f}".format(recall_score(label_all, pred_all)))

    torch.save(net.state_dict(), 'detection_model_using')


def train_batch_ch13(net, X, y, time_series_feature, loss, trainer, devices):
    if isinstance(X, list):
        X = [x.to(devices[0]) for x in X]
    else:
        X = X.to(devices[0])
    y = y.to(devices[0])
    time_series_feature = time_series_feature.to(devices[0])

    net.train()
    trainer.zero_grad()
    pred = net(X, time_series_feature)
    l = loss(pred, y)
    l.sum().backward()
    trainer.step()
    train_loss_sum = l.sum()
    train_acc_sum = d2l.accuracy(pred, y)
    return train_loss_sum, train_acc_sum, d2l.argmax(pred, axis=1), y



def truncate_pad(line, num_steps, padding_token):
    if len(line) > num_steps:
        new_line = line[:num_steps - 1]
        new_line = np.append(new_line, 1.0)
        return new_line # Truncate
    if len(line) == num_steps:
        if line[-1] == 0:
            line[-1] = 1.0
        return line
    line_new = np.append(line, 1.0)
    return np.append(line_new, [padding_token] * (num_steps - len(line) - 1))  # Pad

def evaluate_accuracy_gpu(net, data_iter, device=None):
    """Compute the accuracy for a model on a dataset using a GPU.

    Defined in :numref:`sec_lenet`"""
    if isinstance(net, nn.Module):
        net.eval()  # Set the model to evaluation mode
        if not device:
            device = next(iter(net.parameters())).device
    # No. of correct predictions, no. of predictions
    metric = d2l.Accumulator(2)

    with torch.no_grad():
        for X, y, time_series_futures in data_iter:
            time_series_feature = time_series_futures.unsqueeze(-1).permute(1, 0, 2)
            time_series_feature = time_series_feature.to(device)
            if isinstance(X, list):
                # Required for BERT Fine-tuning (to be covered later)
                X = [x.to(device) for x in X]
            else:
                X = X.to(device)
            y = y.to(device)
            metric.add(d2l.accuracy(net(X, time_series_feature), y), d2l.size(y))
    return metric[0] / metric[1]


if __name__ == '__main__':
    file_name = 'out.csv'
    dataset_folder  = '/home/chenrui/localworkspace/ml_dataset/ml_dataflow/'
    train(dataset_folder + file_name)
