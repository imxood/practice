import os
import time
import random
import argparse
from pprint import pprint
import multiprocessing as mp


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--enable', type=bool, default=False)
    parser.add_argument('--devices', type=str, required=True)
    parser.add_argument('--count', type=int, default=0)
    # 如果有'--names', 任意多个参数 --- [type]
    parser.add_argument('--names', type=str, nargs='*')
    # 如果有'--props', 那么至少一个参数 --- [type]
    parser.add_argument('--props', type=str, nargs='+')
    # 如果有'--attrs', 最多一个参数 --- type
    parser.add_argument('--attrs', type=str, nargs='?')
    return parser.parse_args()


def task(args):

    # 参数解包
    data, share_datas = args

    time_start = time.time()

    time.sleep(0.5)
    data['a'] = random.randint(0, 10000)
    share_datas.append(data)
    time.sleep(0.5)

    time_end = time.time()

    print('[%d]time_diff: %f' % (os.getpid(), time_end - time_start))


if __name__ == "__main__":

    datas = [{'a': d} for d in range(5)]

    option = parse_args()
    pprint(option)

    time_start = time.time()

    with mp.Manager() as mng:

        share_datas = mng.list()

        with mp.Pool(2) as p:
            tasks_args = [(data, share_datas) for data in datas]
            p.map(task, tasks_args)

        # for data in datas:
        #     print(data['a'])
        time_end = time.time()

        print('[%d]time_start: %f' % (os.getpid(), time_start))
        print('[%d]time_end: %f' % (os.getpid(), time_end))
        print('[%d]time_diff: %f' % (os.getpid(), time_end - time_start))

        print('len: ', len(share_datas))
