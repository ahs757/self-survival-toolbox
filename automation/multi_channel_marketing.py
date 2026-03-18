#!/usr/bin/env python3
"""
📢 多渠道营销系统 - Multi Channel Marketing
整合小红书、知乎、微信、抖音等多平台营销内容生成和发布
"""

import json
import os
import random
from datetime import datetime

class MultiChannelMarketing:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.marketing_dir = os.path.join(os.path.dirname(self.base_dir), 'marketing')
        os.makedirs(self.marketing_dir, exist_ok=True)

        # 内容模板库
        self.content_templates = {
            'xiaohongshu': self.get_xiaohongshu_templates(),
            'zhihu': self.get_zhihu_templates(),
            'wechat': self.get_wechat_templates(),
            'douyin': self.get_douyin_templates(),
            'weibo': self.get_weibo_templates()
        }

    def get_xiaohongshu_templates(self):
        """小红书爆款模板"""
        return [
            {
                'title': '打工人必看！每天多出3小时的秘密工具',
                'content': '''姐妹们！！！我真的哭死 😭😭😭

之前每天加班到10点，现在5点准时下班
全靠这几个效率神器，后悔没早点知道！

✅ 工具1: 自动化脚本
- 一键处理Excel数据
- 批量重命名文件
- 自动整理文件夹

✅ 工具2: 模板库
- 周报模板直接套用
- PPT模板秒出方案
- 邮件模板效率翻倍

✅ 工具3: AI助手
- 会议纪要自动生成
- 文案灵感一键获取
- 数据分析智能解读

现在我把这些工具整理成了一个工具包
需要的姐妹评论区扣"工具包"！

#效率工具 #打工人 #职场干货 #时间管理 #办公神器''',
                'tags': ['效率工具', '打工人', '职场', '时间管理']
            },
            {
                'title': '普通人下班后做副业，月入5000+的3个方法',
                'content': '''先说结论：我靠这3个副业，上个月赚了8000+ 🎉

方法1️⃣: 知识付费
- 把你会的技能做成课程
- 定价9.9-99元不等
- 一份时间卖多次

方法2️⃣: 模板销售
- 做PPT/Excel/Word模板
- 上传到各个平台
- 被动收入躺赚

方法3️⃣: 工具开发
- 开发简单的小工具
- 解决特定人群痛点
- 用户自动传播

我整理了一份《副业启动指南》
包含从0到1的完整流程
评论区扣"副业"免费领取！

#副业 #赚钱 #知识付费 #被动收入 #普通人逆袭''',
                'tags': ['副业', '赚钱', '知识付费', '被动收入']
            },
            {
                'title': '老板让我加班做表格，我用10分钟搞定了一天的活',
                'content': '''事情是这样的👇

老板: 这500个数据今晚整理完
我: 好的（内心：完了又要加班）

结果！
我用了10分钟就搞定了 🎉

秘诀就是Python自动化脚本！

✅ 数据清洗：自动去除重复
✅ 格式转换：一键批量处理
✅ 数据分析：图表自动生成
✅ 报告生成：模板自动填充

现在我把这些脚本都整理好了
不需要会编程，一键运行就行

需要的姐妹评论区扣"自动化"
我把链接发你！

#Python #自动化办公 #效率工具 #打工人福音 #职场技能''',
                'tags': ['Python', '自动化', '效率', '职场']
            }
        ]

    def get_zhihu_templates(self):
        """知乎高赞回答模板"""
        return [
            {
                'question': '如何在短时间内大幅提高工作效率？',
                'answer': '''作为一个在互联网公司工作5年的职场人，我来分享一下我的效率提升心得。

## 核心发现

**真正的效率提升不是靠加班，而是靠工具和方法。**

我以前也是加班到10点，后来发现：

1. **80%的重复性工作可以自动化**
2. **模板能节省60%的时间**
3. **正确的时间管理能让效率翻倍**

## 我的效率工具包

### 1. 自动化脚本（10+个）
- Excel数据一键处理：500条数据10秒搞定
- 文件批量重命名：告别手动改名
- 数据自动清洗：重复数据自动去除
- 报告自动生成：模板填数据出报告

### 2. 实用模板（50+个）
- 周报/日报模板：10分钟完成周报
- PPT方案模板：一套模板走天下
- 邮件模板：再也不用纠结措辞
- 简历模板：投递100份收到50个面试

### 3. 时间管理工具
- 番茄钟：25分钟高效专注
- 任务清单：自动排序优先级
- 时间统计：可视化你的时间去哪了

## 实际效果

使用这套工具后：
- 每天准时5点下班
- 周报从2小时变成10分钟
- Excel处理效率提升10倍
- 3个月薪资涨了30%

## 获取方式

我把这套工具整理成了工具包，包含：
- 10+自动化脚本
- 50+实用模板
- 时间管理工具
- 使用教程

如果需要可以私信我，分享给大家。

---

*更新：工具包已整理完成，包含使用视频教程，需要的朋友可以私信获取。*''',
                'tags': ['效率', '职场', '工具', '自动化']
            },
            {
                'question': '普通上班族如何开启副业赚钱？',
                'answer': '''分享一下我从0到月入过万的副业经历。

## 我的副业历程

去年这个时候，我还是个月光族。
现在靠副业每月稳定收入8000-15000。

## 3个验证过的副业方向

### 1. 知识付费（门槛最低）

**核心逻辑：把你的技能变成产品**

我做的：
- 效率工具包（¥29）
- 简历模板库（¥19）
- 职场技能课（¥99）

效果：
- 每月稳定出30-50单
- 客户自动复购和转介绍
- 被动收入占比越来越高

### 2. 技能服务（利润最高）

**核心逻辑：用专业技能解决他人问题**

我做的：
- 简历优化（¥99/次）
- 职业规划咨询（¥199/次）
- 一对一指导（¥499/月）

效果：
- 每月服务10-20人
- 高复购率
- 口碑传播

### 3. 分销代理（最轻松）

**核心逻辑：推广他人的好产品拿佣金**

我做的：
- 推广效率工具（佣金30%）
- 推广职场课程（佣金40%）
- 推广学习平台（佣金50%）

效果：
- 不用自己做产品
- 每月被动收入3000+

## 实操建议

1. **选择你擅长的领域**
2. **先从小产品开始**
3. **重视客户体验**
4. **持续优化迭代**

## 资源分享

我整理了一份《副业从0到1指南》：
- 选方向的方法
- 做产品的模板
- 推广的渠道
- 变现的路径

需要可以私信我免费领取。''',
                'tags': ['副业', '赚钱', '知识付费', '职场']
            }
        ]

    def get_wechat_templates(self):
        """微信朋友圈模板"""
        return [
            {
                'type': 'morning',
                'content': '''【早安分享】☀️

今天又是元气满满的一天！

分享一个效率小技巧：
用番茄钟工作法，25分钟专注+5分钟休息
一天下来效率能提升200%

我已经坚持用了3个月
每天5点准时下班，真的太香了！

需要番茄钟工具的朋友
评论区扣"番茄"，我发你～''',
            },
            {
                'type': 'noon',
                'content': '''【午间干货】💡

又帮一位小伙伴优化了简历
结果：从0面试到3天拿到2个offer

简历优化的核心就3点：
✅ 关键词匹配JD
✅ 数据量化成果
✅ 亮点前置展示

如果你也在求职
一定要重视简历！
需要简历诊断的私聊我～''',
            },
            {
                'type': 'evening',
                'content': '''【今日战绩】🎉

今天的效率工具包又出了5单
看到大家用得开心，我也很有成就感

客户反馈：
"周报从2小时变成10分钟"
"Excel处理效率提升10倍"
"每天多出2小时陪家人"

这就是我做这件事的意义 ❤️

需要的朋友私聊我
限时优惠：前10名8折！''',
            },
            {
                'type': 'promotion',
                'content': '''【限时福利】🔥

今晚12点前下单的朋友
额外赠送价值99元的简历模板库

包含：
✅ 互联网大厂简历模板
✅ 外企英文简历模板
✅ 应届生简历模板
✅ 转行简历模板

仅剩最后3份！
需要的私聊我领取专属优惠码～''',
            }
        ]

    def get_douyin_templates(self):
        """抖音/短视频脚本模板"""
        return [
            {
                'type': 'pain_point',
                'duration': '15秒',
                'script': '''【画面】深夜加班的办公室
【旁白】
"你是不是也这样？
每天加班到10点
周报写了2小时
Excel做到眼花"

【画面】切换到轻松下班
【旁白】
"直到我发现了这个方法
现在每天5点准时下班
想知道怎么做吗？
评论区扣1，我教你"''',
            },
            {
                'type': 'demo',
                'duration': '30秒',
                'script': '''【画面】电脑屏幕录屏
【旁白】
"看好了，这是500条数据
以前要处理2小时
现在只要10秒"

【画面】点击运行脚本
【旁白】
"一键运行
数据自动清洗
格式自动转换
报告自动生成"

【画面】展示结果
【旁白】
"这就是自动化的威力
需要脚本的评论区留言"''',
            },
            {
                'type': 'story',
                'duration': '20秒',
                'script': '''【画面】收到offer的邮件
【旁白】
"投了100份简历，0面试
我以为今年找不到工作了"

【画面】展示简历对比
【旁白】
"直到我改了这3个地方
一周拿到5个offer
最后选了薪资最高的那个"

【画面】文字提示
【旁白】
"想知道改了哪里吗？
评论区扣简历，我发你模板"''',
            }
        ]

    def get_weibo_templates(self):
        """微博营销模板"""
        return [
            {
                'content': '''#效率工具# #职场干货#

打工人必看！每天多出3小时的秘密 🔥

分享我的效率工具包：
✅ 10+自动化脚本
✅ 50+实用模板
✅ 时间管理工具

用了之后：
- 每天5点准时下班
- 周报10分钟搞定
- 效率提升200%

需要的朋友私信我～
限时优惠中！''',
                'tags': ['#效率工具#', '#职场干货#', '#打工人#']
            },
            {
                'content': '''#副业赚钱# #知识付费#

普通人月入过万的副业方法 💰

我验证过的3个方向：
1️⃣ 知识付费：把技能变成产品
2️⃣ 技能服务：用专业解决他人问题
3️⃣ 分销代理：推广好产品拿佣金

上月副业收入：¥8000+
需要《副业指南》的私信我免费领～''',
                'tags': ['#副业赚钱#', '#知识付费#', '#被动收入#']
            }
        ]

    def generate_daily_content_plan(self):
        """生成每日内容发布计划"""
        today = datetime.now().strftime('%Y-%m-%d')
        weekday = datetime.now().strftime('%A')

        plan = {
            'date': today,
            'weekday': weekday,
            'content_plan': []
        }

        # 根据时间选择不同的内容类型
        hour = datetime.now().hour

        if hour < 12:
            # 上午内容
            plan['content_plan'] = [
                {
                    'platform': 'xiaohongshu',
                    'time': '08:30',
                    'content': random.choice(self.content_templates['xiaohongshu']),
                    'goal': '引流 + 收集线索'
                },
                {
                    'platform': 'zhihu',
                    'time': '09:00',
                    'content': random.choice(self.content_templates['zhihu']),
                    'goal': 'SEO + 专业形象'
                },
                {
                    'platform': 'wechat',
                    'time': '09:30',
                    'content': self.content_templates['wechat'][0],  # 早安分享
                    'goal': '朋友圈曝光'
                }
            ]
        elif hour < 18:
            # 下午内容
            plan['content_plan'] = [
                {
                    'platform': 'douyin',
                    'time': '12:00',
                    'content': random.choice(self.content_templates['douyin']),
                    'goal': '短视频引流'
                },
                {
                    'platform': 'wechat',
                    'time': '14:00',
                    'content': self.content_templates['wechat'][1],  # 午间干货
                    'goal': '朋友圈互动'
                },
                {
                    'platform': 'weibo',
                    'time': '16:00',
                    'content': random.choice(self.content_templates['weibo']),
                    'goal': '微博曝光'
                }
            ]
        else:
            # 晚上内容
            plan['content_plan'] = [
                {
                    'platform': 'wechat',
                    'time': '19:00',
                    'content': self.content_templates['wechat'][2],  # 今日战绩
                    'goal': '朋友圈转化'
                },
                {
                    'platform': 'xiaohongshu',
                    'time': '20:00',
                    'content': random.choice(self.content_templates['xiaohongshu']),
                    'goal': '晚间黄金时段'
                },
                {
                    'platform': 'wechat',
                    'time': '21:00',
                    'content': self.content_templates['wechat'][3],  # 限时福利
                    'goal': '紧迫感促单'
                }
            ]

        return plan

    def save_content_to_files(self, plan):
        """保存内容到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        for item in plan['content_plan']:
            platform = item['platform']
            content = item['content']

            # 生成文件名
            filename = f"{platform}_{timestamp}.md"
            filepath = os.path.join(self.marketing_dir, filename)

            # 准备内容
            file_content = f"""# {platform.upper()} 营销内容

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**发布时间**: {item['time']}
**目标**: {item['goal']}

