[English](#english) | [简体中文](#%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

<br>

# English

This is an online implementation of Clash For Windows (CFW) configuration file preprocessing (parser) and mixin tools. Please refer to the CFW documentation for what CFW's parser and mixin are.

Even if CFW is no longer updated, you can continue using its parser and mixin features online through this tool without being constrained by certain implementations.

## Disclaimer

This tool is only intended for modifying YAML configuration files. It is merely a plain text file modification tool. It does not contain any content that violates any national laws or regulations.

## Warning

It's not recommended to use this service set up by others, as your query parameters are likely to be recorded, potentially revealing your subscription information.

Although it's not enabled by default, it can be done with just one line of code.

<br>

Additionally, this program has preset magic numbers that might allow others to use your subscription.

Please search for `jynb` in the main program and change the magic number to another value.

## Features

- Supports preprocessing of YAML configuration files.
- Implements basic parser and mixin functionalities (refer to CFW documentation for details).
- Advanced features might not be fully implemented. Please refer to the examples in this project.

## Typical Use Cases

1. Obtain subscription links from the subscription conversion and specify the rule set you like.
2. The rule set lacks certain rules or some are not suitable.
3. Use the parser feature to add nodes, rules, node groups, etc., to the configuration file.
4. Use the mixin feature to override parts of the configuration file, like `enhanced-mode: fake-ip`.
5. Get a satisfactory configuration file subscription link.

——————

1. Use across multiple devices, frequently changing subscriptions.
2. Use the magic number feature so that all devices use the same link.
3. Since it was designed to have a parser, you need to place a valid `parser.yaml`.
4. When updating the subscription, you only need to update the subscription link in `source.txt` on the server.
5. All devices will just need to update the subscription.

## Processing Flow

1. Get the subscription link (in Clash format) from local or query parameters.
2. Get `parser.yaml` from local or query parameters.
3. Get `mixin.yaml` from local or query parameters.
4. Download the subscription via the link and use `mixin.yaml` to override its content.
5. Preprocess it with `parser.yaml`.
6. Return the Clash-format configuration file.

## Deployment Instructions

#### Server Deployment

For deployment on a server, simply start it directly:

```
python3 parser.py
```

Then use NGINX or other reverse proxies for TLS encryption and port changes.

#### Serverless Deployment

You can easily deploy this application on a serverless platform like Vercel.

For Vercel deployment, refer to this repository: https://github.com/InoryS/Clash-Parser-Online-Vercel

## Usage Instructions

After deployment, send requests by constructing the following URLs:

```
https://your.domain/?source=<base64-encoded-subscription-url>&parser=<base64-encoded-parser.yaml-url>&mixin=<base64-encoded-mixin.yaml-url>
```

### Parameter Explanation

- `source`: Base64 encoded subscription link (Clash format).
- `parser`: Base64 encoded `parser.yaml` download link, same format as the CFW parser. This parameter is optional; if not provided, it will read locally. Refer to the project sample files and CFW documentation.
- `mixin`: Base64 encoded `mixin.yaml` download link, same format as the CFW mixin. This parameter is optional. Refer to the project sample files and CFW documentation.

Example requests:
```
https://example.com/?source=aHR0cDovL2xvY2FsaG9zdDoyNTUwMC9zdWI/dGFyZ2V0PWNsYXNoJm5ld19uYW1lPXRydWUmdXJsPXRlc3QmaW5zZXJ0PWZhbHNlJmNvbmZpZz1odHRwcyUzQSUyRiUyRnJhdy5naXRodWJ1c2VyY29udGVudC5jb20lMkZBQ0w0U1NSJTJGQUNMNFNTUiUyRm1hc3RlciUyRkNsYXNoJTJGY29uZmlnJTJGQUNMNFNTUl9PbmxpbmUuaW5p&parser=aHR0cHM6Ly9leGFtcGxlLmNvbS9wYXJzZXIueWFtbA==&mixin=aHR0cHM6Ly9leGFtcGxlLmNvbS9taXhpbi55YW1s
```

```
https://clash-parser-online-vercel.vercel.app/api?source=aHR0cDovL2xvY2FsaG9zdDoyNTUwMC9zdWI/dGFyZ2V0PWNsYXNoJm5ld19uYW1lPXRydWUmdXJsPXRlc3QmaW5zZXJ0PWZhbHNlJmNvbmZpZz1odHRwcyUzQSUyRiUyRnJhdy5naXRodWJ1c2VyY29udGVudC5jb20lMkZBQ0w0U1NSJTJGQUNMNFNTUiUyRm1hc3RlciUyRkNsYXNoJTJGY29uZmlnJTJGQUNMNFNTUl9PbmxpbmUuaW5p&parser=aHR0cHM6Ly9leGFtcGxlLmNvbS9wYXJzZXIueWFtbA==&mixin=aHR0cHM6Ly9leGFtcGxlLmNvbS9taXhpbi55YW1s
```

### Personal Use

For personal use, if you're too lazy to pass parameters, you can use the preset magic number (default is 'jynb') to automatically read the configuration from local files:

- To read files locally, you need to create `source.txt`, `parser.yaml`, `mixin.yaml`, and `mixin-premium.yaml` in the same directory or parent directory as `parser.py`.
- The first line of `source.txt` should contain the subscription link, and the second line should specify the encoding type (raw, url_encode, or base64).
- The format of `parser.yaml`, `mixin.yaml`, and `mixin-premium.yaml` follows the examples in this repository and the CFW documentation.
- This program has preset magic numbers, please read the personal use section

<br>

- If `source=magic number`, it reads the link from the local `source.txt`.
- If no `parser` is passed, `parser.yaml` reads the parser content locally.
- If `mixin=magic number`, it reads the mixin content from the local `mixin.yaml`.
- Additionally, mixin has two preset magic numbers: `jynb` corresponds to `mixin.yaml`, and `jynb-premium` corresponds to `mixin-premium.yaml`.

It's advisable to search for `jynb` in the main program and change the magic number to another value.

Example requests:
```
https://example.com/?source=jynb&mixin=jynb
```

```
https://clash-parser-online-vercel.vercel.app/api?source=jynb&mixin=jynb
```



<br>
<br>
<br>
<br>
<br>





# 简体中文

这是一个在线实现的 Clash For Windows(CFW) 的配置文件预处理 (Parser) 和 Mixin 工具，CFW 的 Parser 和 Mixin 是什么请参考 CFW 文档。

即使 CFW 不再更新，你也可以通过这个工具在线继续使用它的 Parser 和 Mixin 功能，且不再受限于某某实现。

为众人拾柴者，还是冻毙于风雪了。

## 免责声明

此工具仅用于对 YAML 配置文件进行修改，只是一个纯文本文件修改工具。它不包含违反任何国家法律法规的内容。

## 警告

不建议使用别人搭建的此服务，你的查询参数很可能会被记录，从而泄露你的订阅。

虽然默认不会，但要改也就 1 行代码的事。

<br>

此外，本程序有预设幻数，可能导致其他人使用你的订阅。

请在主程序中搜索 `jynb` 修改幻数为其他值。 

## 功能特性

- 支持 YAML 配置文件的预处理。
- 实现基本的 Parser 和 Mixin 功能。（功能请参考 CFW 文档）
- 高级功能可能实现不全，已实现请参考项目中的示例（虽然还是不全）。

## 典型使用场景

1. 从订阅转换获取订阅链接，并指定自己喜欢的规则集
2. 该规则集少了某些规则或者某些规则不合适
3. 使用 parser 功能向配置文件添加如节点、规则、节点组等
4. 使用 mixin 功能覆盖配置文件中的部分内容，如覆盖 enhanced-mode: fake-ip
5. 获得自己满意的配置文件订阅链接

——————

1. 多设备使用，经常更换订阅
2. 使用幻数功能，各设备都使用同一个链接
3. 设计初衷就是要 parser 的，所以你需要放置一个有效的 parser.yaml
4. 更新订阅时只需要更新服务器上 source.txt 中的订阅链接
5. 各设备更新订阅即可

## 处理流程

1. 从本地或查询参数获取订阅链接（clash 格式）
2. 从本地或查询参数获取 parser.yaml
3. 从本地或查询参数获取 mixin.yaml
4. 从订阅链接下载订阅并使用 mixin.yaml 对其内容进行覆盖
5. 使用 parser.yaml 对其进行预处理
6. 返回 clash 格式配置文件



## 部署说明

#### 服务器部署

部署在服务器上直接启动即可：

```
python3 parser.py
```

然后使用 NGINX 等反向代理进行 TLS 加密，修改端口等。

#### 无服务器部署

你也可以轻松地在如 Vercel 这样的无服务器平台上部署此应用。

在 Vercel 上部署请参考此仓库：https://github.com/InoryS/Clash-Parser-Online-Vercel



## 使用说明

部署后，通过构造以下 URL 发送请求：

```
https://your.domain/?source=<base64-encoded-subscription-url>&parser=<base64-encoded-parser.yaml-url>&mixin=<base64-encoded-mixin.yaml-url>
```

### 参数说明

- `source`: base64 编码后的订阅链接（Clash 格式）
- `parser`: base64 编码后的 `parser.yaml` 下载链接，格式与 CFW 的 parser 相同，此参数是可选的，如果不填默认从本地读取，内容可参考本项目示例文件以及 CFW 文档
- `mixin`: base64 编码后的 `mixin.yaml` 下载链接，格式与 CFW 的 mixin 相同，此参数是可选的，内容可参考本项目示例文件以及 CFW 文档
- 本程序有预设幻数，请阅读个人使用部分

请求例如：

```
https://example.com/?source=aHR0cDovL2xvY2FsaG9zdDoyNTUwMC9zdWI/dGFyZ2V0PWNsYXNoJm5ld19uYW1lPXRydWUmdXJsPXRlc3QmaW5zZXJ0PWZhbHNlJmNvbmZpZz1odHRwcyUzQSUyRiUyRnJhdy5naXRodWJ1c2VyY29udGVudC5jb20lMkZBQ0w0U1NSJTJGQUNMNFNTUiUyRm1hc3RlciUyRkNsYXNoJTJGY29uZmlnJTJGQUNMNFNTUl9PbmxpbmUuaW5p&parser=aHR0cHM6Ly9leGFtcGxlLmNvbS9wYXJzZXIueWFtbA==&mixin=aHR0cHM6Ly9leGFtcGxlLmNvbS9taXhpbi55YW1s
```

```
https://clash-parser-online-vercel.vercel.app/api?source=aHR0cDovL2xvY2FsaG9zdDoyNTUwMC9zdWI/dGFyZ2V0PWNsYXNoJm5ld19uYW1lPXRydWUmdXJsPXRlc3QmaW5zZXJ0PWZhbHNlJmNvbmZpZz1odHRwcyUzQSUyRiUyRnJhdy5naXRodWJ1c2VyY29udGVudC5jb20lMkZBQ0w0U1NSJTJGQUNMNFNTUiUyRm1hc3RlciUyRkNsYXNoJTJGY29uZmlnJTJGQUNMNFNTUl9PbmxpbmUuaW5p&parser=aHR0cHM6Ly9leGFtcGxlLmNvbS9wYXJzZXIueWFtbA==&mixin=aHR0cHM6Ly9leGFtcGxlLmNvbS9taXhpbi55YW1s
```


### 个人使用

对于个人使用，如果懒得传递参数，可以使用预设的幻数（默认为 'jynb'）从本地文件自动读取配置：

- 要从本地读取文件，你需要在 `parser.py` 的同目录或上层目录创建 `source.txt` 和 `parser.yaml` 和 `mixin.yaml` 以及 `mixin-premium.yaml`。
- `source.txt` 的第一行应写入订阅链接，第二行写订阅链接的编码类型（raw、url_encode 或 base64）。
- `parser.yaml` 和 `mixin.yaml` 以及 `mixin-premium.yaml` 文件格式参考本仓库示例以及 CFW 文档。

<br>

- 当 `source=幻数` 时，会从本地 `source.txt` 中读取连接。
- 当不传递 `parser` 参数时，会从本地 `parsr.yaml` 读取 parser 内容。
- 当 `mixin=幻数` 时，会从本地 `mixin.yaml` 中读取 mixin 内容。
- 额外的，mixin 有两个预设幻数，幻数 `jynb` 对应 `mixin.yaml`，幻数 `jynb-premium` 对应 `mixin-premium.yaml`


建议在主程序中搜索 `jynb` 修改幻数为其他值。 

请求例如：

```
https://example.com/?source=jynb&mixin=jynb
```

```
https://clash-parser-online-vercel.vercel.app/api?source=jynb&mixin=jynb
```





