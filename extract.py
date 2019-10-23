# coding=utf-8
import jieba
import os
import codecs

# 分析该目录下的所有文本文件
default_dir = "./output"

# 所有评论的关键字
total_word_dict = {}

# 遍历文件夹
for root, dirs, files in os.walk(default_dir):
    for fileName in files:
        if len(fileName) >= 7 and fileName[-7:] == "key.txt":
            continue

        # 开始分析文件
        print "Analyse %s ..." % fileName

        # 读取文件，去掉首尾三行
        f = codecs.open(os.path.join(root, fileName), 'r', encoding='utf-8')
        lines = f.readlines()
        contents = lines[3:-3]

        # merge
        comments = ""
        for content in contents:
            comments = comments + content.encode('utf-8')

        # 分析
        segments = jieba.cut(comments, cut_all=True)
        word_dict = {}
        for segment in segments:
            if segment == '' or segment == '\n':
                continue

            # file segments
            if segment not in word_dict.keys():
                word_dict[segment] = 1
            else:
                word_dict[segment] = word_dict[segment] + 1

            # total segments
            if segment not in total_word_dict.keys():
                total_word_dict[segment] = 1
            else:
                total_word_dict[segment] = total_word_dict[segment] + 1

        # sort
        dictList = sorted(word_dict.items(), key=lambda d: d[1])
        dictList.reverse()

        # write into file
        baseName = fileName[:-4]
        writeFp = codecs.open('output/%s_key.txt' % baseName, 'w', encoding='utf-8')
        for i in range(len(dictList)):
            writeFp.write(dictList[i][0])
            writeFp.write('   ')
            writeFp.write(str(dictList[i][1]))
            writeFp.write('\n')

# 所有文件夹的评论
tolDictList = sorted(total_word_dict.items(), key=lambda d: d[1])
tolDictList.reverse()

# write into file
writeFp = codecs.open('output/total_key.txt', 'w', encoding='utf-8')
for i in range(len(tolDictList)):
    writeFp.write(tolDictList[i][0])
    writeFp.write('   ')
    writeFp.write(str(tolDictList[i][1]))
    writeFp.write('\n')
