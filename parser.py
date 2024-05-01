import base64
import re
import urllib

import yaml
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests


class handler(BaseHTTPRequestHandler):
    # def __init__(self):
    # 由于 BaseHTTPRequestHandler 不是使用典型的构造方法初始化的，不好 super() 所以使用自定义初始化
    def initialize(self):
        # 自定义初始化逻辑
        if not hasattr(self, 'subscription_userinfo'):
            self.subscription_userinfo = None
            self.profile_update_interval = None
            self.content_disposition = None
            self.profile_web_page_url = None
            self.user_agent = None

    def log_message(self, format, *args):
        # 覆盖此方法以避免在控制台记录每个请求
        pass
    
    @staticmethod
    def parse_query_parameters(path):
        # 解析 URL 中的查询参数
        from urllib.parse import urlparse, parse_qs
        query = urlparse(path).query
        return parse_qs(query)

    def fetch_yaml(self, url, fetch_type=None):
        # 从给定的 URL 获取并解析 YAML
        try:
            print(f"trying to getting url")
            response = requests.get(url)
            response.raise_for_status()
            if fetch_type == 'source':
                # 记录 Subscription-Userinfo 响应头，即流量信息
                self.subscription_userinfo = response.headers.get('Subscription-Userinfo', None)
                # 记录 profile-update-interval 响应头，即更新间隔
                self.profile_update_interval = response.headers.get('Profile-Update-Interval', None)
                # 记录 content-disposition 响应头，即配置文件名称
                self.content_disposition = response.headers.get('Content-Disposition', None)
                # 记录 profile-web-page-url 响应头，即配置文件主页
                self.profile_web_page_url = response.headers.get('Profile-Web-Page-Url', None)
            return yaml.safe_load(response.content)
        except Exception as error:
            print(f"Error fetching YAML from {url}: {error}")
            return None

    @staticmethod
    def merge_yaml(source, mixin):
        # 应用 mixin
        for key, value in mixin.get('mixin', {}).items():
            if key in source:
                source[key].update(value)
            else:
                source[key] = value
        return source

    def modify_yaml(self, source_yaml, parser_yaml):
        # 根据 parser_yaml 中的规则修改 source_yaml
        # 执行 parser
        try:
            for key, operations in parser_yaml.get('yaml', {}).items():
                if key.startswith('append-') or key.startswith('prepend-'):
                    self.modify_list(source_yaml, key, operations)
                elif key.startswith('mix-'):
                    self.mix_object(source_yaml, key, operations)

            # 执行 commands
            for command in parser_yaml.get('yaml', {}).get('commands', []):
                self.apply_command(source_yaml, command)

            return source_yaml

        except Exception as error:
            return None

    @staticmethod
    def modify_list(source_yaml, key, operations):
        # 修改 source_yaml 中的列表
        list_name = key.split('-', 1)[1]
        source_list = source_yaml.get(list_name, [])

        # Prepend or append operations
        # 根据操作类型（附加 Prepend 或前置 append）进行修改
        if key.startswith('append-'):
            source_list.extend(operations)
        elif key.startswith('prepend-'):
            source_list = operations + source_list

        source_yaml[list_name] = source_list

    @staticmethod
    def mix_object(source_yaml, key, operations):
        # 确定 source_yaml 中的目标对象
        object_name = key.split('-', 1)[1]
        source_object = source_yaml.get(object_name, {})

        # 合并对象
        source_object.update(operations)
        source_yaml[object_name] = source_object

    def apply_command(self, source_yaml, command):
        path, operation, value = self.parse_command(command)

        # 查找并处理目标策略组
        target_group = self.find_proxy_group(source_yaml, path)
        if target_group is None:
            return  # 如果没有找到目标策略组，则跳过此命令

        if value.startswith('[]'):
            regex_pattern = value[2:]
            self.apply_regex_to_proxies(source_yaml, target_group, regex_pattern)

        if operation == '+':
            # 插入代理到特定位置
            index = int(path[2]) if path[2].isdigit() else None
            if index is not None and index < len(target_group['proxies']):
                target_group['proxies'].insert(index, value)
            else:
                target_group['proxies'].append(value)  # 如果索引无效，则默认添加到末尾

    @staticmethod
    def find_proxy_group(source_yaml, path):
        # 检查路径长度是否足够
        if len(path) < 2:
            return None
        # 查找指定的策略组
        group_name = path[1]
        for group in source_yaml.get('proxy-groups', []):
            if group['name'] == group_name:
                return group
        return None

    @staticmethod
    def apply_regex_to_proxies(source_yaml, target_group, regex_pattern):
        # 使用正则表达式筛选代理
        regex = re.compile(regex_pattern)
        matched_proxies = [proxy['name'] for proxy in source_yaml.get('proxies', []) if regex.search(proxy['name'])]

        # 将匹配的代理添加到目标策略组
        target_group['proxies'].extend(matched_proxies)

    @staticmethod
    def parse_command(command):
        # 首先尝试以 '+' 为分隔符分割命令
        if '+' in command:
            parts = command.split('+', 1)
            operation = '+'
        # 如果没有 '+', 则尝试以 '=' 为分隔符
        elif '=' in command:
            parts = command.split('=', 1)
            operation = '='
        else:
            raise ValueError("Invalid command format")

        if len(parts) != 2:
            raise ValueError("Invalid command format")

        path = parts[0].split('.')
        value = parts[1]

        return path, operation, value

    @staticmethod
    def decode_raw_url(raw_url):
        # 本地文件解码
        def is_base64(s):
            try:
                encoded = base64.b64encode(base64.b64decode(s)).decode('utf-8')
                return encoded == s and all(char.isprintable() for char in base64.b64decode(s).decode('utf-8'))
            except Exception:
                return False

        def is_url_encoded(s):
            return '%' in s and s != urllib.parse.unquote(s)

        if is_url_encoded(raw_url):
            # 检测是不是 urlencoded 过的文本，是则返回解码的文本
            return urllib.parse.unquote(raw_url)

        if is_base64(raw_url):
            # 检查是不是 base64 过的文本，是则返回解码的文本
            return base64.b64decode(raw_url).decode('utf-8')

        return raw_url

    def fetch_local_url(self, file_name):
        """
        从文件内读取链接
        :param file_name: 文件名
        :return: 解析后的URL
        :rtype: str
        """
        file_processed = False
        file_path = ['./' + file_name, '../' + file_name]

        for file in file_path:
            try:
                with open(file, 'r', encoding='utf-8') as opened_file:
                    url_raw = opened_file.readline().strip()  # 读取第一行，订阅链接
                    url_type = opened_file.readline().strip()  # 读取第一行，链接编码类型

                    # 根据第二行的内容选择解码方法
                    if url_type.lower() in ['base64', 'base64-encoded']:
                        url = base64.b64decode(url_raw).decode('utf-8')
                    elif url_type.lower() in ['urlencode', 'urlencoded', 'url_encode', 'url encode']:
                        url = urllib.parse.unquote(url_raw)
                    elif url_type.lower() in ['raw', 'default', 'normal']:
                        url = url_raw
                    else:
                        url = handler.decode_raw_url(url_raw)  # 假设这是静态方法

                    file_processed = True
                    break
            except FileNotFoundError:
                continue  # 尝试下一个文件路径
            except Exception as error:
                print(f"fetch_local_url error: {error}")
                break

        if file_processed:
            return url
        else:
            print(f"using fetch_local_url, but {file_name} not found")
            self.send_error(500, f"using fetch_local_url, but {file_name} not found")

    def fetch_local_yaml(self, file_name):
        """
        读取本地 yaml 文件。
        :param file_name: 文件名
        :return: 文件内容的yaml对象
        :rtype yaml object
        """
        file_processed = False  # 增加标记变量
        file_path = ['./' + file_name, '../' + file_name]

        for file in file_path:
            try:
                with open(file, 'r', encoding='utf-8') as opened_file:
                    file_processed = True
                    return yaml.safe_load(opened_file)
            except FileNotFoundError:
                continue  # 尝试下一个文件路径
            except Exception as error:
                print(f"fetch_local_yaml error: {error}")
                break

        if not file_processed:
            # 如果没有成功处理任何文件
            print(f"using fetch_local_yaml file, but {file_name} not found")
            self.send_error(500, f"using fetch_local_yaml, but {file_name} file not found")

    def do_GET(self):
        # 确保初始化
        self.initialize()

        source_url, parser_url, mixin_url = None, None, None

        # 解析查询参数，并获取对应文件
        query_components = self.parse_query_parameters(self.path)
        try:
            source = query_components.get('source', [''])[0]
            print(source)
            if source == 'jynb':  # 幻数从本地获取
                source_url = self.fetch_local_url('source.txt')
                source_yaml = self.fetch_yaml(source_url, 'source')
            else:
                source_url = base64.b64decode(source).decode()
                source_yaml = self.fetch_yaml(source_url, 'source')

            if not source_yaml:
                print("Error fetching source_yaml")
                self.send_error(500, "Error fetching source_yaml")

            parser = query_components.get('parser', [''])[0]
            if parser:
                parser_url = base64.b64decode(parser).decode()
                parser_yaml = self.fetch_yaml(parser_url)
            else:  # 不提供就默认从本地获取
                parser_yaml = self.fetch_local_yaml('parser.yaml')

            if not parser_yaml:
                print("Error fetching parser_yaml")
                self.send_error(500, "Error fetching parser_yaml")

            mixin = query_components.get('mixin', [''])[0]
            if mixin:
                if mixin == 'jynb':  # 幻数从本地获取
                    mixin_yaml = self.fetch_local_yaml('mixin.yaml')
                else:
                    mixin_url = base64.b64decode(mixin).decode()
                    mixin_yaml = self.fetch_yaml(mixin_url)
            else:
                mixin_yaml = None
        except Exception as error:
            self.send_error(500, f"Unable to decode URL: {error}")

        try:
            # 进行 mixin
            if source_yaml and mixin_yaml:
                print("Perform mixin")
                source_yaml = self.merge_yaml(source_yaml, mixin_yaml)
        except Exception as error:
            self.send_error(500, f"Error in perform mixin: {error}")

        try:
            # 进行 parser
            if source_yaml and parser_yaml:
                print("Perform parser")
                modified_yaml = self.modify_yaml(source_yaml, parser_yaml)
        except Exception as error:
            self.send_error(500, f"Error in perform parser: {error}")

        if modified_yaml:
            # 发送正确响应
            self.send_response(200)
            # self.send_header('Content-type', 'application/yaml')
            self.send_header('Content-type', 'text/plain;charset=utf-8')
            # 原样返回特殊标头
            if self.subscription_userinfo:
                self.send_header('Subscription-Userinfo', self.subscription_userinfo)
            if self.profile_update_interval:
                self.send_header('Profile-Update-Interval', self.profile_update_interval)
            if self.content_disposition:
                self.send_header('Content-Disposition', self.content_disposition)
            if self.profile_web_page_url:
                self.send_header('Profile-Web-Page-Url', self.profile_web_page_url)
            self.end_headers()
            # 写入文件
            self.wfile.write(
                yaml.dump(modified_yaml, allow_unicode=True, default_flow_style=False, sort_keys=False).encode())
        else:
            self.send_error(500, "Unable to parse YAML files, possibly due to an incorrect YAML file")


def run_server(server_class=HTTPServer, handler_class=handler, port=8000):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
