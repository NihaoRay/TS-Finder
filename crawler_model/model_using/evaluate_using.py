import numpy as np
import torch
from d2l import torch as d2l
from torch.utils import data
from torch import nn

from model_using import DetectionModel, DataSet
from utils_using import read_data, read_test_data




def evalute_using():
    devices = d2l.try_all_gpus()
    net = DetectionModel(1, 16).to(devices[0])
    net.load_state_dict(torch.load('detection_model_using'))
    net.eval()

    file_name = ''
    dataset_folder = '/home/chenrui/localworkspace/ml_dataset/ml_dataflow/'

    dataset_path = dataset_folder + file_name

    x, y, time_series = read_test_data(path=dataset_path, label=1)

    time_series_arr = torch.tensor([])
    time_series_valid_length = []
    num_steps = 180  # rnn步长的长度
    for time_item in time_series:
        time_item_arr = np.array(time_item.split(','), dtype=float)
        arr = truncate_pad(time_item_arr, num_steps, 0)
        time_series_arr = torch.cat((time_series_arr, torch.tensor(arr, dtype=torch.float32).unsqueeze(0)), 0)

        time_item_arr_length = len(time_item_arr) + 1
        if len(time_item_arr) > num_steps:
            time_item_arr_length = num_steps
        time_series_valid_length.append(time_item_arr_length)

    features = torch.tensor(x, dtype=torch.float32)
    labels = torch.tensor(y)


    test_dataset = DataSet(features, labels, time_series_arr)
    batch_size = 128

    train_iter = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=True, num_workers=4)

    test_acc = evaluate_accuracy_gpu(net, train_iter)

    print(test_acc)


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


if __name__ == '__main__':
    evalute_using()
