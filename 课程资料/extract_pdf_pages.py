#!/usr/bin/env python3
"""
提取PDF特定页面的脚本
从intel-system-programming-manual.pdf提取第41-50页到Chapter1.pdf
"""

from pypdf import PdfReader, PdfWriter

def extract_pages(input_pdf, output_pdf, start_page, end_page):
    """
    从PDF中提取指定页面范围

    Args:
        input_pdf: 输入PDF文件路径
        output_pdf: 输出PDF文件路径
        start_page: 起始页码（从1开始）
        end_page: 结束页码（包含）
    """
    # 创建PDF读取器
    reader = PdfReader(input_pdf)

    # 创建PDF写入器
    writer = PdfWriter()

    # 获取总页数
    total_pages = len(reader.pages)
    print(f"原PDF总页数: {total_pages}")

    # 验证页码范围
    if start_page < 1 or end_page > total_pages:
        raise ValueError(f"页码范围错误！请输入1到{total_pages}之间的页码")

    if start_page > end_page:
        raise ValueError("起始页码不能大于结束页码")

    # 提取页面（注意：索引从0开始，所以需要减1）
    for page_num in range(start_page - 1, end_page):
        page = reader.pages[page_num]
        writer.add_page(page)
        print(f"提取第{page_num + 1}页")

    # 写入输出文件
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)

    extracted_pages = end_page - start_page + 1
    print(f"成功提取第{start_page}页到第{end_page}页，共{extracted_pages}页")
    print(f"输出文件: {output_pdf}")

if __name__ == "__main__":
    # 配置参数
    input_file = "《计算机网络》实验指导书(2023).pdf"
    output_file = "实验7.pdf"
    start = 73
    end = 105

    try:
        extract_pages(input_file, output_file, start, end)
    except Exception as e:
        print(f"错误: {e}")
