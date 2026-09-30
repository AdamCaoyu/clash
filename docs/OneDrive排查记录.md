# OneDrive 原配置与本次修正

## 找回的原配置

基线为 GitHub 提交 `810e577` 与桌面 `草鱼-自动.yaml`。原策略关系：

```text
☁️ OneDrive → 美国-自动（默认）
Ⓜ️ Microsoft → DIRECT（默认）
```

用户已确认：使用的是个人微软账号，面板手动选择“美国-自动”。本次保留这一用法；不把 OneDrive 合回普通 Microsoft。

旧 `list/OneDrive` 的内容如下，每行当时都带“美国节点”策略字段：

```text
DOMAIN-SUFFIX,onedrive.live.com,美国节点
DOMAIN-SUFFIX,storage.live.com,美国节点
DOMAIN-SUFFIX,1drv.com,美国节点
DOMAIN-SUFFIX,sharepoint.com,美国节点
DOMAIN-SUFFIX,sharepoint-df.com,美国节点
DOMAIN-SUFFIX,officeapps.live.com,美国节点
DOMAIN-SUFFIX,office.com,美国节点
DOMAIN-SUFFIX,live.com,美国节点
DOMAIN-SUFFIX,msedge.net,美国节点
DOMAIN-SUFFIX,trafficmanager.net,美国节点
```

因此原意是让 OneDrive、部分 Office 网页及相关微软地址走独立代理，不是只分出一个文件下载域名。

但旧仓库文件名为 `list/OneDrive`，模板却请求 `list/OneDrive.list`。桌面旧 YAML 中虽存在 OneDrive 组，却没有任何规则指向它；onedrive.live.com、1drv.com、sharepoint.com、login.live.com 等首先匹配 Microsoft。它也没有 rule-providers。因此只能确认那份桌面文件没有实现预期分流，不能拿它推断路由器此刻的完整运行状态或历史缓存选择。没有历史连接日志，无法证明这就是当时账号打不开的唯一原因。

## 上一版与现在的区别

| 版本 | OneDrive 默认 | 含义 |
| --- | --- | --- |
| 原模板 | 美国-自动 | 想独立代理，但存在规则路径错误 |
| 上一版 5f3a62d | Microsoft → 默认直连 | 不符合用户需要独立代理的用途 |
| 当前版本 | 美国-自动 | 恢复原选择；实际绑定完整基础列表及个人版补充 |

`🔑 微软登录` 默认跟随 `☁️ OneDrive`。个人登录、身份资源及 Graph API 可与文件访问用同一条出口；普通 `Ⓜ️ Microsoft` 仍默认直连，OneDrive 不再跟随它。登录组也能单独改为 Microsoft、DIRECT 或具体节点。

微软身份域名是共享的：其他使用相同微软登录 / Graph 地址的应用也会受登录组影响，域名规则不能按用户名区分账号。若需让某个微软应用的所有业务都保持同一出口，应把 Microsoft 组也选成同一具体节点；不要创建互相引用的组。此方案针对个人账号，企业组织的条件访问、设备合规和租户策略不由代理规则解决。

## 采用的范围与依据

继续引用 blackmatrix7 OneDrive 动态列表；个人补充维护在 `list/OneDrive.list`，旧无扩展名路径由脚本同步。补上个人版文件 API、Office 网页预览和 OneDrive 新入口；登录 / 身份资源单独维护在 `list/MicrosoftLogin.list`。

[微软个人版 OneDrive 端点文档](https://learn.microsoft.com/en-us/sharepoint/required-urls-and-ports)列有个人登录、Office 网页及 live.net 文件服务；[Microsoft 365 端点文档](https://learn.microsoft.com/en-us/microsoft-365/enterprise/urls-and-ip-address-ranges)补充身份验证与共享资源范围。[微软 OneDrive 团队说明](https://techcommunity.microsoft.com/blog/onedriveblog/now-on-demand--onedrive-office-hours--june-2026/4526529)确认新的 onedrive.cloud.microsoft 入口。

这些文档说明可达性需求，不等于要求使用美国代理；“美国-自动”来自用户原配置和实际选择。没有将微软文档中整个 microsoft.com、共享遥测平台和所有云服务统统纳入 OneDrive。

继续保留 office.com 的网页入口用途；不再用整个 live.com、msedge.net、trafficmanager.net 匹配 OneDrive。Outlook 邮件等仍属于 Microsoft；OneDrive / 登录中已确认的子域先匹配专门规则。

## 更新后核对

1. 更新原订阅；确认 OneDrive 仍选“美国-自动”，微软登录选“OneDrive”。有选择缓存时，新默认不一定覆盖旧选择，需看面板。
2. 测试个人账号登录、文件列表、上传下载和 Office 在线预览。查看连接日志中的域名、策略组和实际节点。
3. 若同一账号仍反复验证，可在 OneDrive 组直接选一个验证可用的美国具体节点；微软登录默认会一起跟随。自动组按延迟切换是原有功能，不代表同一公网 IP。
4. 本次未登录你的账号、未改路由器、未测试真实上传下载。若仍打不开，应记录错误、时间和命中域名继续定位，不能宣称已经修复实际账号问题。
