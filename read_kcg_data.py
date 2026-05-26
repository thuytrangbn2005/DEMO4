import ssl
import urllib.request
import csv
import io
from datetime import datetime
from itertools import zip_longest

url = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file"

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

try:
    with urllib.request.urlopen(url, context=context) as response:
        raw_data = response.read()
        content_type = response.headers.get('Content-Type', 'Unknown')
        text = raw_data.decode("utf-8", errors="replace")
        
        # 解析 CSV
        csv_file = io.StringIO(text)
        reader = csv.DictReader(csv_file)
        headers = reader.fieldnames or []
        rows = list(reader)
        
        # 準備輸出內容
        output_lines = []
        
        output_lines.append("\n" + "="*80)
        output_lines.append("讀取結果")
        output_lines.append("="*80)
        output_lines.append(f"URL: {url}")
        output_lines.append(f"Content-Type: {content_type}")
        output_lines.append(f"資料長度: {len(raw_data)} bytes")
        output_lines.append(f"讀取時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if rows:
            output_lines.append("\n" + "="*80)
            output_lines.append("資料摘要")
            output_lines.append("="*80)
            output_lines.append(f"總列數: {len(rows)}")
            output_lines.append(f"欄位數: {len(headers)}")
            output_lines.append(f"\n欄位列表:")
            for i, header in enumerate(headers, 1):
                output_lines.append(f"  {i}. {header}")
            
            # 逐筆顯示所有資料
            output_lines.append("\n" + "="*80)
            output_lines.append("詳細資料")
            output_lines.append("="*80)
            
            for idx, row in enumerate(rows, 1):
                output_lines.append(f"\n───── 第{idx}筆資料 ─────")
                for header in headers:
                    output_lines.append(f"{header}: {row.get(header, '')}")
                extra_keys = [k for k in row.keys() if k not in headers]
                for key in extra_keys:
                    output_lines.append(f"{key}: {row.get(key, '')}")
        else:
            output_lines.append("無法解析資料")
        
        # 輸出到終端機
        output_text = "\n".join(output_lines)
        print(output_text)
        
        # 保存到檔案
        output_file = "output_result.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_text)
        
        print(f"\n{'='*80}")
        print(f"✓ 結果已保存到: {output_file}")
        print(f"{'='*80}\n")
            
except Exception as e:
    print(f"讀取資料失敗：{e}")
