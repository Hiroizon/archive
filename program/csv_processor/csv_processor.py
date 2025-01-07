import re

def _remove_rows_with_4digit_first_column(content):
    """
    1列目のカラムが4桁の場合にその行を削除する処理を行う関数

    Args:
        content (str): CSVファイルの内容 (文字列)
    
    Returns:
        str : 4桁の1列目を持つ行が削除されたCSVファイルの内容(文字列)
    """
    lines = content.splitlines()
    filtered_lines = []
    for line in lines:
      if not line: # 空行はそのまま返す
        filtered_lines.append(line)
        continue
      parts = line.split(',', 1) # 最初の,で分割
      if len(parts) > 0:
          first_column = parts[0]
          if len(first_column) == 4 and first_column.isdigit():
              continue  # 4桁ならスキップして次の行へ
      filtered_lines.append(line)
    return "\n".join(filtered_lines)

def process_csv(input_filepath, output_filepath):
    """
    CSVファイルを処理する関数

    Args:
        input_filepath (str): 入力CSVファイルのパス
        output_filepath (str): 出力CSVファイルのパス
    """
    try:
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            content = infile.read()

        # ①「"」を置換で消す
        content = content.replace('"', '')

        # ② "NULL"という文字列を置換で消す
        content = content.replace('NULL', '')

        # ③ メールアドレスの末尾+,の置換
        patterns = [
            r'(\.jp),,',
            r'(\.com),,',
            r'(\.biz),,',
            r'(t),,',
            r'(g),,',
            r'(b),,',
            r'(\.net),,'
        ]
        
        for pattern in patterns:
           content = re.sub(pattern, r'\1,', content)

        # 1列目が4桁の行を削除する処理
        content = _remove_rows_with_4digit_first_column(content)


        with open(output_filepath, 'w', encoding='utf-8', newline='') as outfile:
            outfile.write(content)

        print(f"処理完了: {output_filepath} に出力しました。")

    except FileNotFoundError:
        print(f"エラー: ファイル {input_filepath} が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")


if __name__ == "__main__":
    input_csv_path = "requester_list_1.csv"  # 入力ファイルパス
    output_csv_path = "requester_list_1_processed.csv"  # 出力ファイルパス
    process_csv(input_csv_path, output_csv_path)