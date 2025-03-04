from PyPDF2 import PdfReader, PdfWriter

#提取pdf部分页面的内容
def extract_pages(input_pdf_path, output_pdf_path, start_page, end_page):
    # 读取PDF文件
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # 确保页面范围在有效范围内
    if start_page < 1 or end_page > len(reader.pages) or start_page > end_page:
        raise ValueError("Invalid page range")

    # 添加指定范围的页面到新的PDF
    for page_num in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_num])

    # 将新PDF写入文件
    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)

# 示例用法
input_pdf = "/Users/Jenius/Desktop/测算/合肥滨湖国家森林公园4A级景区旅游基础设施建设项目申报材料2.12.pdf"
output_pdf = "/Users/Jenius/Desktop/测算/财评报告.pdf"
start_page = 432  # 从第3页开始
end_page = 470    # 到第5页结束

extract_pages(input_pdf, output_pdf, start_page, end_page)