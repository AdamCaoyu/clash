# 域名列表

当前个人维护源：Apple、ChatGPT、CaoyuDirect、CaoyuProxy、AI2、OneDrive、MicrosoftLogin、AppleCDN、GoogleCDN、AIOverrides、DisneyExtra、NetflixExtra、HBOExtra 的 `.list`。

`python3 scripts/sync_templates.py` 生成对应 `rules/clash/*.yaml`，并同步旧 `list/OneDrive` 地址。源文件不带策略字段，可以为未来 Shadowrocket 复用。主模板指定策略和顺序。

- Apple 是唯一 Apple AI 专项规则；AppleCDN 属于普通 Apple，分开维护。
- OneDrive 补充个人文件 / Office 网页入口，MicrosoftLogin 为共享身份资源；详见 [OneDrive 排查](../docs/OneDrive排查记录.md)。
- GoogleCDN / AIOverrides / 三份媒体 Extra 是已确认的范围或顺序修正，文件注释注明来源。
- Grok.list 兼容保留，当前 Grok 采用 MetaCubeX xai 动态源。

其他文件为 Fork 历史资料，保留旧链接；存在文件不代表持续更新或已启用。当前启用来源与先后顺序以 [规则目录](../docs/规则目录.md) 和 [模板](../config/openclash.ini) 为准。
