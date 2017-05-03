# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup


def remove_html_tag(content):
    soup = BeautifulSoup(content, 'lxml')
    return soup.get_text()


def get_units(content, units):
    data = remove_html_tag(content)
    units_str = ''.join(units)
    pattern = re.compile(r'[0-9o.]+[{}]+'.format(units_str))
    results = re.findall(pattern, data)
    results = [r for r in results if r.endswith(tuple(units))]
    results = [r.replace('o', '0') for r in results]
    return results


if __name__ == '__main__':
    # example
    content = """<p><span style="font-size: 16px;">
                本地块位于河北省和北京交界处，官厅湖南岸祈康公路路边，紧
                邻碧桂园官厅湖1号.香水湾.拉斐水岸.观澜墅.上古水郡几大别墅区，
                村口就有880公交车通往朱辛庄地铁口站，这里绿化面积高达80%以上，空气质量特别高，
                最适宜休闲度假.旅游.养老居住.在这一带买别墅客户大多都反映说这里的风水特别好，
                是居住最佳圣地。此宅基地东西长45米南北长5o2米共2340平米的少有的大院子，此地块在村
                口东墙外就是大片的海棠园区，南墙外就是乡村公路，西墙外是街道，非常独体的这莫一个院
                子发展改造空间特别大，可以建三层以下独体别墅，可以建农家乐等就是可以按自己的意愿
                去改造，另外在此地块大约50米处很快就会修一条8米宽公路通湖边的旅游大道，此地块还
                潜在被获拆迁款的机会，如拆迁其价值为：按一平米宅基地赔一平米楼房.按当地楼房价格
                6000左右就是2340平米*6000元=14040o000元，咋样潜力大不大。这就是此地块现实真实的
                现有条件。 准备永久性出售， 价格可以谈</span></p>"""
    print(remove_html_tag(content))
    print(get_units(content, ['米', '平米', '元']))
