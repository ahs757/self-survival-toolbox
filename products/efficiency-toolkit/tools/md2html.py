#!/usr/bin/env python3
"""
Markdown转HTML工具 - 一键转换格式
作者: 效率工具包
版本: 2.0
"""

import os
import re
import argparse
from pathlib import Path

class MarkdownToHTML:
    def __init__(self, template=None):
        self.template = template or self.get_default_template()

    def get_default_template(self):
        """获取默认HTML模板"""
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }}
        h1 {{ font-size: 2em; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        h2 {{ font-size: 1.5em; border-bottom: 1px solid #eee; padding-bottom: 8px; }}
        h3 {{ font-size: 1.25em; }}
        p {{ margin: 1em 0; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        code {{
            background-color: #f8f8f8;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f8f8f8;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            margin: 0;
            padding-left: 20px;
            color: #666;
        }}
        ul, ol {{ padding-left: 20px; }}
        li {{ margin: 0.5em 0; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .highlight {{
            background-color: #fff3cd;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
        }}
        .footer {{
            margin-top: 2em;
            padding-top: 1em;
            border-top: 1px solid #eee;
            color: #666;
            font-size: 0.9em;
            text-align: center;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 5px;
        }}
        .toc {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .toc ul {{
            list-style: none;
            padding-left: 0;
        }}
        .toc li {{
            margin: 5px 0;
        }}
        .toc a {{
            color: #2c3e50;
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
        <div class="footer">
            <p>由效率工具包生成 | {date}</p>
        </div>
    </div>
</body>
</html>'''

    def parse_markdown(self, md_text):
        """解析Markdown文本"""
        lines = md_text.split('\n')
        html_lines = []
        in_code_block = False
        in_list = False
        list_type = None
        in_table = False
        table_headers = []
        table_rows = []

        i = 0
        while i < len(lines):
            line = lines[i]

            # 代码块处理
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    lang = line.strip()[3:].strip()
                    html_lines.append(f'<pre><code class="language-{lang}">')
                else:
                    in_code_block = False
                    html_lines.append('</code></pre>')
                i += 1
                continue

            if in_code_block:
                html_lines.append(self.escape_html(line))
                i += 1
                continue

            # 空行处理
            if not line.strip():
                if in_list:
                    html_lines.append('</ul>' if list_type == 'ul' else '</ol>')
                    in_list = False
                    list_type = None
                if in_table:
                    html_lines.extend(self.render_table(table_headers, table_rows))
                    in_table = False
                    table_headers = []
                    table_rows = []
                html_lines.append('')
                i += 1
                continue

            # 标题处理
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                if level <= 6:
                    title = line.lstrip('#').strip()
                    html_lines.append(f'<h{level}>{self.parse_inline(title)}</h{level}>')
                    i += 1
                    continue

            # 引用处理
            if line.startswith('>'):
                quote_text = line[1:].strip()
                html_lines.append(f'<blockquote>{self.parse_inline(quote_text)}</blockquote>')
                i += 1
                continue

            # 列表处理
            if re.match(r'^[-*+]\s', line):
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
                    list_type = 'ul'
                item = re.sub(r'^[-*+]\s', '', line)
                html_lines.append(f'<li>{self.parse_inline(item)}</li>')
                i += 1
                continue

            if re.match(r'^\d+\.\s', line):
                if not in_list:
                    html_lines.append('<ol>')
                    in_list = True
                    list_type = 'ol'
                item = re.sub(r'^\d+\.\s', '', line)
                html_lines.append(f'<li>{self.parse_inline(item)}</li>')
                i += 1
                continue

            # 表格处理
            if '|' in line and line.strip().startswith('|'):
                if not in_table:
                    in_table = True
                    # 解析表头
                    cells = [cell.strip() for cell in line.split('|')[1:-1]]
                    table_headers = cells
                    i += 1
                    continue
                else:
                    # 跳过分隔行
                    if re.match(r'^[\s|:-]+$', line):
                        i += 1
                        continue
                    # 解析数据行
                    cells = [cell.strip() for cell in line.split('|')[1:-1]]
                    table_rows.append(cells)
                    i += 1
                    continue

            # 水平线处理
            if re.match(r'^[-*_]{3,}$', line.strip()):
                html_lines.append('<hr>')
                i += 1
                continue

            # 普通段落
            if in_list:
                html_lines.append('</ul>' if list_type == 'ul' else '</ol>')
                in_list = False
                list_type = None

            html_lines.append(f'<p>{self.parse_inline(line)}</p>')
            i += 1

        # 清理未关闭的标签
        if in_list:
            html_lines.append('</ul>' if list_type == 'ul' else '</ol>')
        if in_table:
            html_lines.extend(self.render_table(table_headers, table_rows))

        return '\n'.join(html_lines)

    def parse_inline(self, text):
        """解析行内元素"""
        # 粗体
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text)

        # 斜体
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)

        # 删除线
        text = re.sub(r'~~(.*?)~~', r'<del>\1</del>', text)

        # 行内代码
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)

        # 链接
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)

        # 图片
        text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">', text)

        return text

    def escape_html(self, text):
        """转义HTML特殊字符"""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#39;')
        return text

    def render_table(self, headers, rows):
        """渲染表格"""
        html = ['<table>']

        # 表头
        if headers:
            html.append('<thead><tr>')
            for header in headers:
                html.append(f'<th>{self.parse_inline(header)}</th>')
            html.append('</tr></thead>')

        # 表体
        if rows:
            html.append('<tbody>')
            for row in rows:
                html.append('<tr>')
                for cell in row:
                    html.append(f'<td>{self.parse_inline(cell)}</td>')
                html.append('</tr>')
            html.append('</tbody>')

        html.append('</table>')
        return html

    def extract_title(self, md_text):
        """提取标题"""
        lines = md_text.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return "无标题文档"

    def convert(self, md_text, title=None):
        """转换Markdown到HTML"""
        if title is None:
            title = self.extract_title(md_text)

        content = self.parse_markdown(md_text)

        from datetime import datetime
        date_str = datetime.now().strftime('%Y-%m-%d %H:%M')

        html = self.template.format(
            title=title,
            content=content,
            date=date_str
        )

        return html

    def convert_file(self, input_file, output_file=None):
        """转换文件"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                md_text = f.read()
        except UnicodeDecodeError:
            with open(input_file, 'r', encoding='gbk') as f:
                md_text = f.read()

        # 提取标题
        title = self.extract_title(md_text)

        # 转换
        html = self.convert(md_text, title)

        # 输出
        if output_file is None:
            output_file = Path(input_file).with_suffix('.html')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_file

def main():
    parser = argparse.ArgumentParser(description='Markdown转HTML工具')
    parser.add_argument('input', help='输入Markdown文件路径')
    parser.add_argument('--output', '-o', help='输出HTML文件路径')
    parser.add_argument('--title', help='自定义标题')
    parser.add_argument('--template', help='自定义HTML模板文件')

    args = parser.parse_args()

    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}")
        return

    # 加载模板
    template = None
    if args.template and os.path.exists(args.template):
        with open(args.template, 'r', encoding='utf-8') as f:
            template = f.read()

    # 创建转换器
    converter = MarkdownToHTML(template)

    # 转换文件
    output_file = converter.convert_file(args.input, args.output)

    print(f"转换成功: {args.input} -> {output_file}")

if __name__ == '__main__':
    main()