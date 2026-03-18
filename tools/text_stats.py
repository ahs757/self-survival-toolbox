#!/usr/bin/env python3
"""
📊 文本统计分析工具
分析文本文件的各种统计信息

用法:
    python text_stats.py file.txt
    python text_stats.py file.txt --word-freq --top 20
    echo "hello world" | python text_stats.py -

作者: AI Self-Survival Project
许可证: MIT
"""

import sys
import re
import argparse
from collections import Counter
from pathlib import Path

def analyze_text(text: str) -> dict:
    """分析文本统计信息"""
    lines = text.split('\n')
    words = re.findall(r'\b\w+\b', text.lower())
    chars = len(text)
    chars_no_space = len(text.replace(' ', '').replace('\n', ''))
    sentences = len(re.findall(r'[.!?。！？]+', text))
    paragraphs = len([p for p in text.split('\n\n') if p.strip()])

    # 中文字符
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 英文单词
    english_words = len(re.findall(r'[a-zA-Z]+', text))

    # 阅读时间估算（中文300字/分钟，英文200词/分钟）
    read_time_cn = chinese_chars / 300
    read_time_en = english_words / 200
    total_read_time = read_time_cn + read_time_en

    return {
        '总字符数': chars,
        '非空格字符': chars_no_space,
        '行数': len(lines),
        '非空行': len([l for l in lines if l.strip()]),
        '单词数': len(words),
        '英文单词': english_words,
        '中文字符': chinese_chars,
        '句子数': max(sentences, 1),
        '段落数': max(paragraphs, 1),
        '平均行长': round(chars / max(len(lines), 1), 1),
        '平均每词长度': round(chars_no_space / max(len(words), 1), 1),
        '预估阅读时间': f"{total_read_time:.1f} 分钟",
        '字数统计(中英混合)': chinese_chars + english_words,
    }

def word_frequency(text: str, top_n: int = 10) -> list:
    """词频统计"""
    words = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z]+', text.lower())
    return Counter(words).most_common(top_n)

def main():
    parser = argparse.ArgumentParser(description='📊 文本统计分析工具')
    parser.add_argument('input', help='输入文件路径 (- 表示stdin)')
    parser.add_argument('--word-freq', action='store_true', help='显示词频统计')
    parser.add_argument('--top', type=int, default=10, help='显示前N个高频词')
    parser.add_argument('--json', action='store_true', help='JSON格式输出')

    args = parser.parse_args()

    if args.input == '-':
        text = sys.stdin.read()
    else:
        path = Path(args.input)
        if not path.exists():
            print(f"❌ 文件不存在: {path}")
            sys.exit(1)
        text = path.read_text(encoding='utf-8')

    stats = analyze_text(text)

    if args.json:
        import json
        result = {**stats}
        if args.word_freq:
            result['词频'] = word_frequency(text, args.top)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*40}")
        print(f"📊 文本统计分析")
        print(f"{'='*40}")
        for key, value in stats.items():
            print(f"  {key}: {value}")

        if args.word_freq:
            print(f"\n🔤 词频统计 (Top {args.top}):")
            print(f"{'─'*30}")
            for word, count in word_frequency(text, args.top):
                bar = '█' * min(count, 20)
                print(f"  {word:>10} │ {count:>4} │ {bar}")

        print(f"\n{'='*40}")

if __name__ == '__main__':
    main()
