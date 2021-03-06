# coding:utf8
import sys
import os
import torch as t
from generation.data import get_data
from generation.model import PoetryModel
from torch import nn
from generation.utils import Visualizer
import tqdm
from torchnet import meter
import ipdb
# import main
from generation.main import Config
from generation.main import gen
import numpy as np
from project_config import PROJECT_ROOT_PATH
PICKLE_PATH = os.path.join(PROJECT_ROOT_PATH,"generation/tang.npz")
MODEL_PATH = os.path.join(PROJECT_ROOT_PATH,"generation/checkpoints/tang_199.pth")

def test(boy_name, girl_name):
    opt = Config()
    if boy_name == "张立":
        opt.prefix_words = "何当共剪西窗烛，却话巴山夜雨时。"
    elif boy_name == "李鸿斌":
        # opt.prefix_words = "同房昨夜停红烛，待晓堂前拜舅姑。"
        # opt.prefix_words="月落乌啼霜满天，江枫渔火对愁眠。"
        opt.prefix_words="在天愿作比翼鸟，在地愿为连理枝。"
    elif boy_name == "唐梅芝":
        opt.prefix_words = "此情可待成追忆，只是当时已惘然。"
    elif boy_name == "张一山":
        opt.prefix_words = "梦念伊人肝肠断，恋花怀玉迎料峭。"
    else:
        pool =  ["何当共剪西窗烛，却话巴山夜雨时。", "人生若只如初见，何事秋风悲画扇。",
    "借问江潮与海水，何似君情与妾心。", "月轮已落尚残光，一似西山没夕阳。",
    "次第长庚都落去，日华犹未出扶桑。", "长庚初让月先行，不料姮娥也世情。",
    "笑杀桑根甘瓠苗，乱它桑叶上它条。", "州在三峰最上头，上头高处更高楼。",
    "一雨飞来四天黑，乱云遮断万峰青。"]
        opt.prefix_words = np.random.choice(pool,1,True)[0]
        # opt.prefix_words = "借问江潮与海水，何似君情与妾心。"
    opt.data_path = 'data/'
    opt.pickle_path = PICKLE_PATH  # 预处理好的二进制文件
    opt.author = None  # 只学习某位作者的诗歌
    opt.constrain = None  # 长度限制
    opt.category = 'poet.tang'  # 类别，唐诗还是宋诗歌(poet.song)
    opt.lr = 1e-3
    opt.weight_decay = 1e-4
    opt.use_gpu = False
    opt.epoch = 20
    opt.batch_size = 128
    opt.maxlen = 125  # 超过这个长度的之后字被丢弃，小于这个长度的在前面补空格
    opt.plot_every = 20  # 每20个batch 可视化一次
    opt.env = 'poetry'  # visdom env
    opt.max_gen_len = 200  # 生成诗歌最长长度
    opt.debug_file = '/tmp/debugp'
    opt.model_path = MODEL_PATH  # 预训练模型路径
    tran_dict = {"高梽强": "高志强", "胡钰培": "胡玉培", "张鑫": "张金", "谭官鑫": "谭官金", "覃营晟": "覃营盛", "张琦": "张奇", "刘晗": "刘含"}
    if boy_name in tran_dict: boy_name = tran_dict[boy_name]
    if girl_name in tran_dict: girl_name = tran_dict[girl_name]
    if len(girl_name) == 2:
        opt.start_words = "我爱" + girl_name
    elif len(girl_name) == 3:
        opt.start_words = "爱" + girl_name
    opt.acrostic = True  # 是否是藏头诗
    opt.model_prefix = 'checkpoints/tang'  # 模型保存路径
    res = gen(opt)
    return res

if __name__ == '__main__':
    res = test("唐梅芝","刘昊然")
    print(res)