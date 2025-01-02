''' gen by: https://chat.deepseek.com/
输入文件`paperlist.xlsx`为一个表格，适用pandas进行处理，筛选出`category`列值为`Pretrain & Representation.`的所有行，解析其`Method`字段
'''
import pandas as pd
import os
import requests
import re
from tqdm import tqdm

def parse_args():    
    import argparse

    parser = argparse.ArgumentParser(description="Main")
    parser.add_argument("--input", type=str,  default="paperlist.xlsx") 
    parser.add_argument("--output", type=str,  default="pdf") 
    parser.add_argument("--category", type=str,  default=None) 
    args = parser.parse_args()
    return args
    
def parse_method(input_str):
    # 使用正则表达式解析标题和URL
    match = re.match(r'\[(.*?)\]\((https?://.*?)\)', input_str)

    if match:
        title = match.group(1)  # 标题
        url = match.group(2)    # URL
        return title, url
    return None, None

def replace_url_parts(url):
    """
    将字符串中的 /abs/ 替换为 /pdf/，将 /forum? 替换为 /pdf?
    
    参数:
    url (str): 需要替换的字符串
    
    返回:
    str: 替换后的字符串
    """
    # 替换 /abs/ 为 /pdf/
    url = url.replace('/abs/', '/pdf/')
    # 替换 /forum? 为 /pdf?
    url = url.replace('/forum?', '/pdf?')
    return url    


def download_pdf(file_path, url):
    """
    从 URL 下载 PDF 文件并保存到指定目录下，文件名为 name.pdf

    参数:
    dir (str): 保存文件的目录路径
    name (str): 保存的文件名（不含扩展名）
    url (str): 要下载的 PDF 文件的 URL

    返回:
    str: 保存的文件路径，如果下载失败则返回 None
    """

    if os.path.exists(file_path):
        return file_path

    try:
        # 发送 HTTP GET 请求下载文件
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        # 将文件内容写入本地文件
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        #print(f"文件已保存到: {file_path}")
        return file_path

    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")
        return None

