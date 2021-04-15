#!/user/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import pandas as pd

starttime = datetime.datetime.now()

if __name__ == '__main__':

    filenames_in = '/Users/serein_x/Desktop/InstagrameMoniter/scraper'  # 输入文件的文件地址
    filenames_out = '/Users/serein_x/Desktop/InstagrameMoniter/'  # 新文件的地址
    for files in os.walk(filenames_in):
        file = files[2]
        for i in range(len(file)):
            name = file[i]
            domain1 = os.path.abspath(filenames_in)  # 待处理文件位置
            info = os.path.join(domain1, name)  # 拼接出待处理文件名字
            print(info, "开始处理")
            df = pd.DataFrame(pd.read_csv(info, header=None, names=['id', 'username', 'name']))

            df_id = df[['id']]
            id_top10 = df_id.loc[:, 'id'].value_counts().head(10)  # 统计id列重复值的个数，并输出top10
            domain2 = os.path.abspath(filenames_out)  # 处理完文件保存地址
            for i in range(len(id_top10.index)):  # 不同的id循环处理
                id= id_top10 .index[i]  # 取id
                id_row = df[df['id'] == id]   # 取id所在行数据
                id_name = str(id) + '.csv'  # 生成新csv文件名
                outfo = os.path.join(domain2, id_name)  # 拼接出新文件名字
                if os.path.exists(outfo) is False:  # 判断文件是否存在
                    # id_row.to_csv(outfo, header=None, index=None, encoding='utf-8')   # 不存在，创建新的csv
                    pass
                else:   # 存在，合并到已有csv
                    id_exists= pd.DataFrame(pd.read_csv(outfo, header=None, names=['**', 'id', '**',
                                                                    '**', '**', '**', '**']))
                    id_new= pd.concat([id_exists, id_row ])   # 合并
                    id_new.to_csv(outfo, header=None, index=None, encoding='utf-8')   # 保存合并后的csv

            print(info, "处理完")

endtime = datetime.datetime.now()
print(endtime - starttime)
