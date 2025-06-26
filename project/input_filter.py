import re
import json

with open('SensitiveLexicon.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class SensitiveWordFilter:
    def __init__(self):
        self.root = TrieNode()
    
    def add_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def filter_text(self, text):
        result = []
        i = 0
        n = len(text)
        
        while i < n:
            node = self.root
            j = i
            last_end = -1
            
            while j < n and text[j] in node.children:
                node = node.children[text[j]]
                if node.is_end:
                    last_end = j
                j += 1
            
            if last_end != -1:
                result.append('*' * (last_end - i + 1))
                i = last_end + 1
            else:
                result.append(text[i])
                i += 1
        
        return ''.join(result)

def sanitize_sql_input(input_str):
    
    # 移除SQL注释
    input_str = re.sub(r'--.*$', '', input_str)
    input_str = re.sub(r'/\*.*?\*/', '', input_str, flags=re.DOTALL)
    
    # 移除常见SQL关键字
    sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 
                   'UNION', 'WHERE', 'OR', 'AND', 'EXEC', 'EXECUTE']
    
    for keyword in sql_keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        input_str = pattern.sub('', input_str)
    
    # 移除特殊字符
    input_str = re.sub(r'[;\'"\\]', '', input_str)
    
    return input_str.strip()

def sanitize_command_input(input_str):
    """
    命令注入防护
    :param input_str: 用户输入
    :return: 净化后的字符串
    """
    # 移除特殊字符和命令分隔符
    input_str = re.sub(r'[;&|`$\n\r]', '', input_str)
    
    # 移除路径相关字符
    input_str = re.sub(r'[./\\]', '', input_str)
    
    # 移除常见命令
    commands = ['rm', 'sh', 'bash', 'cmd', 'powershell', 'wget', 'curl']
    for cmd in commands:
        pattern = re.compile(r'\b' + re.escape(cmd) + r'\b', re.IGNORECASE)
        input_str = pattern.sub('', input_str)
    
    return input_str.strip()

class InputPreprocessor:
    def __init__(self):
        self.sensitive_words = data["words"]
        self.filter = SensitiveWordFilter()
        for word in self.sensitive_words:
            self.filter.add_word(word)
    
    def preprocess(self, input_str):
        """
        综合预处理
        :param input_str: 用户输入
        :param input_type: 输入类型 ('text', 'sql', 'command')
        :return: 预处理后的字符串
        """
        # 去除前后空白
        input_str = input_str.strip()
        
        # 敏感词过滤
        input_str = self.filter.filter_text(input_str)
        
        # 指令注入防护
        input_str = sanitize_sql_input(input_str)
        input_str = sanitize_command_input(input_str)
        
        return input_str