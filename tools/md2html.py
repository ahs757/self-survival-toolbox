#!/usr/bin/env python3
"""
📝 Markdown 转 HTML 工具
轻量级 Markdown 转 HTML 转换器，支持代码高亮、表格、TOC

用法:
    python md2html.py input.md [-o output.html] [--template minimal|blog|doc]

作者: AI Self-Survival Project
许可证: MIT
"""

import re
import sys
import argparse
from pathlib import Path

# HTML 模板
TEMPLATES = {
    'minimal': '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
pre {{ background: #f4f4f4; padding: 16px; border-radius: 4px; overflow-x: auto; }}
code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 3px; font-size: 0.9em; }}
pre code {{ background: none; padding: 0; }}
blockquote {{ border-left: 4px solid #ddd; margin: 0; padding-left: 16px; color: #666; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #f4f4f4; }}
img {{ max-width: 100%; }}
</style>
</head>
<body>
{content}
</body>
</html>''',

    'blog': '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Georgia', 'Noto Serif SC', serif; background: #fafafa; color: #333; line-height: 1.8; }}
.container {{ max-width: 720px; margin: 0 auto; padding: 40px 20px; }}
header {{ margin-bottom: 40px; border-bottom: 1px solid #eee; padding-bottom: 20px; }}
h1 {{ font-size: 2.2em; margin-bottom: 10px; color: #1a1a1a; }}
.meta {{ color: #888; font-size: 0.9em; }}
h2 {{ margin-top: 40px; margin-bottom: 16px; font-size: 1.5em; }}
h3 {{ margin-top: 30px; margin-bottom: 12px; font-size: 1.2em; }}
p {{ margin-bottom: 16px; }}
pre {{ background: #2d2d2d; color: #f8f8f2; padding: 20px; border-radius: 8px; overflow-x: auto; margin: 20px 0; }}
code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
pre code {{ background: none; padding: 0; }}
blockquote {{ border-left: 3px solid #333; margin: 20px 0; padding: 10px 20px; background: #f9f9f9; }}
table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
th, td {{ border: 1px solid #ddd; padding: 12px; }}
th {{ background: #333; color: white; }}
a {{ color: #0066cc; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
footer {{ margin-top: 60px; padding-top: 20px; border-top: 1px solid #eee; color: #888; font-size: 0.9em; }}
</style>
</head>
<body>
<div class="container">
<header>
<h1>{title}</h1>
<div class="meta">{date} · {author}</div>
</header>
{content}
<footer>
<p>由 AI Self-Survival Project 生成</p>
</footer>
</div>
</body>
</html>''',

    'doc': '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; display: flex; }}
.sidebar {{ width: 250px; position: fixed; height: 100vh; overflow-y: auto; background: #f8f9fa; padding: 20px; border-right: 1px solid #eee; }}
.sidebar a {{ display: block; padding: 6px 0; color: #333; text-decoration: none; }}
.sidebar a:hover {{ color: #0066cc; }}
.main {{ margin-left: 270px; padding: 40px; max-width: 800px; }}
h1 {{ border-bottom: 2px solid #333; padding-bottom: 10px; }}
h2 {{ margin-top: 40px; border-bottom: 1px solid #eee; padding-bottom: 8px; }}
pre {{ background: #f4f4f4; padding: 16px; border-radius: 4px; overflow-x: auto; }}
code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
pre code {{ background: none; padding: 0; }}
table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px; }}
th {{ background: #f4f4f4; }}
</style>
</head>
<body>
<nav class="sidebar">{toc}</nav>
<div class="main">{content}</div>
</body>
</html>'''
}

def parse_markdown(md_text: str) -> tuple:
    """解析 Markdown 文本，返回 (title, html_content, toc)"""
    lines = md_text.split('\n')
    html_lines = []
    toc_items = []
    title = 'Untitled'
    in_code_block = False
    in_list = False
    in_table = False
    table_headers = []

    for line in lines:
        # 代码块
        if line.startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                lang = line[3:].strip()
                html_lines.append(f'<pre><code class="language-{lang}">')
                in_code_block = True
            continue

        if in_code_block:
            html_lines.append(escape_html(line))
            continue

        # 标题
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            if level == 1 and title == 'Untitled':
                title = text
            anchor = re.sub(r'[^\w\u4e00-\u9fff-]', '', text.lower().replace(' ', '-'))
            html_lines.append(f'<h{level} id="{anchor}">{text}</h{level}>')
            toc_items.append((level, text, anchor))
            continue

        # 表格
        if '|' in line and line.strip().startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if all(re.match(r'^[-:]+$', c) for c in cells):
                continue  # 分隔行
            if not in_table:
                table_headers = cells
                html_lines.append('<table><thead><tr>')
                for h in cells:
                    html_lines.append(f'<th>{h}</th>')
                html_lines.append('</tr></thead><tbody>')
                in_table = True
            else:
                html_lines.append('<tr>')
                for c in cells:
                    html_lines.append(f'<td>{c}</td>')
                html_lines.append('</tr>')
            continue
        elif in_table:
            html_lines.append('</tbody></table>')
            in_table = False

        # 分隔线
        if re.match(r'^[-*_]{3,}$', line.strip()):
            html_lines.append('<hr>')
            continue

        # 引用
        if line.startswith('>'):
            text = line[1:].strip()
            html_lines.append(f'<blockquote><p>{inline_format(text)}</p></blockquote>')
            continue

        # 无序列表
        if re.match(r'^[-*+]\s+', line):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{inline_format(line[2:].strip())}</li>')
            continue
        elif in_list:
            html_lines.append('</ul>')
            in_list = False

        # 有序列表
        ol_match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if ol_match:
            html_lines.append(f'<ol><li>{inline_format(ol_match.group(2))}</li></ol>')
            continue

        # 空行
        if not line.strip():
            html_lines.append('')
            continue

        # 普通段落
        html_lines.append(f'<p>{inline_format(line)}</p>')

    if in_table:
        html_lines.append('</tbody></table>')
    if in_list:
        html_lines.append('</ul>')

    # 生成 TOC
    toc_html = ''
    for level, text, anchor in toc_items:
        indent = '&nbsp;' * (level - 1) * 4
        toc_html += f'{indent}<a href="#{anchor}">{text}</a><br>\n'

    return title, '\n'.join(html_lines), toc_html

def inline_format(text: str) -> str:
    """行内格式化"""
    # 粗体+斜体
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # 粗体
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # 斜体
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # 删除线
    text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
    # 行内代码
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # 链接
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    # 图片
    text = re.sub(r'!\[(.+?)\]\((.+?)\)', r'<img src="\2" alt="\1">', text)
    return text

def escape_html(text: str) -> str:
    """转义 HTML 特殊字符"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def main():
    parser = argparse.ArgumentParser(description='📝 Markdown 转 HTML')
    parser.add_argument('input', help='输入 Markdown 文件')
    parser.add_argument('-o', '--output', help='输出 HTML 文件')
    parser.add_argument('--template', choices=['minimal', 'blog', 'doc'], default='minimal',
                       help='HTML 模板风格')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 文件不存在: {input_path}")
        sys.exit(1)

    md_text = input_path.read_text(encoding='utf-8')
    title, content, toc = parse_markdown(md_text)

    from datetime import datetime
    template = TEMPLATES[args.template]
    html = template.format(
        title=title,
        content=content,
        toc=toc,
        description=md_text[:200].replace('\n', ' '),
        date=datetime.now().strftime('%Y-%m-%d'),
        author='AI Assistant'
    )

    output_path = Path(args.output) if args.output else input_path.with_suffix('.html')
    output_path.write_text(html, encoding='utf-8')

    print(f"✅ 转换完成!")
    print(f"   输入: {input_path}")
    print(f"   输出: {output_path}")
    print(f"   模板: {args.template}")

if __name__ == '__main__':
    main()
