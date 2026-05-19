import ssl
import urllib.request
import csv
import io

url = "https://data.kcg.gov.tw/File/DirectDownload/80bbbbd3-9ee4-4244-98e9-b4c08deda91b"

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

try:
    with urllib.request.urlopen(url, context=context) as response:
        raw_data = response.read()
        content_type = response.headers.get('Content-Type', 'Unknown')
        text = raw_data.decode("utf-8", errors="replace")
        
        print("\n===== 讀取結果 =====")
        print(f"URL: {url}")
        print(f"Content-Type: {content_type}")
        print(f"資料長度: {len(raw_data)} bytes")
        
        # 解析 CSV
        reader = csv.reader(io.StringIO(text))
        data = list(reader)
        
        if data:
            headers = data[0]
            rows = data[1:]
            
            print("\n===== 資料摘要 =====")
            print(f"總列數: {len(rows)}")
            print(f"欄位數: {len(headers)}")
            
            # 逐筆顯示資料
            for idx, row in enumerate(rows, 1):
                print(f"\n===== 第{idx}筆資料 =====")
                for header, value in zip(headers, row):
                    print(f"{header}: {value}")
        else:
            print("無法解析資料")
            
except Exception as e:
    print(f"讀取資料失敗：{e}")
