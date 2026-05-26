import ssl
import urllib.request
import csv
import io
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, abort

app = Flask(__name__)

url = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file"


def resolve_header(headers, candidates):
    lower_headers = [h.lower() for h in headers]
    for candidate in candidates:
        for index, header in enumerate(lower_headers):
            if candidate in header:
                return headers[index]
    return None


def build_display_headers(headers):
    priority = [
        'title',
        'name',
        'subject',
        'description',
        'desc',
        'link',
        'url',
        'website',
        'date',
        'category'
    ]
    ordered = []
    for candidate in priority:
        for header in headers:
            if candidate in header.lower() and header not in ordered:
                ordered.append(header)
    for header in headers:
        if header not in ordered:
            ordered.append(header)
    return ordered


def fetch_data():
    """獲取遠端 CSV 資料"""
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(url, context=context) as response:
            raw_data = response.read()
            content_type = response.headers.get('Content-Type', 'Unknown')
            text = raw_data.decode('utf-8', errors='replace')

            reader = csv.reader(io.StringIO(text))
            data = list(reader)

            if not data:
                return {'success': False, 'error': '無法解析資料'}

            headers = data[0]
            rows = data[1:]
            records = [dict(zip(headers, row)) for row in rows]
            display_headers = build_display_headers(headers)
            link_field = resolve_header(headers, ['link', 'url', 'website', 'href'])
            title_field = resolve_header(headers, ['title', 'name', 'subject'])
            description_field = resolve_header(headers, ['description', 'desc', 'content', 'summary'])

            return {
                'success': True,
                'url': url,
                'content_type': content_type,
                'data_length': len(raw_data),
                'fetch_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'headers': headers,
                'display_headers': display_headers,
                'records': records,
                'link_field': link_field,
                'title_field': title_field,
                'description_field': description_field,
                'total_rows': len(rows),
                'total_columns': len(headers)
            }

    except Exception as e:
        return {'success': False, 'error': str(e)}


@app.route('/')
def index():
    data = fetch_data()
    return render_template('index.html', data=data)


@app.route('/table')
def table():
    data = fetch_data()
    return render_template('table.html', data=data)


@app.route('/details/')
def details_root():
    return redirect(url_for('table'))


@app.route('/details/<int:record_id>')
def details(record_id):
    data = fetch_data()
    if not data['success']:
        return render_template('details.html', data=data, record=None, record_id=None)

    if record_id < 1 or record_id > data['total_rows']:
        abort(404)

    record = data['records'][record_id - 1]
    return render_template('details.html', data=data, record=record, record_id=record_id)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
