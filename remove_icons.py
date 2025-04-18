from bs4 import BeautifulSoup
import shutil
import os

def remove_bookmark_icons():
    # 备份原始文件
    backup_file = 'bookmarks.html.bak'
    shutil.copy2('bookmarks.html', backup_file)
    
    # 读取bookmarks.html文件
    with open('bookmarks.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # 找到所有带ICON属性的A标签
    for a_tag in soup.find_all('a'):
        if 'icon' in a_tag.attrs:
            del a_tag['icon']
    
    # 写入修改后的文件
    with open('bookmarks.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f'已备份原始文件到 {backup_file}')
    print('成功移除所有书签的ICON属性')

if __name__ == '__main__':
    remove_bookmark_icons()