---

"""
            if isinstance(content, dict):
                for key, value in content.items():
                    if key != 'tags':
                        file_content += f"## {key}\n\n{value}\n\n"
                    else:
                        file_content += f"## 标签\n\n{', '.join(value)}\n\n"
            else:
                file_content += str(content)

            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(file_content)

            print(f"✅ 已生成 {platform} 内容: {filepath}")

    def run_marketing(self):
        """运行营销系统"""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   📢 多渠道营销系统启动中... 📢                               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """)

        # 生成今日内容计划
        print("\n📅 生成今日内容计划...")
        plan = self.generate_daily_content_plan()

        print(f"\n📊 今日发布计划 ({plan['date']} {plan['weekday']}):")
        for item in plan['content_plan']:
            print(f"  {item['time']} - {item['platform']} - {item['goal']}")

        # 保存内容到文件
        print("\n💾 保存内容到文件...")
        self.save_content_to_files(plan)

        print("""
✅ 营销内容已生成！

📋 执行步骤：
1. 打开对应平台
2. 复制生成的内容
3. 按计划时间发布
4. 互动回复评论
5. 引导私信转化

🎯 今日目标：
- 发布 6-8 条内容
- 收集 10+ 个线索
- 转化 2-3 个销售

🚀 开始行动吧！
        """)