def replace_invalid_chars(filename, spliter='_'):
    """
    将文件名中的非法字符替换为指定的分隔符。

    参数:
    filename (str): 原始文件名
    spliter (str): 替换非法字符的分隔符，默认为 '_'

    返回:
    str: 替换后的合法文件名
    """
    # 定义 Windows 文件名中非法的字符
    invalid_chars = r'[\\/:*?"<>|\0\t\n\r\x0b\x0c&%$#@!+=,;`\'\{\}\[\]()~]'
    
    # 使用正则表达式替换非法字符
    valid_filename = re.sub(invalid_chars, spliter, filename)
    
    # 去除文件名开头和结尾的空格或句点
    valid_filename = valid_filename.strip('. ')
    
    # 如果文件名为空，则返回一个默认的合法文件名
    if not valid_filename:
        valid_filename = 'untitled'
    
    # 检查文件名是否是 Windows 保留的设备名称
    reserved_names = {'CON', 'PRN', 'AUX', 'NUL', 
                      'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                      'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
    
    if valid_filename.upper() in reserved_names:
        valid_filename = spliter + valid_filename
    
    return valid_filename


def parse_text(args):
    # 读取文件内容
    with open('data/README.md', 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则表达式匹配<details>块
    pattern = re.compile(
        r'<details><summary><h2[^>]*>(.*?)</h2></summary>(.*?)</details>',
        re.DOTALL
    )

    # 初始化一个空的DataFrame来存储所有表格数据
    all_data = pd.DataFrame()

    # 遍历所有匹配的<details>块
    for match in pattern.findall(content):
        category = match[0].strip()  # 提取category
        table_content = match[1].strip()  # 提取表格内容

        # 将表格内容按行分割
        rows = table_content.split('\n')
        
        # 提取表头和数据
        header = [col.strip() for col in rows[0].split('|') if col.strip()]
        data = []
        for row in rows[2:]:  # 跳过表头和分隔线
            cols = [col.strip() for col in row.split('|') if col.strip()]
            if cols:
                data.append(cols)
        
        # 将数据转换为DataFrame
        df = pd.DataFrame(data, columns=header)
        
        # 添加category列
        df['category'] = category
        
        # 将当前表格数据添加到总数据中
        all_data = pd.concat([all_data, df], ignore_index=True)

    # 保存为Excel文件
    all_data.to_excel(args.input, index=False)
    print(f"表格已成功保存为:{args.input}")


def get_path_url(row, rootdir):
    category = row['category']
    method = row['Method']
    name, url = parse_method(method)
    url = replace_url_parts(url)
    save_dir = rootdir + '/' + replace_invalid_chars(category)
    
    # 构造完整的文件路径
    file_path = os.path.join(save_dir, f"{name}.pdf")
    return name, url, file_path
        
def download(args):
    # 读取Excel文件
    rootdir = args.output

    df = pd.read_excel(args.input)

    #category = 'Pretrain & Representation.'
    category = args.category
    if category:
        filtered_df = df[df['category'] == category]
    else:
        filtered_df = df
        
    #print(filtered_df)
    total = len(filtered_df)
    suceed = 0
    for index, row in tqdm(filtered_df.iterrows(), total=total):
        # print(row)
        name, url, file_path = get_path_url(row, rootdir)
        
        # 确保目录存在，如果不存在则创建
        os.makedirs(save_dir, exist_ok=True)
        save_path = download_pdf(file_path, url)
        if save_path:
            suceed += 1
            
    print(f'DONE {suceed}/{total} !')

def extract_brackets_content(text):
    """
    Extracts content within square brackets from a given string.

    Parameters:
    text (str): The input string from which to extract bracketed content.

    Returns:
    list: A list of strings containing the content within each pair of square brackets.
    """
    if text is None:
        return ''
    # Define the regex pattern to find content within brackets
    pattern = r'\[(.*?)\]'
    # Use re.findall to extract all matches
    matches = re.findall(pattern, text)
    return matches[0] if matches else ''
    
def refine_table(args):
    # 读取Excel文件
    rootdir = args.output

    df = pd.read_excel(args.input)
    #df.sort_values(by='Date', ascending=False, inplace=True)
    
    # 创建一个 Excel 写入对象
    writer = pd.ExcelWriter('output.xlsx', engine='openpyxl')

    # 将 DataFrame 写入 Excel
    df.to_excel(writer, index=False, sheet_name='Sheet1')

    # 获取 Excel 的工作表对象
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    total = len(df)
    suceed = 0
    for index, row in tqdm(df.iterrows(), total=total):
        name, url, file_path = get_path_url(row, rootdir)
        # B:Method
        link = file_path if os.path.exists(file_path) else url
        # replace
        cell = f'B{index+2}'
        # 设置超链接
        worksheet[cell].value = name  # 设置单元格内容
        worksheet[cell].hyperlink = link  # 设置超链接
        worksheet[cell].style = 'Hyperlink'  # 设置单元格样式为超链接
        # E:Code
        title, code_url = parse_method(row['Code'])
        cell = f'E{index+2}'
        worksheet[cell].value = title
        worksheet[cell].hyperlink = code_url 
        worksheet[cell].style = 'Hyperlink' 
        # G:Type
        cell = f'G{index+2}'
        worksheet[cell].value = extract_brackets_content(worksheet[cell].value)

    # 设置每列的宽度
    worksheet.column_dimensions['A'].width = 10
    worksheet.column_dimensions['B'].width = 20
    worksheet.column_dimensions['C'].width = 12
    worksheet.column_dimensions['D'].width = 130
    worksheet.column_dimensions['E'].width = 15
    worksheet.column_dimensions['F'].width = 20
    worksheet.column_dimensions['G'].width = 20
    # 保存 Excel 文件
    writer.save()    
    print(f'DONE !')
    

def main(args):
    parse_text(args)
    download(args)
    refine_table(args)
    
if __name__ == "__main__":
    args = parse_args()
    main(args)    