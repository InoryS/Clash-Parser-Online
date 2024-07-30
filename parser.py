#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: InoryS
# Git repository: https://github.com/InoryS/Clash-Parser-Online
# Version: 2024-07-30.5

import base64
import json
import logging
import re
import urllib

import yaml
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests


class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.subscription_userinfo = None
        self.profile_update_interval = None
        self.content_disposition = None
        self.profile_web_page_url = None
        self.user_agent = None
        self.magic_number = 'jynb'
        super().__init__(*args, **kwargs)

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
            response = requests.get(url, headers={'User-Agent': self.user_agent})
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
        except requests.RequestException as error:
            logging.exception(f"Error fetching YAML from {url}: {error}")
            self.send_error(500, f"Error fetching YAML from {url}: {error}")
            return None
        except Exception as error:
            logging.exception(f"Unknown error fetching YAML from {url}: {error}")
            self.send_error(500, f"Unknown error fetching YAML from {url}: {error}")
            return None

    @staticmethod
    def merge_yaml(source, mixin):
        # 应用 mixin
        for key, value in mixin.get('mixin', {}).items():
            if key in source:
                if isinstance(source[key], dict) and isinstance(value, dict):
                    source[key].update(value)
                else:
                    source[key] = value
            else:
                source[key] = value
        return source

    def modify_yaml(self, source_yaml, parser_yaml):
        # 根据 parser_yaml 中的规则修改 source_yaml
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
            logging.exception(f"Error modifying YAML: {error}")
            self.send_error(500, f"Error modifying YAML: {error}")
            return None

    @staticmethod
    def modify_list(source_yaml, key, operations):
        # 修改 source_yaml 中的列表
        list_name = key.split('-', 1)[1]
        source_list = source_yaml.get(list_name, [])

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
        try:
            path, operation, value = self.parse_command(command)
            logging.debug(f"Applying command: {command} -> path: {path}, operation: {operation}, value: {value}")

            # 查找并处理目标策略组
            target_group = self.find_proxy_group(source_yaml, path)
            if target_group is None:
                logging.debug(f"Target group not found for path: {path}, skipping")
                return  # 如果没有找到目标策略组，则跳过此命令

            if value.startswith('[]'):
                regex_pattern = value[2:]
                self.apply_regex_to_proxies(source_yaml, target_group, regex_pattern, operation)
            else:
                if operation == '+':
                    # 插入代理到特定位置
                    index = int(path[-1]) if path[-1].isdigit() else None
                    if index is not None and index < len(target_group['proxies']):
                        target_group['proxies'].insert(index, value)
                    else:
                        target_group['proxies'].append(value)  # 如果索引无效，则默认添加到末尾
                elif operation == '=':
                    # 覆盖指定位置
                    index = int(path[-1]) if path[-1].isdigit() else None
                    if index is not None and index < len(target_group['proxies']):
                        target_group['proxies'][index] = value
                    else:
                        target_group['proxies'] = [value]  # 如果索引无效，则覆盖整个列表
                elif operation == '_':
                    # 删除指定位置或匹配名称的代理
                    proxy_name = value.strip('()')
                    if proxy_name.isdigit():
                        index = int(proxy_name)
                        if 0 <= index < len(target_group['proxies']):
                            del target_group['proxies'][index]
                    else:
                        target_group['proxies'] = [proxy for proxy in target_group['proxies'] if proxy != proxy_name]

        except Exception as error:
            logging.exception(f"Error applying command {command}: {error}")
            self.send_error(500, f"Error applying command {command}")
            return

    @staticmethod
    def find_proxy_group(source_yaml, path):
        # 检查路径长度是否足够
        if len(path) < 2:
            logging.debug(f"Path too short: {path}")
            return None
        # 查找指定的策略组
        group_name = path[1]
        for group in source_yaml.get('proxy-groups', []):
            if group['name'] == group_name:
                return group
        return None

    @staticmethod
    def apply_regex_to_proxies(source_yaml, target_group, regex_pattern, operation):
        logging.debug(f"Applying regex Target group: {target_group}")
        logging.debug(f"Applying regex pattern: {regex_pattern}")
        # 使用正则表达式筛选代理
        regex = re.compile(regex_pattern)
        matched_proxies = [proxy['name'] for proxy in source_yaml.get('proxies', []) if regex.search(proxy['name'])]

        if operation == '+':
            # 将匹配的代理添加到目标策略组
            target_group['proxies'].extend(matched_proxies)
        if operation == '=':
            # 将匹配的代理覆盖原目标策略组
            target_group['proxies'] = matched_proxies
        if operation == '_':
            # 将匹配的代理从目标策略组移除
            target_group['proxies'] = [proxy for proxy in target_group['proxies'] if proxy not in matched_proxies]


    @staticmethod
    def parse_command(command):
        # 解析命令，支持 + = _ 三种操作符
        operators = ['+', '=', '_']
        regx_keys = ['[]proxyNames', '[]groupNames', '[]shuffledProxyNames']

        # 判断是否包含正则表达式特殊关键字
        is_regex = any(key in command for key in regx_keys)

        if is_regex:
            # 如果是正则表达式命令，只选择正则关键字左边的操作符
            for key in regx_keys:
                if key in command:
                    # 分割命令，确保操作符在正则关键字左边
                    parts = command.split(key, 1)
                    if len(parts) != 2:
                        raise ValueError("Invalid command format")
                    # 找到操作符
                    left_part = parts[0]
                    operation = next((op for op in operators if op in left_part), None)
                    if not operation:
                        raise ValueError("Invalid command format")
                    path = left_part.split('.')
                    path[-1] = f"{path[-1]}{key}"  # 将关键字重新加回路径中
                    value = key + parts[1]
                    logging.debug(f"Parsing command regx operation: {operation}")
                    logging.debug(f"Parsing command regx command: {command}")
                    logging.debug(f"Parsing command regx parts: {parts}")
                    logging.debug(f"Parsing command regx path: {path}")
                    logging.debug(f"Parsing command regx Value: {value}")
                    break
        else:
            # 对于普通命令，使用 rpartition 分割命令为三个部分
            operation = next((op for op in operators if op in command), None)
            if not operation:
                raise ValueError("Invalid command format")
            parts = command.rpartition(operation)
            if len(parts) != 3:
                raise ValueError("Invalid command format")
            path = parts[0].split('.')
            value = parts[2]
            logging.debug(f"Parsing command normal operation: {operation}")
            logging.debug(f"Parsing command normal command: {command}")
            logging.debug(f"Parsing command normal parts: {parts}")
            logging.debug(f"Parsing command normal path: {path}")
            logging.debug(f"Parsing command normal Value: {value}")

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

    def fetch_local_url_txt(self, file_name):
        """
        从 txt 文件内读取链接
        :param file_name: 文件名
        :return: 解析后的URL
        :rtype: str
        """
        file_path = ['../' + file_name, './' + file_name]

        for file in file_path:
            try:
                with open(file, 'r', encoding='utf-8') as opened_file:
                    url_raw = opened_file.readline().strip()  # 读取第一行，订阅链接
                    url_type = opened_file.readline().strip()  # 读取第二行，链接编码类型

                    # 根据第二行的内容选择解码方法
                    if url_type.lower() in ['base64', 'base64-encoded']:
                        url = base64.b64decode(url_raw).decode('utf-8')
                    elif url_type.lower() in ['urlencode', 'urlencoded', 'url_encode', 'url encode']:
                        url = urllib.parse.unquote(url_raw)
                    elif url_type.lower() in ['raw', 'default', 'normal']:
                        url = url_raw
                    else:
                        url = self.decode_raw_url(url_raw)

                    if url:
                        return url
            except FileNotFoundError:
                continue  # 尝试下一个文件路径
            except Exception as error:
                logging.exception(f"fetch_local_url_txt: Error in reading {file_name}: {error}")
                self.send_error(500, f"fetch_local_url_txt: Error in reading {file_name}")
                break

        logging.exception(f"fetch_local_url_txt: File {file_name} not found")
        self.send_error(500, f"fetch_local_url_txt: File {file_name} not found")

    def fetch_local_url_json(self, file_name, source_name):
        """
        从 json 文件内读取链接
        :param file_name: 文件名
        :param source_name: 订阅名称
        :return: 解析后的URL
        :rtype: str
        """
        file_path = ['../' + file_name, './' + file_name]

        for file in file_path:
            try:
                with open(file, 'r', encoding='utf-8') as opened_file:
                    json_raw = json.load(opened_file)
                    url_raw = json_raw.get('data', {}).get(source_name, {}).get('url')  # 订阅链接
                    url_type = json_raw.get('data', {}).get(source_name, {}).get('url_type')  # 链接编码类型

                    # 根据第二行的内容选择解码方法
                    if url_type.lower() in ['base64', 'base64-encoded']:
                        url = base64.b64decode(url_raw).decode('utf-8')
                    elif url_type.lower() in ['urlencode', 'urlencoded', 'url_encode', 'url encode']:
                        url = urllib.parse.unquote(url_raw)
                    elif url_type.lower() in ['raw', 'default', 'normal']:
                        url = url_raw
                    else:
                        url = self.decode_raw_url(url_raw)

                    if url:
                        return url
            except FileNotFoundError:
                continue  # 尝试下一个文件路径
            except Exception as error:
                logging.exception(f"fetch_local_url_json: Error in reading {file_name}: {error}")
                self.send_error(500, f"fetch_local_url_json: Error in reading {file_name}")
                break

        logging.exception(f"fetch_local_url_json: File {file_name} not found")
        self.send_error(500, f"fetch_local_url_json: File {file_name} not found")
        return

    def fetch_local_yaml(self, file_name):
        """
        读取本地 yaml 文件。
        :param file_name: 文件名
        :return: 文件内容的yaml对象
        :rtype: yaml object
        """
        file_path = ['../' + file_name, './' + file_name]

        for file in file_path:
            try:
                with open(file, 'r', encoding='utf-8') as opened_file:
                    return yaml.safe_load(opened_file)
            except FileNotFoundError:
                continue  # 尝试下一个文件路径
            except Exception as error:
                logging.exception(f"fetch_local_yaml: Error in reading {file_name}: {error}")
                self.send_error(500, f"fetch_local_yaml: Error in reading {file_name}")
                break

        logging.exception(f"fetch_local_yaml: File {file_name} not found")
        self.send_error(500, f"fetch_local_yaml: File {file_name} not found")
        return

    def do_GET(self):
        # 处理 favicon.ico 请求
        if self.path == '/favicon.ico':
            self.send_error(404, "favicon.ico Not Found")
            return

        # 只处理 /api 路径的请求
        if not self.path.startswith('/api'):
            self.send_error(404, "Not Found")
            return

        logging.info("Start processing")
        # 记录 UA 远程获取时原样使用
        self.user_agent = self.headers.get('User-Agent')

        source_url, parser_url, mixin_url, modified_yaml = None, None, None, None

        # 解析查询参数，并获取对应文件
        query_components = self.parse_query_parameters(self.path)
        try:
            source = query_components.get('source', [''])[0]
            source_split = source.split('-', 2)
            if len(source_split) == 2 and source_split[0] == self.magic_number:
                # 如果为 幻数-123 那么就从本地 source.json 中获取名为 123 的链接
                source_url = self.fetch_local_url_json('source.json', source_split[1])
                source_yaml = self.fetch_yaml(source_url, 'source')
            elif source == self.magic_number:  # 如果为幻数从本地 source.txt 获取第一行链接
                source_url = self.fetch_local_url_txt('source.txt')
                source_yaml = self.fetch_yaml(source_url, 'source')
            else:  # 否则尝试解码 base64
                source_url = base64.b64decode(source).decode()
                source_yaml = self.fetch_yaml(source_url, 'source')

            if not source_yaml:
                logging.error(f"Error in fetching source_yaml: The YAML content could not be retrieved or parsed.")
                self.send_error(500,
                                "Error in fetching source_yaml: The YAML content could not be retrieved or parsed.")
                return

            parser = query_components.get('parser', [''])[0]
            parser_split = parser.split('-', 2)
            if len(parser_split) == 2 and parser_split[0] == self.magic_number:  # 如果为 幻数-123 那么就从本地读取 parser-123.yaml
                parser_yaml = self.fetch_local_yaml('parser-' + parser_split[1] + '.yaml')
            elif parser == self.magic_number:  # 如果为 幻数 那么就从本地读取 mixin.yaml
                parser_yaml = self.fetch_local_yaml('parser.yaml')
            elif parser:  # 否则尝试解码 base64
                parser_url = base64.b64decode(parser).decode()
                parser_yaml = self.fetch_yaml(parser_url)
            else:  # 不提供 parser 参数就默认从本地获取，因为设计就是为了 parser，也是向前兼容
                parser_yaml = self.fetch_local_yaml('parser.yaml')

            if not parser_yaml:
                logging.error("Error in fetching parser_yaml: The YAML content could not be retrieved or parsed.")
                self.send_error(500,
                                "Error in fetching parser_yaml: The YAML content could not be retrieved or parsed.")
                return

            mixin = query_components.get('mixin', [''])[0]
            mixin_split = mixin.split('-', 2)
            if mixin:
                if len(mixin_split) == 2 and mixin_split[0] == self.magic_number:  # 如果为 幻数-123 那么就从本地读取 mixin-123.yaml
                    mixin_yaml = self.fetch_local_yaml('mixin-' + mixin_split[1] + '.yaml')
                elif mixin == self.magic_number:  # 如果为 幻数 那么就从本地读取 mixin.yaml
                    mixin_yaml = self.fetch_local_yaml('mixin.yaml')
                else:  # 否则尝试解码 base64
                    mixin_url = base64.b64decode(mixin).decode()
                    mixin_yaml = self.fetch_yaml(mixin_url)
            else:  # 不提供 mixin 就不处理
                mixin_yaml = None

        except Exception as error:
            logging.exception(f"Unable to decode URL: {error}")
            self.send_error(500, f"Unable to decode URL: {error}")
            return

        try:
            # 进行 mixin
            logging.info("Perform mixin")
            if source_yaml and mixin_yaml:
                source_yaml = self.merge_yaml(source_yaml, mixin_yaml)
        except Exception as error:
            logging.exception(f"Error in perform mixin: {error}")
            self.send_error(500, f"Error in perform mixin: {error}")
            return

        try:
            # 进行 parser
            if source_yaml and parser_yaml:
                logging.info("Perform parser")
                modified_yaml = self.modify_yaml(source_yaml, parser_yaml)
        except Exception as error:
            logging.exception(f"Error in perform parser: {error}")
            self.send_error(500, f"Error in perform parser: {error}")
            return

        if modified_yaml:
            # 发送正确响应
            logging.info("Successfully modified yaml")
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
            return
        else:
            logging.error("Unable to parse YAML files, possibly due to an incorrect YAML file structure.")
            self.send_error(500, "Unable to parse YAML files, possibly due to an incorrect YAML file structure.")
            return


def run_server(server_class=HTTPServer, handler_class=Handler, port=8000):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    logging.info(f"Starting HTTP server on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 由于vercel 原因，不能 global 也不能传递 init 参数
    # 请自行到 class 内 __init__ 方法的 self.magic_number = 'jynb' 修改 'jynb' 为你想要的值
    run_server()



