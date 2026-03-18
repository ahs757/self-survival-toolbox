#!/usr/bin/env python3
"""
文本统计分析工具 - 快速分析文档信息
作者: 效率工具包
版本: 2.0
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime

class TextAnalyzer:
    def __init__(self):
        self.stop_words = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '里', '为', '么', '他', '她', '它', '们', '这', '那', '哪', '谁', '什么', '怎么', '为什么', '因为', '所以', '但是', '而且', '或者', '如果', '虽然', '尽管', '即使', '无论', '不管', '只有', '只要', '除了', '关于', '对于', '由于', '通过', '根据', '按照', '依据', '为了', '以便', '以免', '除非', '假如', '假使', '倘若', '要是', '若是', '即使', '就算', '纵然', '尽管', '不管', '不论', '无论', '任凭', '只有', '只要', '除非', '除了', '除了', '除了'
        }

    def analyze_file(self, file_path):
        """分析单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
            except:
                return None

        return self.analyze_text(content, file_path)

    def analyze_text(self, text, source="direct_input"):
        """分析文本内容"""
        result = {
            'source': source,
            'timestamp': datetime.now().isoformat(),
            'basic_stats': self.get_basic_stats(text),
            'word_frequency': self.get_word_frequency(text),
            'char_frequency': self.get_char_frequency(text),
            'sentence_stats': self.get_sentence_stats(text),
            'readability': self.get_readability_score(text),
            'structure': self.get_text_structure(text)
        }

        return result

    def get_basic_stats(self, text):
        """获取基本统计信息"""
        lines = text.split('\n')
        paragraphs = [p for p in text.split('\n\n') if p.strip()]

        # 字符统计
        char_count = len(text)
        char_no_space = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))

        # 单词统计（中英文混合）
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text)
        word_count = len(words)

        # 中文字符统计
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        chinese_count = len(chinese_chars)

        # 英文单词统计
        english_words = re.findall(r'[a-zA-Z]+', text)
        english_word_count = len(english_words)

        # 数字统计
        numbers = re.findall(r'\d+', text)
        number_count = len(numbers)

        return {
            'total_characters': char_count,
            'characters_no_spaces': char_no_space,
            'total_words': word_count,
            'chinese_characters': chinese_count,
            'english_words': english_word_count,
            'numbers': number_count,
            'lines': len(lines),
            'non_empty_lines': len([l for l in lines if l.strip()]),
            'paragraphs': len(paragraphs),
            'spaces': text.count(' '),
            'tabs': text.count('\t')
        }

    def get_word_frequency(self, text, top_n=20):
        """获取词频统计"""
        # 提取中文词汇（2-4字）
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)

        # 提取英文单词
        english_words = re.findall(r'[a-zA-Z]{2,}', text.lower())

        # 合并并过滤停用词
        all_words = chinese_words + english_words
        filtered_words = [w for w in all_words if w not in self.stop_words and len(w) > 1]

        # 统计频率
        word_counter = Counter(filtered_words)
        return dict(word_counter.most_common(top_n))

    def get_char_frequency(self, text, top_n=15):
        """获取字符频率统计"""
        # 只统计中文字符和英文字母
        chars = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z]', text)
        char_counter = Counter(chars)
        return dict(char_counter.most_common(top_n))

    def get_sentence_stats(self, text):
        """获取句子统计"""
        # 按标点符号分割句子
        sentences = re.split(r'[。！？；\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return {
                'total_sentences': 0,
                'average_sentence_length': 0,
                'longest_sentence': 0,
                'shortest_sentence': 0
            }

        lengths = [len(s) for s in sentences]

        return {
            'total_sentences': len(sentences),
            'average_sentence_length': sum(lengths) / len(lengths),
            'longest_sentence': max(lengths),
            'shortest_sentence': min(lengths),
            'sentence_length_distribution': {
                'short (1-20)': len([l for l in lengths if l <= 20]),
                'medium (21-50)': len([l for l in lengths if 21 <= l <= 50]),
                'long (51+)': len([l for l in lengths if l > 50])
            }
        }

    def get_readability_score(self, text):
        """获取可读性评分（简化版）"""
        basic = self.get_basic_stats(text)

        if basic['total_sentences'] == 0 or basic['total_words'] == 0:
            return {'score': 0, 'level': '无法评估'}

        # 平均句子长度
        avg_sentence_len = basic['total_words'] / basic['total_sentences']

        # 平均词长
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text)
        if words:
            avg_word_len = sum(len(w) for w in words) / len(words)
        else:
            avg_word_len = 0

        # 简化的可读性评分（0-100）
        score = max(0, min(100, 100 - (avg_sentence_len * 2) - (avg_word_len * 5)))

        # 可读性等级
        if score >= 80:
            level = "非常容易阅读"
        elif score >= 60:
            level = "容易阅读"
        elif score >= 40:
            level = "中等难度"
        elif score >= 20:
            level = "较难阅读"
        else:
            level = "非常难阅读"

        return {
            'score': round(score, 2),
            'level': level,
            'average_sentence_length': round(avg_sentence_len, 2),
            'average_word_length': round(avg_word_len, 2)
        }

    def get_text_structure(self, text):
        """获取文本结构分析"""
        lines = text.split('\n')

        # 标题检测（以#开头或全大写）
        headers = []
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('#') or (line.isupper() and len(line) > 3):
                headers.append({'line': i+1, 'content': line[:50]})

        # 列表项检测
        list_items = []
        for i, line in enumerate(lines):
            line = line.strip()
            if re.match(r'^[-•*]\s', line) or re.match(r'^\d+\.\s', line):
                list_items.append({'line': i+1, 'content': line[:50]})

        # 代码块检测
        code_blocks = []
        in_code_block = False
        code_start = 0

        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_start = i+1
                else:
                    in_code_block = False
                    code_blocks.append({'start': code_start, 'end': i+1})

        return {
            'headers': headers[:10],  # 最多显示10个
            'list_items_count': len(list_items),
            'code_blocks_count': len(code_blocks),
            'has_headers': len(headers) > 0,
            'has_lists': len(list_items) > 0,
            'has_code': len(code_blocks) > 0
        }

    def generate_report(self, analysis_result, format='text'):
        """生成分析报告"""
        if format == 'json':
            return json.dumps(analysis_result, ensure_ascii=False, indent=2)

        # 文本格式报告
        report = []
        report.append("=" * 60)
        report.append("文本统计分析报告")
        report.append("=" * 60)
        report.append(f"分析时间: {analysis_result['timestamp']}")
        report.append(f"数据来源: {analysis_result['source']}")
        report.append("")

        # 基本统计
        basic = analysis_result['basic_stats']
        report.append("📊 基本统计")
        report.append("-" * 30)
        report.append(f"总字符数: {basic['total_characters']:,}")
        report.append(f"字符数(不含空格): {basic['characters_no_spaces']:,}")
        report.append(f"总词数: {basic['total_words']:,}")
        report.append(f"中文字符: {basic['chinese_characters']:,}")
        report.append(f"英文单词: {basic['english_words']:,}")
        report.append(f"数字: {basic['numbers']:,}")
        report.append(f"行数: {basic['lines']:,}")
        report.append(f"非空行: {basic['non_empty_lines']:,}")
        report.append(f"段落数: {basic['paragraphs']:,}")
        report.append("")

        # 可读性
        readability = analysis_result['readability']
        report.append("📖 可读性分析")
        report.append("-" * 30)
        report.append(f"可读性评分: {readability['score']}/100")
        report.append(f"阅读难度: {readability['level']}")
        report.append(f"平均句子长度: {readability['average_sentence_length']} 词")
        report.append(f"平均词长: {readability['average_word_length']} 字符")
        report.append("")

        # 句子统计
        sentence = analysis_result['sentence_stats']
        report.append("📝 句子统计")
        report.append("-" * 30)
        report.append(f"句子总数: {sentence['total_sentences']:,}")
        report.append(f"平均句长: {sentence['average_sentence_length']:.1f} 字符")
        report.append(f"最长句子: {sentence['longest_sentence']} 字符")
        report.append(f"最短句子: {sentence['shortest_sentence']} 字符")
        report.append("")

        # 词频统计
        word_freq = analysis_result['word_frequency']
        if word_freq:
            report.append("🔤 高频词汇 (Top 10)")
            report.append("-" * 30)
            for i, (word, count) in enumerate(list(word_freq.items())[:10], 1):
                report.append(f"{i:2d}. {word:<10} {count:>5} 次")
            report.append("")

        # 文本结构
        structure = analysis_result['structure']
        report.append("🏗️ 文本结构")
        report.append("-" * 30)
        report.append(f"标题数量: {len(structure['headers'])}")
        report.append(f"列表项数量: {structure['list_items_count']}")
        report.append(f"代码块数量: {structure['code_blocks_count']}")

        if structure['headers']:
            report.append("\n标题列表:")
            for header in structure['headers'][:5]:
                report.append(f"  第{header['line']}行: {header['content']}")

        report.append("")
        report.append("=" * 60)

        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='文本统计分析工具')
    parser.add_argument('input', help='输入文件路径或文本')
    parser.add_argument('--output', '-o', help='输出报告文件路径')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='输出格式')
    parser.add_argument('--top', type=int, default=20, help='显示高频词数量')

    args = parser.parse_args()

    analyzer = TextAnalyzer()

    # 分析输入
    if os.path.isfile(args.input):
        result = analyzer.analyze_file(args.input)
        if result is None:
            print(f"错误: 无法读取文件 {args.input}")
            return
    else:
        # 当作文本直接分析
        result = analyzer.analyze_text(args.input)

    # 生成报告
    report = analyzer.generate_report(result, args.format)

    # 输出报告
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存到: {args.output}")
    else:
        print(report)

if __name__ == '__main__':
    main()