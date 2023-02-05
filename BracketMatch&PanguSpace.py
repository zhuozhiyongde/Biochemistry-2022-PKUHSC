# -*- encoding: utf-8 -*-
#@Author  :   Arthals
#@File    :   BracketMatch&PanguSpace.py
#@Time    :   2023/02/02 20:35:56
#@Contact :   zhuozhiyongde@126.com
#@Software:   Visual Studio Code

import re
import os
import sys
import pangu


def match_brackets(origin_text: str):
    # 将所有中文圆括号替换为英文圆括号
    text = origin_text.replace('（', '(').replace('）', ')')

    # 检查括号匹配
    stack = []
    for i in range(len(text)):
        if text[i] == '(':
            stack.append(text[i])
        elif text[i] == ')':
            if not stack or stack[-1] != '(':
                return False
            stack.pop()

    if stack:
        return False

    # 按照左括号的语言匹配右括号
    new_text = re.sub(r'\(([^\(]*?)）', r'(\1)', text)
    new_text = re.sub(r'（([^（]*?)\)', r'（\1）', new_text)

    pattern = re.compile(r'(?<=[\u4e00-\u9fff])\(([^(]*?)\)')
    while True:
        text = new_text
        new_text = re.sub(pattern, '（\\1）', new_text)
        if text == new_text:
            break
    pattern = re.compile(r'\(([\u4e00-\u9fff][^\(]*?)\)')
    while True:
        text = new_text
        new_text = re.sub(pattern, '（\\1）', new_text)
        if text == new_text:
            break

    return new_text


if __name__ == '__main__':
    # list all md files in current directory
    """ import difflib
    text = '2. 三级结构的稳定性主要靠**次级键(疏水键，盐键(离子键），氢键和范德华力)**维持，尤其是**疏水键**；'
    # print(match_brackets(text))

    # print([text == match_brackets(text)])
    # use difflib to compare two strings
    d = difflib.HtmlDiff()
    # save html
    print(text == match_brackets(text))
    with open('diff.html', 'w', encoding='utf-8') as f:
        f.write(d.make_file(text, match_brackets(text)))

    exit() """

    md_files = [
        file for file in os.listdir('.')
        if file.endswith('.md') and re.match(r'\d{2}', file)
    ]
    print(md_files)

    # check brackets
    for file in md_files:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        flag = False
        match_flag = False
        for i in range(len(lines)):
            line = lines[i]
            if '/Users/zhuozhiyongde/' in line:
                continue
            if re.search(r'[\(\)（）]', line):
                new_line = match_brackets(line)
                if new_line is False:
                    print('Error in file: %s, line: %d' % (file, i + 1))
                    print('Error line: %s' % line)
                    # sys.exit(1)
                    match_flag = True
                    continue
                if new_line == line:
                    continue
                lines[i] = new_line
                flag = True
                print('File: %s, line: %d bracket formatted' % (file, i + 1))

        if not flag and not match_flag:
            print('File: %s, no error' % file)

        if match_flag:
            print('File: %s, bracket match error' % file)

        # print(lines)
        # pangu format lines
        flag = False
        new_lines = []
        for i in range(len(lines)):
            if '/Users/zhuozhiyongde/' in lines[i] or lines[i] == '\n':
                new_lines.append(lines[i])
                continue

            new_line = pangu.spacing_text(lines[i])
            pattern = re.compile(r'(?<=\*\*)[^\*]*?(?=\*\*)')
            new_line = re.sub(pattern, lambda x: x.group().strip(), new_line)

            # lines[i] = new_line + '\n'
            if not new_line.endswith('\n'):
                new_line = new_line + '\n'

            if re.match(r' +', lines[i]):
                # print(lines[i])
                new_line = re.match(r' +',
                                    lines[i]).group() + new_line.lstrip()

            new_lines.append(new_line)
            if new_line != lines[i]:
                # pass
                print([lines[i]], [new_line], sep='\n')
                print('File: %s, line: %d pangu formatted' % (file, i + 1))
                flag = True

        # print(new_lines)
        if not flag:
            print('File: %s, no pangu format' % file)

        # pangu format lines and write to file
        with open(file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
