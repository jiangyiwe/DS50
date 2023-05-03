import json
import pandas as pd
import os
import xml.etree.ElementTree as ET

# 定义要转换的文件夹,路径为xml文件所在文件夹
folder_path = r"E:\chatbot\MedQuAD（数据集）\1_CancerGov_QA"

# 定义要保存的CSV文件名
csv_file_name = r"E:\chatbot\Code\output.csv"

# 定义要提取的字段
columns = ['id', 'question', 'answer']

# 定义一个空的列表，用于保存所有问答对
qa_pairs = []




def traverseXML():
    c = 0
    d = 0
    # 递归遍历文件夹中的所有 XML 文件
    for file_name in os.listdir(folder_path):
            d += 1
            if file_name.endswith(".xml"):
                # 读取 XML 文件
                try:
                    tree = ET.parse(os.path.join(folder_path, file_name))
                    root_element = tree.getroot()
                    # 提取数据
                    for qa_pair in root_element.findall("QAPairs/QAPair"):
                        c += 1
                        question = qa_pair.find("Question")
                        answer = qa_pair.find("Answer")
                        if question is not None and answer is not None:
                            qa = {
                                'id': qa_pair.get('pid'),
                                'question': question.text,
                                'answer': answer.text,
                            }
                            qa_pairs.append(qa)

                    # 输出提取到的数据
                    print(f"Extracted {len(qa_pairs)} QA pairs from {file_name}")

                except Exception as e:
                    # 如果出现读取异常，跳过当前文件
                    print(f"Error reading {file_name}: {str(e)}")
                    continue

    # 将问答对列表转换为 DataFrame 对象，并保存为 CSV 文件
    df = pd.DataFrame(qa_pairs, columns=columns)
    df.to_csv(csv_file_name, index=False)
    print(c)
    print(d)

#traverseXML()