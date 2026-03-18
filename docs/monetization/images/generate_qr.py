#!/usr/bin/env python3
"""
收款码生成器 - 生成SVG占位符
用户可以替换为真实收款码
"""

import os
import base64
from datetime import datetime

def generate_svg_qr(text, filename, color="#000"):
    """生成SVG格式的收款码占位符"""
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="200" fill="white"/>
  <rect x="10" y="10" width="180" height="180" fill="none" stroke="{color}" stroke-width="2"/>
  <text x="100" y="90" font-family="Arial" font-size="14" text-anchor="middle" fill="{color}">{text}</text>
  <text x="100" y="110" font-family="Arial" font-size="12" text-anchor="middle" fill="#666">请替换为真实收款码</text>
  <text x="100" y="130" font-family="Arial" font-size="10" text-anchor="middle" fill="#999">{datetime.now().strftime("%Y-%m-%d")}</text>
</svg>'''

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"生成收款码: {filename}")

def main():
    # 生成微信收款码
    generate_svg_qr("微信收款", "wechat_qr.svg", "#07C160")

    # 生成支付宝收款码
    generate_svg_qr("支付宝收款", "alipay_qr.svg", "#1677FF")

    print("收款码占位符已生成！")
    print("请将真实收款码图片替换这些文件")
    print("支持格式: PNG, JPG, SVG")

if __name__ == "__main__":
    main()