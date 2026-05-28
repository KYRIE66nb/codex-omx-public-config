#!/usr/bin/env python3
"""Find specific content in DOCX: 技术线路图, 图3-1, 表4-1"""
import sys
from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

def find_targets(path):
    doc = Document(path)

    print("=== 查找目标内容 ===\n")

    # Track element index
    elem_idx = 0

    for element in doc.element.body:
        if isinstance(element, CT_P):
            para = Paragraph(element, doc)
            text = para.text.strip()

            # 查找技术线路图
            if '技术线路' in text or '线路图' in text:
                print(f"[找到] 技术线路图相关 at element {elem_idx}")
                print(f"  文本: {text}")
                print(f"  样式: {para.style.name if para.style else 'Normal'}")
                # Check for images
                if para._element.xpath('.//pic:pic'):
                    print(f"  -> 包含图片")
                print()

            # 查找图3-1
            if '图3-1' in text or '图 3-1' in text:
                print(f"[找到] 图3-1 at element {elem_idx}")
                print(f"  文本: {text}")
                if para._element.xpath('.//pic:pic'):
                    print(f"  -> 包含图片")
                print()

        elif isinstance(element, CT_Tbl):
            table = Table(element, doc)

            # 查找表4-1
            first_cell = table.rows[0].cells[0].text.strip() if table.rows else ""
            if '表4-1' in first_cell or '4-1' in first_cell:
                print(f"[找到] 表4-1 at element {elem_idx}")
                print(f"  表格大小: {len(table.rows)} 行 x {len(table.columns)} 列")
                print(f"  前3行内容:")
                for r_idx, row in enumerate(table.rows[:5]):
                    cells = [c.text.strip() for c in row.cells]
                    print(f"    Row {r_idx}: {cells}")
                print()

            # 也检查表格前的段落标题

        elem_idx += 1

    print(f"\n总共检查了 {elem_idx} 个元素")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: find_targets.py <docx_path>")
        sys.exit(1)
    find_targets(sys.argv[1])
