# 草鱼的分流规则

在原有服务分组上维护：保留自动测速、直连兜底，为 Apple、Microsoft 及重要账号提供独立选节点的能力。

## 直接使用

沿用 OpenClash 中已有的订阅地址和订阅转换服务，只需保持自定义模板地址为：

```text
https://raw.githubusercontent.com/AdamCaoyu/clash/refs/heads/main/Clash-Full.ini
```

这是兼容入口，与 [config/openclash.ini](config/openclash.ini) 内容一致。不要把 INI 地址填写到机场“订阅地址”一栏；它属于“自定义模板地址”。本仓库不提供节点或新的转换服务。

[OneDrive 原配置与排查](docs/OneDrive排查记录.md) · [设置与更新步骤](docs/使用与维护.md) · [苹果专项说明](docs/苹果服务优化与使用说明.md) · [规则源对比](docs/规则来源与取舍.md) · [当前规则目录](docs/规则目录.md)

## 分组与默认行为

| 范围 | 行为 |
| --- | --- |
| 原有 32 个组 | 名称保留；10 个自动测速组仍为 url-test，180 秒检测、100 ms 切换容差 |
| 未匹配流量 | MATCH,DIRECT，黑名单模式 |
| 普通 Apple / Microsoft | 保留默认 DIRECT；可直接选具体节点，也保留原来的自动组选项 |
| OneDrive | 恢复美国-自动；保留独立选节点能力 |
| 微软登录 | 默认跟随 OneDrive；可独立调整，共享身份域名也影响其他微软应用 |
| Apple Intelligence | 默认跟随新增 ChatGPT 组；ChatGPT 初始跟随原 AI1 |
| Claude | 独立选择；初始跟随原 AI1 |
| Google / PayPal | 独立选择；分别默认跟随原“国外”组 / DIRECT |
| 媒体、社交、游戏 | 恢复原有独立分组和选项，没有合并成大组 |

原业务组的默认选择保留，OneDrive 已恢复原来的美国-自动。原模板多数业务组默认 DIRECT；面板中已有的选择是否保留由 OpenClash / 内核缓存决定，更新后应核对。要让黑名单中的国外网站走代理，可在“🌍 国外”选择原有自动组。

敏感服务组支持直接选择订阅中的具体节点，彼此独立。需要固定出口时请选择节点本身；选择“所有-自动”等自动组仍会按延迟切换。固定节点不能保证固定公网 IP 或避免账号风控。

## 只维护这些位置

- `config/`：唯一日常模板；根目录 `Clash-Full.ini` 为兼容副本。
- `list/`：个人补充列表及历史域名资料；[目录说明](list/README.md)标明实际使用项。
- `rules/clash/`：由个人列表生成的原生 Clash 规则集，与 `.list` 是同一套规则的不同格式。
- `docs/`：配置说明、来源、更新与回滚记录。
- `shadowrocket/`：下一阶段外出配置入口，尚无正式配置。
- `archive/`：历史配置索引，旧链接保留但不参与当前模板。
- `tests/`、`scripts/`：维护校验工具，不是订阅转换服务。

本地目录：`文稿/GitHub/我的Fork/clash`。私人 YAML / 订阅 / 节点信息只放 `.local/`，不提交 GitHub。

## 维护检查

```sh
python3 scripts/sync_templates.py
python3 -m unittest discover -s tests -v
```

原 Fork 来源：[liandu2024/clash](https://github.com/liandu2024/clash)。当前按个人使用需求选择性维护，不整体同步覆盖。
