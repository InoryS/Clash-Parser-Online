[English](#english) | [简体中文](#%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

<br>

# English

This is an online implementation of the Clash For Windows (CFW)-style configuration file preprocessor (Parser) and Mixin tool. For details on what CFW-style Parser and Mixin are, please refer to the CFW documentation or the examples in this repository.

In other words, you can continue writing configuration file preprocessors in the CFW style and use them with any client implementation.

Even if CFW is no longer updated, you can continue using its Parser and Mixin features online through this tool, without being restricted to any specific implementation.

For those who contribute to the firewood, yet still freeze in the snow.

## Disclaimer

This tool is only for modifying YAML configuration files and is simply a plain text file modification tool. It does not contain any content that violates the laws or regulations of any country.

## Warning

It is not recommended to use this service hosted by others, as your query parameters may be logged, potentially leaking your subscription.

Although it is not the default behavior, it only takes one line of code to change this.

Additionally, this program has preset magic numbers, which may cause others to use your subscription.

Please search for `jynb` in the main program to change the magic number to another value.

## Features

- Implements the basic Parser and Mixin functionalities of CFW (limited to YAML method, please refer to CFW documentation for features).
- Some advanced command features may not be fully implemented. Please refer to the project examples for features that have been implemented (though the examples are still not complete).

## Typical Use Cases
Scenario 1
1. Obtain a subscription link via conversion and specify your preferred rule set.
2. The rule set may lack certain rules or contain rules that are not suitable.
3. Use the parser feature to add/delete/override nodes, node groups, rules, rule groups, etc., in the configuration file.
4. Use the mixin feature to override parts of the configuration file, such as enhanced-mode: fake-ip, DNS settings, program settings, etc.
5. Obtain a subscription link with your desired configuration.

Scenario 2
1. Multiple devices in use, frequently changing subscriptions.
2. Use the magic number feature to have all devices use the same link.
3. Since the design intention is to use a parser, you need to place a valid parser.yaml (it can be empty, but it must exist).
4. When updating subscriptions, you only need to update the subscription link in source.txt on the server, without needing to change the link on your devices.
5. Each device can update subscriptions by itself.

Scenario 3
1. Many subscriptions to process or simply want to add a relay layer.
2. Use magic number parameters to easily manage multiple subscription links.
3. When updating subscriptions, only update the subscription link in source.json on the server without needing to change the link on your devices.
4. Each device can update subscriptions by itself.

## Processing Flow

1. Obtain the subscription link (in Clash format) from the local file or query parameters.
2. Obtain parser.yaml from the local file or query parameters.
3. Obtain mixin.yaml from the local file or query parameters (optional).
4. Download the subscription YAML file from the subscription link.
5. Override its contents with mixin.yaml (optional).
6. Preprocess it using parser.yaml.
7. Return a configuration file in Clash format.

## Deployment Instructions

#### Server Deployment

Clone this repository to the server.

Install dependencies
```
pip install -r requirements.txt
```

Then just start it:

```
python3 parser.py
```

Default listener `127.0.0.1:8000`

Then use a reverse proxy such as NGINX for TLS encryption, change the port, etc.

You should be careful to protect your source.txt and other files from being accessed externally, these files can be placed in the upper directory.

#### Serverless Deployment

You can also easily deploy this application on a serverless platform such as Vercel.

When deploying on a serverless platform, you should be careful to protect your source.txt and other files from being directly accessed externally, for example, use Vercel's vercel.json to redirect these files to other files.

For deployment on Vercel, please refer to this repository: https://github.com/InoryS/Clash-Parser-Online-Vercel

## Instructions

After deployment, send a GET request by constructing the following URL:

```
https://example.com/?source=<base64-encoded-subscription-url>&parser=<base64-encoded-parser.yaml-url>&mixin=<base64-encoded-mixin.yaml-url>
```

### Parameter Description

- `source`: base64-encoded subscription link (Clash format)

- `parser`: base64-encoded `parser.yaml` download link, the basic format is the same as CFW's parser, but the `parsers:` header should be removed and it should start with `yaml:` directly. For the content, please refer to the sample files of this project and the CFW documentation (this parameter is optional, if not passed **it will be read from the local by default**)
- `mixin`: download link of `mixin.yaml` encoded in base64, the format is the same as CFW's mixin, the content can refer to the sample file of this project and CFW documentation (this parameter is optional, if not passed, it will not be processed)
- **This program has a preset magic number**, when the parameter passed is a magic number, it can read the file from the local, please read the personal use section and the request example belowy: https://github.com/InoryS/Clash-Parser-Online-Vercel

#### Request Examples

You can decode the base64 data to see what is being passed in.

These are valid requests that you can copy and paste into your browser to see what you get.

The files for these request examples are in [this repository](https://github.com/InoryS/Clash-Parser-Online-Vercel):

A valid complete request:
```
https://clash-parser-online-vercel.vercel.app/api?source=aHR0cHM6Ly9zdWIueGV0b24uZGV2L3N1Yj90YXJnZXQ9Y2xhc2gmdXJsPWh0dHBzJTNBJTJGJTJGcmF3LmdpdGh1YnVzZXJjb250ZW50Lm NvbSUyRklub3J5UyUyRkNsYXNoLVBhcnNlci1PbmxpbmUtVmVyY2VsJTJGbWFpbiUyRmNsYXNoLnlhbWwmaW5zZXJ0PWZhbHNlJmNvbmZpZz1odHRwcyUzQSUyRiUyRnJhdy5naXRod WJ1c2VyY29udGVudC5jb20lMkZBQ0w0U1NSJTJGQUNMNFNTUiUyRm1hc3RlciUyRkNsYXNoJTJGY29uZmlnJTJGQUNMNFNTUl9PbmxpbmVfRnVs bF9NdWx0aU1vZGUuaW5pJmVtb2ppPXRydWUmbGlzdD1mYWxzZSZ0Zm89dHJ1ZSZmZG49ZmFsc2Umc29ydD10cnVlJmNsYXNoLmRvaD10cnVlJm5ld19uYW1lPXRydWUmYXB wZW5kX3R5cGU9dHJ1ZSZ1ZHA9dHJ1ZSZpbnRlcnZhbD00MzIwMCZ0bHMxMz10cnVlJnNjdj1mYWxzZQ==&parser=aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcm NvbnRlbnQuY29tL0lub3J5Uy9DbGFzaC1QYXJzZXItT25saW5lLVZlcmNlbC9tYWluL3BhcnNlci55YW1s&mixin=YUhSMGNITTZMeTl5WVhjdVoybDBhSFZpZFhObGNtTnZiblJsYm5RdVkyOXRMMGx 1YjNKNVV5OURiR0Z6YUMxUVlYSnpaWEl0VDI1c2FXNWxMVlpsY21ObGJDOXRZV2x1TDNCaGNuTmxjaTU1WVcxcw==
```

A valid request without a mixin parameter request:
```
https://clash-parser-online-vercel.vercel.app/api?source=aHR0cHM6Ly9zdWIueGV0b24uZGV2L3N1Yj90YXJnZXQ9Y2xhc2gmdXJsPWh0dHBzJTNBJTJGJTJGcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSUyRklub3J5U yUyRkNsYXNoLVBhcnNlci1PbmxpbmUtVmVyY2VsJTJGbWFpbiUyRmNsYXNoLnlhbWwmaW5zZXJ0PWZhbHNlJmNvbmZpZz1odHRwcyUzQSUyRiUyRnJhdy5naXRodWJ1c2VyY29udGV udC5jb20lMkZBQ0w0U1NSJTJGQUNMNFNTUiUyRm1hc3RlciUyRkNsY XNoJTJGY29uZmlnJTJGQUNMNFNTUl9PbmxpbmVfRnVsbF9NdWx0aU1vZGUuaW5pJmVtb2ppPXRydWUmbGlzdD1mYWxzZSZ0Zm89dHJ1ZSZmZG49ZmFsc2Umc29ydD10cnVlJmNsYXNoLmRvaD10cnVlJm5ld19uYW1lPXRydWUmYXBwZW5kX3R5cGU9dHJ1Z SZ1ZHA9dHJ1ZSZpbnRlcnZhbD00MzIwMCZ0bHMxMz10cnVlJnNjdj1mYWxzZQ==&parser=aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0lub3J5Uy9DbGFzaC1QYXJzZXItT25saW5lLVZlcmNlbC9tYWluL3BhcnNlci55YW1s
```

A valid request without a parser parameter (using the local parser.yaml for parser) request:
```
https://clash-parser-online-vercel.vercel.app/api?source=aHR0cHM6Ly9zdWIueGV0b24uZGV2L3N1Yj90YXJnZXQ9Y2xhc2gmdXJsPWh0dHBzJTNBJTJGJTJGcmF3LmdpdGh1YnVz ZXJjb250ZW50LmNvbSUyRklub3J5UyUyRkNsYXNoLVBhcnNlci1PbmxpbmUtVmVyY2VsJTJGbWFpbiUyRmNsYXNoLnlhbWwmaW5zZXJ0PWZhbHNlJmNvbmZpZz1odHRwcyUzQSUy RiUyRnJhdy5naXRodWJ1c2VyY2 9udGVudC5jb20lMkZBQ0w0U1NSJTJGQUNMNFNTUiUyRm1hc3RlciUyRkNsYXNoJTJGY29uZmlnJTJGQUNMNFNTUl9PbmxpbmVfRnVsbF9NdWx0aU1vZGUuaW5pJmVtb2ppPXRydWU mbGlzdD1mYWxzZSZ0Zm89dHJ1 ZSZmZG49ZmFsc2Umc29ydD10cnVlJmNsYXNoLmRvaD10cnVlJm5ld19uYW1lPXRydWUmYXBwZW5kX3R5cGU9dHJ1ZSZ1ZHA9dHJ1ZSZpbnRlcnZhbD00MzIwMCZ0bHMxMz10c nVlJnNjdj1mYWxzZQ==
```


### Magic Number Example
**`jynb` is the preset magic number**

The files for these request examples are located in [this repository](https://github.com/InoryS/Clash-Parser-Online-Vercel):

Read subscription connections from source.txt and parse them using local parser.yaml (no parser parameter is passed to use local files by default):
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb
```

Read subscription connections from source.txt and parse them using local parser.yaml:
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb&parser=jynb
```

Read subscription connections from source.txt and parse them using local parser.yaml, and then use local mixin.yaml to parse them mixin:
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb&parser=jynb&mixin=jynb
```

Version 2024-08-17.1 and later can use magic parameters to specify subscription connections and files:

Read subscription connections from data.test.url in source.json and parse with local parser.yaml:
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb-test
```

Read subscription connections from data.example.url in source.json and parse with local parser-test.yaml:
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb-example&parser=jynb-test
```

Read subscription connections from data.example1.url in source.json and parse with local parser-test.yaml: Read subscription connection, parse it with local parser-test.yaml, and then mix it with local mixin.yaml:
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb-example1&parser=jynb-test&mixin=jynb
```

Read subscription connection from data.test.url in source.json, parse it with local parser-test.yaml, and then mix it with local mixin-premium.yaml:
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb-test&parser=jynb-test&mixin=jynb-premium
```

Read subscription connection from source.txt, parse it with local parser-test.yaml, and then mix it with local mixin-premium.yaml mixin:
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb&parser=jynb-test&mixin=jynb-premium
```

### Personal use -- Magic number usage

For personal use, if you are too lazy to pass parameters, you can use the preset magic number (default is 'jynb') to automatically read the configuration from the local file:

- To read files from the local, you need to create `source.txt` or `source.json` and `parser.yaml` and `mixin.yaml` in the same directory or the upper directory of `parser.py`.
- The first line of `source.txt` should write the subscription link, and the second line should write the encoding type of the subscription link (raw, url_encode or base64).
- Using `source.json` allows you to manage multiple subscription connections. The format refers to this repository. `url` should write the subscription link, `url_type` can be raw, url_encode or base64, and `url_name` is a comment.
- The file formats of `parser.yaml` and `mixin.yaml` refer to the examples in this repository and the CFW documentation.

<br>

- When `source=magic`, the connection is read from the local `source.txt`.
- When the `parser` parameter is not passed, the parser content is read from the local `parsr.yaml`, which can be empty but must be present.
- When `mixin=magic`, the mixin content is read from the local `mixin.yaml`.

Version 2024-08-17.1 and later can use magic parameters to specify subscription connections and files:

- When `source=magic-foobar`, the connection is read from data.foobar.url in the local `source.json`.
- When `source=magic-example`, the connection is read from data.example.url in the local `source.json`.
-
- When `parser=magic-example`, the parser content is read from the local `parser-example.yaml`.
- When `parser=magic-foobar`, the parser content will be read from the local `parser-foobar.yaml`.
-
- When `mixin=magic-example`, the mixin content will be read from the local `mixin-example.yaml`.
- When `mixin=magic-foobar`, the mixin content will be read from the local `mixin-foobar.yaml`.

See above for example requests.
<br>

**Please be sure to search for `jynb` in the main program (parser.py or index.py) and modify the magic number to other values, otherwise it is easy to be stolen by others. **
<br>


### Public use

Deploy directly and delete the local yaml file. Of course, there will be no problem keeping it.

Just don't provide source.

Others can access with complete parameters.




<br>
<br>
<br>
<br>
<br>





# 简体中文

这是一个在线实现的 Clash For Windows(CFW) 风格的配置文件预处理 (Parser) 和 Mixin 工具，CFW 风格的 Parser 和 Mixin 是什么请参考 CFW 文档，或参考本仓库文件示例。

也就是说，你可以继续以 CFW 风格来编写配置文件预处理，并且可以在任何客户端实现使用。

即使 CFW 不再更新，你也可以通过这个工具在线继续使用它的 Parser 和 Mixin 功能，且不再受限于某某实现。

为众人拾柴者，还是冻毙于风雪了。

## 免责声明

此工具仅用于对 YAML 配置文件进行处理，只是一个纯文本文件修改工具，其输出完全依赖于用户输入，程序本身并不能产生任何数据。

它不包含违反任何国家法律法规的内容。

## 警告

不建议使用别人搭建的此服务，你的查询参数很可能会被记录，从而泄露你的订阅。

虽然默认不会，但要改也就 1 行代码的事。

<br>

此外，本程序有预设幻数，可能导致其他人使用你的订阅。

请在主程序中搜索 `jynb` 修改幻数为其他值。 

## 功能特性

- 实现基本 CFW 的 Parser 和 Mixin 功能。（仅限 YAML 方法，功能请参考 CFW 文档）
- 高级 command 功能可能实现不全，已实现请参考项目中的示例（虽然还是不是完整示例）。

## 典型使用场景
场景1
1. 从订阅转换获取订阅链接，并指定自己喜欢的规则集
2. 该规则集少了某些规则或者某些规则不合适
3. 使用 parser 功能向配置文件添加/删除/覆盖 节点、节点组、规则、规则组等
4. 使用 mixin 功能覆盖配置文件中的部分内容，如覆盖 enhanced-mode: fake-ip、DNS 设置、程序设置等
5. 获得自己满意的配置文件订阅链接


场景2
1. 多设备使用，经常更换订阅
2. 使用幻数功能，各设备都使用同一个链接
3. 设计初衷就是要 parser 的，所以你需要放置一个有效的 parser.yaml (可以为空，但必须有）
4. 更新订阅时只需要更新服务器上 source.txt 中的订阅链接，而不需要更换设备上的链接
5. 各设备更新订阅即可


场景3
1. 订阅众多，希望都进行处理，或是单纯想加一层中转
2. 使用幻数功能的幻数参数，便捷管理多个订阅链接
3. 更新订阅时只需要更新服务器上 source.json 中的订阅链接，而不需要更换设备上的链接
4. 各设备更新订阅即可


## 处理流程

1. 从本地或查询参数获取订阅链接（clash 格式）
2. 从本地或查询参数获取 parser.yaml
3. 从本地或查询参数获取 mixin.yaml (可选)
4. 从获取到的订阅链接下载订阅 yaml 文件
5. 使用 mixin.yaml 对其内容进行覆盖 (可选)
6. 使用 parser.yaml 对其进行预处理
7. 返回 clash 格式配置文件



## 部署说明

#### 服务器部署

克隆本仓库到服务器。

安装依赖
```
pip install -r requirements.txt
```

然后直接启动即可：

```
python3 parser.py
```

默认监听 `127.0.0.1:8000`

然后使用 NGINX 等反向代理进行 TLS 加密，修改端口等。

你应该注意保护你的 source.txt 等文件不可被外部访问，这些文件可以放在上层目录。

#### 无服务器部署

你也可以轻松地在如 Vercel 这样的无服务器平台上部署此应用。

在无服务器平台部署时，你应该注意保护你的 source.txt 等文件不可被外部直接访问，例如使用 Vercel 的 vercel.json 将这些文件重定向到其他文件。

在 Vercel 上部署请参考此仓库：https://github.com/InoryS/Clash-Parser-Online-Vercel


## 使用说明

部署后，通过构造以下 URL 发送 GET 请求：

```
https://example.com/?source=<base64-encoded-subscription-url>&parser=<base64-encoded-parser.yaml-url>&mixin=<base64-encoded-mixin.yaml-url>
```

### 参数说明

- `source`: base64 编码后的订阅链接（Clash 格式）
- `parser`: base64 编码后的 `parser.yaml` 下载链接，基本格式与 CFW 的 parser 相同但要去掉 `parsers:` 头，直接以 `yaml:` 开头，内容可参考本项目示例文件以及 CFW 文档（此参数是可选的，如果不传递**默认从本地读取**）
- `mixin`: base64 编码后的 `mixin.yaml` 下载链接，格式与 CFW 的 mixin 相同，内容可参考本项目示例文件以及 CFW 文档（此参数是可选的，不传递则不处理）
- **本程序有预设幻数**，传入参数为幻数时可以从本地读取文件，请阅读个人使用部分以及下面的请求示例


#### 请求示例

你可以解码 base64 数据看看传入了什么。

这些是有效请求，你可以复制到浏览器请求查看会得到什么。

这些请求示例的文件位于[此仓库](https://github.com/InoryS/Clash-Parser-Online-Vercel)：


一个完整的请求：
```
https://clash-parser-online-vercel.vercel.app/api?source=aHR0cHM6Ly9zdWIueGV0b24uZGV2L3N1Yj90YXJnZXQ9Y2xhc2gmdXJsPWh0dHBzJTNBJTJGJTJGcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSUyRklub3J5UyUyRkNsYXNoLVBhcnNlci1PbmxpbmUtVmVyY2VsJTJGbWFpbiUyRmNsYXNoLnlhbWwmaW5zZXJ0PWZhbHNlJmNvbmZpZz1odHRwcyUzQSUyRiUyRnJhdy5naXRodWJ1c2VyY29udGVudC5jb20lMkZBQ0w0U1NSJTJGQUNMNFNTUiUyRm1hc3RlciUyRkNsYXNoJTJGY29uZmlnJTJGQUNMNFNTUl9PbmxpbmVfRnVsbF9NdWx0aU1vZGUuaW5pJmVtb2ppPXRydWUmbGlzdD1mYWxzZSZ0Zm89dHJ1ZSZmZG49ZmFsc2Umc29ydD10cnVlJmNsYXNoLmRvaD10cnVlJm5ld19uYW1lPXRydWUmYXBwZW5kX3R5cGU9dHJ1ZSZ1ZHA9dHJ1ZSZpbnRlcnZhbD00MzIwMCZ0bHMxMz10cnVlJnNjdj1mYWxzZQ==&parser=aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0lub3J5Uy9DbGFzaC1QYXJzZXItT25saW5lLVZlcmNlbC9tYWluL3BhcnNlci55YW1s&mixin=YUhSMGNITTZMeTl5WVhjdVoybDBhSFZpZFhObGNtTnZiblJsYm5RdVkyOXRMMGx1YjNKNVV5OURiR0Z6YUMxUVlYSnpaWEl0VDI1c2FXNWxMVlpsY21ObGJDOXRZV2x1TDNCaGNuTmxjaTU1WVcxcw==
```

一个无 mixin 参数的有效请求：
```
https://clash-parser-online-vercel.vercel.app/api?source=aHR0cHM6Ly9zdWIueGV0b24uZGV2L3N1Yj90YXJnZXQ9Y2xhc2gmdXJsPWh0dHBzJTNBJTJGJTJGcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSUyRklub3J5UyUyRkNsYXNoLVBhcnNlci1PbmxpbmUtVmVyY2VsJTJGbWFpbiUyRmNsYXNoLnlhbWwmaW5zZXJ0PWZhbHNlJmNvbmZpZz1odHRwcyUzQSUyRiUyRnJhdy5naXRodWJ1c2VyY29udGVudC5jb20lMkZBQ0w0U1NSJTJGQUNMNFNTUiUyRm1hc3RlciUyRkNsYXNoJTJGY29uZmlnJTJGQUNMNFNTUl9PbmxpbmVfRnVsbF9NdWx0aU1vZGUuaW5pJmVtb2ppPXRydWUmbGlzdD1mYWxzZSZ0Zm89dHJ1ZSZmZG49ZmFsc2Umc29ydD10cnVlJmNsYXNoLmRvaD10cnVlJm5ld19uYW1lPXRydWUmYXBwZW5kX3R5cGU9dHJ1ZSZ1ZHA9dHJ1ZSZpbnRlcnZhbD00MzIwMCZ0bHMxMz10cnVlJnNjdj1mYWxzZQ==&parser=aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0lub3J5Uy9DbGFzaC1QYXJzZXItT25saW5lLVZlcmNlbC9tYWluL3BhcnNlci55YW1s
```

一个无 parser 参数的有效请求（使用本地的 parser.yaml 进行 parser）：
```
https://clash-parser-online-vercel.vercel.app/api?source=aHR0cHM6Ly9zdWIueGV0b24uZGV2L3N1Yj90YXJnZXQ9Y2xhc2gmdXJsPWh0dHBzJTNBJTJGJTJGcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSUyRklub3J5UyUyRkNsYXNoLVBhcnNlci1PbmxpbmUtVmVyY2VsJTJGbWFpbiUyRmNsYXNoLnlhbWwmaW5zZXJ0PWZhbHNlJmNvbmZpZz1odHRwcyUzQSUyRiUyRnJhdy5naXRodWJ1c2VyY29udGVudC5jb20lMkZBQ0w0U1NSJTJGQUNMNFNTUiUyRm1hc3RlciUyRkNsYXNoJTJGY29uZmlnJTJGQUNMNFNTUl9PbmxpbmVfRnVsbF9NdWx0aU1vZGUuaW5pJmVtb2ppPXRydWUmbGlzdD1mYWxzZSZ0Zm89dHJ1ZSZmZG49ZmFsc2Umc29ydD10cnVlJmNsYXNoLmRvaD10cnVlJm5ld19uYW1lPXRydWUmYXBwZW5kX3R5cGU9dHJ1ZSZ1ZHA9dHJ1ZSZpbnRlcnZhbD00MzIwMCZ0bHMxMz10cnVlJnNjdj1mYWxzZQ==
```


### 幻数示例
**`jynb` 为预设幻数**

这些请求示例的文件位于[此仓库](https://github.com/InoryS/Clash-Parser-Online-Vercel)：

从 source.txt 中读取订阅连接，并使用本地的 parser.yaml 进行 parser（没有传递 parser 参数默认使用本地文件）：
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb
```

从 source.txt 中读取订阅连接，并使用本地的 parser.yaml 进行 parser：
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb&parser=jynb
```

从 source.txt 中读取订阅连接，并使用本地的 parser.yaml 进行 parser，然后使用本地的 mixin.yaml 进行 mixin：
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb&parser=jynb&mixin=jynb
```



版本  2024-08-17.1 及之后可以使用幻数参数来指定订阅连接和文件:

从 source.json 中的 data.test.url 读取订阅连接，并使用本地的 parser.yaml 进行 parser：
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb-test
```

从 source.json 中的 data.example.url 读取订阅连接，并使用本地的 parser-test.yaml 进行 parser：
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb-example&parser=jynb-test
```

从 source.json 中的 data.example1.url 读取订阅连接，并使用本地的 parser-test.yaml 进行 parser，然后使用本地的 mixin.yaml 进行 mixin：
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb-example1&parser=jynb-test&mixin=jynb
```

从 source.json 中的 data.test.url 读取订阅连接，并使用本地的 parser-test.yaml 进行 parser，然后使用本地的 mixin-premium.yaml 进行 mixin：
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb-test&parser=jynb-test&mixin=jynb-premium
```

从 source.txt 中读取订阅连接，并使用本地的 parser-test.yaml 进行 parser，然后使用本地的 mixin-premium.yaml 进行 mixin：
```
https://clash-parser-online-vercel.vercel.app/api?source=jynb&parser=jynb-test&mixin=jynb-premium
```


### 个人使用--幻数使用

对于个人使用，如果懒得传递参数，可以使用预设的幻数（默认为 'jynb'）从本地文件自动读取配置：

- 要从本地读取文件，你需要在 `parser.py` 的同目录或上层目录创建 `source.txt` 或 `source.json` 和 `parser.yaml` 和 `mixin.yaml`。
- `source.txt` 的第一行应写入订阅链接，第二行写订阅链接的编码类型（raw、url_encode 或 base64）。
-  使用 `source.json` 可以让你管理多个订阅连接，格式参考本仓库，`url` 应写入订阅链接，`url_type` 可以为 raw、url_encode 或 base64，`url_name` 是注释。
- `parser.yaml` 和 `mixin.yaml` 文件格式参考本仓库示例以及 CFW 文档。

<br>

- 当 `source=幻数` 时，会从本地 `source.txt` 中读取连接。
- 当不传递 `parser` 参数时，会从本地 `parsr.yaml` 读取 parser 内容，文件可以为空，但必须有。
- 当 `mixin=幻数` 时，会从本地 `mixin.yaml` 中读取 mixin 内容。

版本  2024-08-17.1 及之后可以使用幻数参数来指定订阅连接和文件：

- 当 `source=幻数-foobar` 时，会从本地 `source.json` 中的 data.foobar.url 读取连接。
- 当 `source=幻数-example` 时，会从本地 `source.json` 中的 data.example.url 读取连接。
- 
- 当 `parser=幻数-example` 时，会从本地 `parser-example.yaml` 读取 parser 内容。
- 当 `parser=幻数-foobar` 时，会从本地 `parser-foobar.yaml` 读取 parser 内容。
- 
- 当 `mixin=幻数-example` 时，会从本地 `mixin-example.yaml` 读取 mixin 内容。
- 当 `mixin=幻数-foobar` 时，会从本地 `mixin-foobar.yaml` 读取 mixin 内容。

请求示例请查看上方。
<br>

**请务必在主程序(parser.py 或 index.py)中搜索 `jynb` 修改幻数为其他值，否则容易被他人盗用。**
<br>


### 公共使用

**不建议使用别人搭建的此服务，你的查询参数很可能会被记录，从而泄露你的订阅.**

直接部署，删除本地 yaml 文件即可，当然保留也不会有什么问题。

只要不提供 source 就行。

其他人带完整参数访问。

