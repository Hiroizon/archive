import csv
import glob
import os
from datetime import datetime

# 現在の日付を取得
current_date = datetime.now().strftime("%Y%m%d")

# 作業ディレクトリを設定
work_dir = rf"path to your directory"

# 作業ディレクトリに移動
os.chdir(work_dir)

# ファイル名を生成（パスを含む）
update_file = os.path.join(work_dir, f"db_update_{current_date}.sql")
select_file = os.path.join(work_dir, f"select_{current_date}.sql")
csv_command_file = os.path.join(work_dir, f"output_csv_{current_date}.txt")

# 'gear'で始まるCSVファイルを探す（現在のディレクトリで）
csv_files = glob.glob('gear*.csv')
if not csv_files:
    error_message = f"'gear'で始まるCSVファイルが見つかりません。検索ディレクトリ: {work_dir}"
    print(error_message)
    exit()

# 最初に見つかったファイルを使用
csv_file = csv_files[0]
print(f"使用するファイル: {csv_file}")

# エンコーディングを固定
encoding = 'shift_jis'

# UPDATE文とSELECT文を生成
update_statements = []
order_ids = []

try:
    with open(csv_file, 'r', encoding=encoding) as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダーをスキップ
        for row in reader:
            order_id = row[0]
            notification = row[1].strip()
            
            # 先頭の<br>を削除
            if notification.startswith('<br>'):
                notification = notification[4:]
            
            # SQLインジェクション対策：シングルクォートをエスケープ
            notification = notification.replace("'", "''")
            
            update_statement = f"""UPDATE dtb_web_order_detail SET notification = CONCAT(IFNULL(notification, ''), CASE WHEN notification IS NOT NULL THEN '<br>' ELSE '' END,'{notification}') WHERE web_sales_order_id = {order_id};"""
            update_statements.append(update_statement)
            order_ids.append(order_id)

    # UPDATE文をファイルに書き込む
    with open(update_file, 'w', encoding='utf-8') as file:
        file.write("BEGIN;\n")
        for statement in update_statements:
            file.write(statement + "\n")
    print(f"UPDATE文が {update_file} に保存されました。")

    # SELECT文を生成してファイルに書き込む
    select_statement = f"SELECT web_sales_order_id, notification FROM dtb_web_order_detail WHERE web_sales_order_id IN({','.join(order_ids)});"
    with open(select_file, 'w', encoding='utf-8') as file:
        file.write(select_statement + "\n")
    print(f"SELECT文が {select_file} に保存されました。")

    # MySQLコマンドを生成してファイルに書き込む
    mysql_command = f"""mysql -h rds-777ec-jp-prddb-1.c3wyyu0inhxz.ap-northeast-1.rds.amazonaws.com -P 3306 -usammy_appusr -p2y_#%mN4@TDJdz\\(B sammy_data -e "{select_statement}" | sed 's/"/""/g;s/\\t/","/g;s/^/"/;s/$/"/;s/\\n//g' > ./`date +%Y%m%d%H%M%S`_notification_list.csv"""
    
    with open(csv_command_file, 'w', encoding='utf-8') as file:
        file.write(mysql_command + "\n")
    print(f"CSV出力コマンドが {csv_command_file} に保存されました。")

except Exception as e:
    print(f"エラーが発生しました: {str(e)}")