# 域名列表

## 当前直接维护并启用

- `Apple.list`：唯一 Apple Intelligence / Siri / PCC 专项规则源。
- `ChatGPT.list`：ChatGPT 服务域名，独立组供 Apple AI 默认跟随。
- `CaoyuDirect.list`：个人直连例外。
- `CaoyuProxy.list`：个人代理例外。
- `AI2.list`：原 AI2 的 Meta AI 部分；Perplexity 采用专项远程规则。

这五份经 `scripts/sync_templates.py` 生成 `rules/clash/*.yaml`，供 OpenClash 原生规则集使用。未来 Shadowrocket 可继续使用无策略字段的 `.list` 源。

## 兼容保留，不再参与日常模板

`Grok.list`、`OneDrive`、`OneDrive.list` 已修复格式；旧无扩展名 OneDrive 地址仍可用。日常模板的 Grok 使用 MetaCubeX xai 专项规则，OneDrive 使用 blackmatrix7 专项规则；这两份兼容列表已收窄共享域名和关键字。

其他 `.list` 是 Fork 继承的历史资料，保留旧链接；未被当前模板引用的文件不代表持续更新。不要因文件存在便全部订阅，也不要把此目录文件时间当作上游实时更新状态。

实际启用来源与先后顺序以 [当前规则目录](../docs/规则目录.md) 和 [主模板](../config/openclash.ini) 为准。
