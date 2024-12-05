import time
import logging
import os
from collections import defaultdict


def get_logger(dir, tile):
    os.makedirs(dir, exist_ok=True)
    log_file = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    log_file = os.path.join(dir, "{}_{}.log".format(log_file, tile))

    logger = logging.getLogger()
    logger.setLevel('DEBUG')
    BASIC_FORMAT = "%(levelname)s:%(message)s"
    # DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(BASIC_FORMAT)
    chlr = logging.StreamHandler()
    chlr.setFormatter(formatter)

    fhlr = logging.FileHandler(log_file) 
    fhlr.setFormatter(formatter)
    fhlr.setLevel('INFO') 

    logger.addHandler(chlr)
    logger.addHandler(fhlr)
    return logger



class Meter:
    def __init__(self):
        self.reset()

    def add(self, value):
        self.values.append(value)

    def mean(self):
        return sum(self.values) / len(self.values) if self.values else 0.0

    def std(self):
        if len(self.values) < 2:
            return 0.0
        mean_val = self.mean()
        variance = sum((x - mean_val) ** 2 for x in self.values) / (len(self.values) - 1)
        return variance ** 0.5

    def reset(self):
        self.values = []



class MetricsManager:
    def __init__(self):
        self.meters = defaultdict(Meter)

    def __getitem__(self, key):
        return self.meters[key]

    def reset(self):
        for meter in self.meters.values():
            meter.reset()





class AverageMeter(object):
    """Computes and stores the average and current/max/min value"""
    def __init__(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0
        self.max = -1e10
        self.min = 1e10
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0
        self.max = -1e10
        self.min = 1e10

    def update(self, val, n=1):
        self.max = max(val, self.max)
        self.min = min(val, self.min)
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
