# 草鱼的分流规则

台湾固定节点为主，Netflix 默认新加坡；Apple Intelligence 与普通苹果服务分开，重要账号共用稳定出口。

## 直接使用

沿用 OpenClash 中已有的订阅地址和订阅转换服务，只需保持自定义模板地址为：

```text
https://raw.githubusercontent.com/AdamCaoyu/clash/refs/heads/main/Clash-Full.ini
```

这是兼容入口，与 [config/openclash.ini](config/openclash.ini) 内容一致。不要把 INI 地址填写到机场“订阅地址”一栏；它属于“自定义模板地址”。本仓库不提供节点或新的转换服务。

[设置与更新步骤](docs/使用与维护.md) · [苹果专项说明](docs/苹果服务优化与使用说明.md) · [规则源对比](docs/规则来源与取舍.md) · [当前规则目录](docs/规则目录.md)

## 默认策略

| 业务 | 默认出口 |
| --- | --- |
| 日常国外网站、国际媒体、游戏商店 | 台湾固定 |
| Apple Intelligence / ChatGPT、其他 AI | 稳定账号 → 台湾固定 |
| Google、GitHub、Microsoft、OneDrive | 稳定账号 → 台湾固定 |
| PayPal、Amazon | 稳定账号 → 台湾固定 |
| Netflix | 新加坡固定 |
| 普通 Apple、国内网站、Steam 国内下载 | DIRECT |
| 未分类流量 | 日常代理 → 台湾固定，可手动改为直连 |

“固定”指手动选定节点，不按延迟自动切换；不是固定公网 IP 服务。账号、AI、Netflix 是否可用还取决于节点出口和服务条件。

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