def main():
    """主函数"""
    marketing = MultiChannelMarketing()

    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   📢 Multi Channel Marketing - 多渠道营销系统 📢              ║
║                                                               ║
║   功能菜单:                                                    ║
║   1. 运行营销系统                                              ║
║   2. 生成今日内容计划                                          ║
║   3. 查看内容模板                                              ║
║   4. 生成指定平台内容                                          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    choice = input("请选择功能 (1-4): ")

    if choice == '1':
        marketing.run_marketing()
    elif choice == '2':
        plan = marketing.generate_daily_content_plan()
        print(f"\n📅 今日内容计划 ({plan['date']}):")
        for item in plan['content_plan']:
            print(f"  {item['time']} - {item['platform']} - {item['goal']}")
    elif choice == '3':
        print("\n📚 内容模板库:")
        for platform in marketing.content_templates:
            print(f"  {platform}: {len(marketing.content_templates[platform])} 个模板")
    elif choice == '4':
        platform = input("平台名称 (xiaohongshu/zhihu/wechat/douyin/weibo): ")
        if platform in marketing.content_templates:
            template = random.choice(marketing.content_templates[platform])
            print(f"\n📝 {platform} 内容:")
            if isinstance(template, dict):
                for key, value in template.items():
                    print(f"\n## {key}")
                    print(value)
            else:
                print(template)

if __name__ == '__main__':
    main()
