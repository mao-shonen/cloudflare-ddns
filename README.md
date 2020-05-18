# cloudflare-ddns
自用cloudflare的DDNS腳本  
種花電信的固定IP實在是太爛了  
有些服務又不想浪費VPS的流量  
為了放在家裡只好隨手寫一個DDNS腳本


# 使用
## Docker
```bash
docker run -it -d \
  --name cloudflare-ddns \
  --restart unless-stopped \
  -e CLOUDFLARE_TOKEN={cloudflare_token} \
  -e CLOUDFLARE_ZONE_ID={cloudflare_zone_id} \
  -e CLOUDFLARE_RECORDS={mydomain.com|*.mydomain.com} \
  q267009886/cloudflare-ddns:latest
```


# 設定
環境變數            | 預設   | 說明
-------------------|--------|---
CLOUDFLARE_TOKEN   | `None` | cloudflare token https://dash.cloudflare.com/profile/api-tokens
CLOUDFLARE_ZONE_ID | `None` | 要更新的cloudflare zone id，在儀表板右側有寫
CLOUDFLARE_RECORDS | `None` | 要更新的cloudflare record，可以使用`|`填入多個，例 `mydomain.com|*.mydomain.com`
UPDATE_RATE        | 60.0   | 更新間隔秒數
LOG_LEVEL          | INFO   | 日誌等級 `DEBUG`、`INFO`、`WARN`、`ERROR`
