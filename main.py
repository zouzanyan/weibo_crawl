import logging
import os
from concurrent.futures import ThreadPoolExecutor

from utils.cost_time import cost_time

import requests
import yaml


class CrawlAlbum:

    def __init__(self):
        self.config = yaml.load(open('config.yml'), Loader=yaml.Loader)
        self.headers = {
            'user-agent': 'Mozilla/5.0',
            'cookie': self.config['cookie']
        }
        # 原画图片请求地址
        self.pic_url = 'https://wx1.sinaimg.cn/large/'
        # 页面url列表
        self.album_url_list = []
        # 照片字典
        self.obj_dict_pic = {}
        # livephoto字典
        self.obj_dict_mov = {}

    def get_album(self, user_id):
        # 原画图片请求地址
        since_id = 0
        isbottom = False
        try:
            while not isbottom:
                # time.sleep(2)
                url = f'https://weibo.com/ajax/profile/getImageWall?uid={user_id}&sinceid={since_id}&has_album=true'
                response = requests.get(url, headers=self.headers)
                print('爬取中')

                if response.status_code == 200:
                    data = response.json()

                    since_id = data['data']['since_id']
                    self.album_url_list += data['data']['list']
                    # isbottom为true或since_id为0时表示页面全部加载完
                    isbottom = data['bottom_tips_visible'] | (not data['data']['since_id'])
                else:
                    logging.warning('网络异常')
        except Exception as e:
            logging.error(repr(e) + '\tcookie可能失效')

    def handle_album(self):
        for obj in self.album_url_list:
            try:
                if obj['type'] == 'pic':
                    url_pic_1 = self.pic_url + obj['pid'] + '.jpg'
                    self.obj_dict_pic.update({obj['pid']: url_pic_1})
                    continue
                if obj['type'] == 'livephoto':
                    self.obj_dict_mov.update({obj['pid']: obj['video']})
                    continue
            # 有个别返回的json没有'type'字段,作异常处理
            except Exception as e:
                url_pic_1 = self.pic_url + obj['pid'] + '.jpg'
                self.obj_dict_pic.update({obj['pid']: url_pic_1})
                # 默认logging的info级别不会显示,所以这个异常日志处理相当于没有
                logging.info(repr(e) + '此异常可忽略')
                continue

    def thread_download_src(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            for key, value in self.obj_dict_pic.items():
                executor.map(self.download, {key}, {value}, {'pic'})
            for key, value in self.obj_dict_mov.items():
                executor.map(self.download, {key}, {value}, {'mov'})

    def download(self, name, url, flag):
        content = requests.get(url, self.headers).content
        if flag == 'pic':
            with open(f'{name}.jpg', 'wb') as f:
                f.write(content)
        else:
            with open(f'{name}.mov', 'wb') as f:
                f.write(content)

    @cost_time('')
    def crawl_main(self, user_id):
        print(f'解析中......')
        self.get_album(user_id)
        self.handle_album()
        print(f'一共{len(self.obj_dict_pic) + len(self.obj_dict_mov)}张图片')
        # 新建下载文件夹
        if not os.path.exists(user_id):
            os.mkdir(user_id)
        os.chdir(user_id)
        print('下载到硬盘中......')
        self.thread_download_src()
        os.chdir('..')


if __name__ == '__main__':
    userid = input('---------------请在此粘贴微博用户的uid---------------\n')
    a = CrawlAlbum()
    a.crawl_main(userid)
