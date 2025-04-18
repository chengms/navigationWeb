import csv
from bs4 import BeautifulSoup

def extract_bookmarks(html_file):
    try:
        # 读取HTML文件
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f'成功读取{html_file}文件')
        
        # 解析HTML
        soup = BeautifulSoup(content, 'html.parser')
        bookmarks = []
        
        def process_folder(element, path=[]):
            if not element:
                return
            
            # 遍历所有dt元素（包括嵌套在p标签中的）
            for dt in element.find_all('dt', recursive=True):
                # 处理文件夹
                h3 = dt.find('h3')
                if h3:
                    folder_name = h3.get_text().strip()
                    current_path = path + [folder_name]
                    # 查找下一级dl（可能在dt后面的兄弟元素中）
                    next_dl = dt.find_next_sibling('dl')
                    if next_dl:
                        process_folder(next_dl, current_path)
                
                # 处理书签链接
                a = dt.find('a')
                if a and not h3:  # 确保这不是文件夹的标题
                    category_path = '/'.join(path) if path else '未分类'
                    
                    # 确定主分类
                    if any(x in category_path.lower() for x in ['公司', '企业']):
                        main_category = '企业工具'
                    elif any(x in category_path.lower() for x in ['go', 'python', 'java', '前端', 'ui']):
                        main_category = '开发资源'
                    elif any(x in category_path.lower() for x in ['github', 'gitee', 'coding', '开源']):
                        main_category = '开源社区'
                    elif any(x in category_path.lower() for x in ['云', '阿里云', '腾讯云']):
                        main_category = '云服务'
                    elif any(x in category_path.lower() for x in ['文档', '书籍', '教程', '课程']):
                        main_category = '学习资源'
                    elif any(x in category_path.lower() for x in ['工具', '站点']):
                        main_category = '实用工具'
                    else:
                        main_category = '其他资源'
                    
                    bookmark = {
                        '标题': a.get_text().strip(),
                        'URL': a.get('href', ''),
                        '添加时间': a.get('add_date', ''),
                        '原始分类': category_path,
                        '主分类': main_category
                    }
                    bookmarks.append(bookmark)
        
        # 从根dl标签开始处理
        root_dl = soup.find('dl')
        if root_dl:
            process_folder(root_dl)
            print(f'找到 {len(bookmarks)} 个书签')
        else:
            print('错误：未找到书签列表')
        
        return bookmarks
    
    except Exception as e:
        print(f'处理文件时出错：{str(e)}')
        return []

def save_bookmarks(bookmarks, output_file):
    try:
        # 按主分类和原始分类排序
        bookmarks.sort(key=lambda x: (x['主分类'], x['原始分类']))
        
        # 写入CSV文件
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['标题', 'URL', '添加时间', '原始分类', '主分类'])
            writer.writeheader()
            writer.writerows(bookmarks)
        
        print(f'成功保存 {len(bookmarks)} 个书签到 {output_file}')
        return True
    
    except Exception as e:
        print(f'保存文件时出错：{str(e)}')
        return False

def main():
    input_file = 'bookmarks.html'
    output_file = 'bookmarks.csv'
    
    # 提取书签
    bookmarks = extract_bookmarks(input_file)
    
    # 保存结果
    if bookmarks:
        save_bookmarks(bookmarks, output_file)

if __name__ == '__main__':
    main()