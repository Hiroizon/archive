import csv

def process_csv_remove_second_column(input_filepath, output_filepath):
    """
    CSVファイルから " を削除し、2列目を削除する関数

    Args:
        input_filepath (str): 入力CSVファイルのパス
        output_filepath (str): 出力CSVファイルのパス
    """
    try:
        with open(input_filepath, 'r', encoding='utf-8', newline='') as infile, \
             open(output_filepath, 'w', encoding='utf-8', newline='') as outfile:
            
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            
            for row in reader:
                # 2列目を削除
                if len(row) > 1:
                    del row[1]
                # 削除後、「"」を削除
                row = [cell.replace('"', '') for cell in row]
                writer.writerow(row)

        print(f"処理完了: {output_filepath} に出力しました。")

    except FileNotFoundError:
        print(f"エラー: ファイル {input_filepath} が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")


if __name__ == "__main__":
    input_csv_path = "requester_list_2.csv"  # 入力ファイルパス
    output_csv_path = "requester_list_2_processed.csv"  # 出力ファイルパス
    process_csv_remove_second_column(input_csv_path, output_csv_path)