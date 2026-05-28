#!/usr/bin/env python3
"""
毕业论文生成器 - 一键生成论文大纲、数据库设计和ER图
"""

import argparse
import json
import os
from datetime import datetime

# 论文标准结构模板
PAPER_OUTLINE_TEMPLATE = """# {title}

## 摘要
[待填写]

## Abstract
[To be filled]

## 第一章 绪论

### 1.1 研究背景
[描述项目背景和研究动机]

### 1.2 研究意义
[阐述研究的理论意义和实践意义]

### 1.3 国内外研究现状
[综述国内外相关研究]

## 第二章 相关技术介绍

### 2.1 {tech1}
[介绍主要开发语言或框架]

### 2.2 {tech2}
[介绍系统架构]

### 2.3 {tech3}
[介绍数据库技术]

### 2.4 {tech4}
[介绍其他相关技术]

## 第三章 系统需求分析

### 3.1 可行性分析

#### 3.1.1 技术可行性
[分析技术实现的可行性]

#### 3.1.2 经济可行性
[分析经济成本的可行性]

#### 3.1.3 操作可行性
[分析操作使用的可行性]

### 3.2 功能需求分析
[详细描述系统功能需求]

### 3.3 非功能需求分析
[描述性能、安全性等非功能需求]

## 第四章 系统设计

### 4.1 系统架构设计
[描述系统整体架构]

### 4.2 数据库设计

#### 4.2.1 数据库概念设计
[ER图]

#### 4.2.2 数据库逻辑设计
[表结构设计]

### 4.3 功能模块设计
[详细设计各功能模块]

## 第五章 系统实现

### 5.1 登录模块实现
[描述登录功能的实现]

### 5.2 {module1}实现
[描述核心功能模块的实现]

### 5.3 {module2}实现
[描述其他功能模块的实现]

## 第六章 系统测试

### 6.1 测试环境
[描述测试环境配置]

### 6.2 测试方法
[说明测试方法和策略]

### 6.3 测试用例
[列举主要测试用例]

### 6.4 测试结果与分析
[展示测试结果并分析]

## 第七章 总结与展望

### 7.1 总结
[总结研究工作和成果]

### 7.2 展望
[展望未来改进方向]

## 参考文献
[1] [待添加]

## 致谢
[待填写]

---
生成时间: {timestamp}
生成工具: Paper Generator v1.0
"""

# 数据库表设计模板
def generate_db_table(table_name, fields):
    """生成数据库表设计"""
    lines = [f"## {table_name}表"]
    lines.append("| 字段名称 | 类型 | 长度 | 字段说明 | 主键 | 默认值 |")
    lines.append("|---------|------|------|---------|------|--------|")

    # 必备字段
    lines.append("| id | bigint | | 主键 | 主键 | |")
    lines.append("| addtime | timestamp | | 创建时间 | | CURRENT_TIMESTAMP |")

    # 自定义字段
    for field in fields:
        name = field.get('name', '')
        ftype = field.get('type', 'varchar')
        length = field.get('length', '200' if ftype == 'varchar' else '')
        comment = field.get('comment', '')
        lines.append(f"| {name} | {ftype} | {length} | {comment} | | |")

    lines.append("")
    return "\n".join(lines)

# ER图生成
def generate_er_diagram(tables):
    """生成Mermaid格式的ER图"""
    lines = ["```mermaid", "erDiagram"]

    for table in tables:
        table_name = table.get('name', 'TABLE')
        fields = table.get('fields', [])

        lines.append(f"    {table_name} {{")
        lines.append(f"        bigint id PK \"主键\"")
        lines.append(f"        timestamp addtime \"创建时间\"")

        for field in fields:
            name = field.get('name', '')
            ftype = field.get('type', 'varchar')
            comment = field.get('comment', '')
            lines.append(f"        {ftype} {name} \"{comment}\"")

        lines.append("    }")

    # 添加关系
    for table in tables:
        relations = table.get('relations', [])
        for rel in relations:
            source = table.get('name', '')
            target = rel.get('target', '')
            rel_type = rel.get('type', 'one-to-many')
            if rel_type == 'one-to-many':
                lines.append(f"    {source} ||--o{{ {target} : \"has\"")

    lines.append("```")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description='毕业论文生成器')
    parser.add_argument('--title', required=True, help='论文标题')
    parser.add_argument('--tech', nargs=4, default=['Java编程语言', 'B/S架构', 'MySQL数据库', 'MyBatis-Plus框架'],
                        help='四个主要技术')
    parser.add_argument('--modules', nargs='+', default=['用户管理模块', '核心业务模块'],
                        help='功能模块列表')
    parser.add_argument('--output', default='paper_output', help='输出目录')

    args = parser.parse_args()

    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)

    # 生成论文大纲
    outline = PAPER_OUTLINE_TEMPLATE.format(
        title=args.title,
        tech1=args.tech[0],
        tech2=args.tech[1],
        tech3=args.tech[2],
        tech4=args.tech[3],
        module1=args.modules[0] if len(args.modules) > 0 else '核心功能模块',
        module2=args.modules[1] if len(args.modules) > 1 else '其他功能模块',
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    outline_path = os.path.join(args.output, 'paper_outline.md')
    with open(outline_path, 'w', encoding='utf-8') as f:
        f.write(outline)

    print(f"✓ 论文大纲已生成: {outline_path}")

    # 生成数据库设计示例
    db_design = "# 数据库设计\n\n"
    db_design += generate_db_table("用户", [
        {'name': 'username', 'type': 'varchar', 'length': '100', 'comment': '用户名'},
        {'name': 'password', 'type': 'varchar', 'length': '100', 'comment': '密码'},
        {'name': 'nickname', 'type': 'varchar', 'length': '200', 'comment': '昵称'},
        {'name': 'avatar', 'type': 'varchar', 'length': '500', 'comment': '头像'},
        {'name': 'phone', 'type': 'varchar', 'length': '20', 'comment': '手机号'},
        {'name': 'status', 'type': 'int', 'length': '', 'comment': '状态'},
    ])

    db_path = os.path.join(args.output, 'database_design.md')
    with open(db_path, 'w', encoding='utf-8') as f:
        f.write(db_design)

    print(f"✓ 数据库设计已生成: {db_path}")

    # 生成ER图示例
    tables = [
        {
            'name': 'USER',
            'fields': [
                {'name': 'username', 'type': 'varchar', 'comment': '用户名'},
                {'name': 'password', 'type': 'varchar', 'comment': '密码'},
                {'name': 'nickname', 'type': 'varchar', 'comment': '昵称'},
            ]
        }
    ]

    er_diagram = generate_er_diagram(tables)
    er_path = os.path.join(args.output, 'er_diagram.md')
    with open(er_path, 'w', encoding='utf-8') as f:
        f.write("# ER图\n\n")
        f.write(er_diagram)

    print(f"✓ ER图已生成: {er_path}")

    print(f"\n所有文件已生成到目录: {args.output}")
    print("\n使用方法:")
    print(f"  1. 查看论文大纲: cat {outline_path}")
    print(f"  2. 查看数据库设计: cat {db_path}")
    print(f"  3. 查看ER图: cat {er_path}")

if __name__ == '__main__':
    main()
