"""
load_cfg.py
"""
import os


def load_cfg(cfg_file):
    result = {}
    # crnt_path = os.path.abspath('..')
    crnt_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..')
    print('load_cfg(): crnt_path=', crnt_path)
    cfg_path = os.path.join(crnt_path, 'config')
    file_path = os.path.join(cfg_path, cfg_file)
    if not os.path.exists(file_path):
        # print('出错：配置文件 {cf} 不存在'.format(cfg_file))
        print('出错：配置文件 {cf} 不存在'.format(cf=file_path))
        return result
    with open(file_path, 'r') as fp:
        for line in fp.readlines():
            if line[0] == '#' or len(line.strip())==0:
                continue
            cell = line.split('\t')
            result[cell[0].strip()] = cell[1].strip()
    print('load_cfg() result : ', result)
    return result
