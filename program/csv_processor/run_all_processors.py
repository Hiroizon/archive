import subprocess

def run_csv_processors():
    """
    csv_processor.py と csv_processor_2.py を実行する関数
    """
    try:
        print("csv_processor.py を実行します...")
        subprocess.run(["python", "csv_processor.py"], check=True)
        print("csv_processor.py の実行が完了しました。")

        print("\ncsv_processor_2.py を実行します...")
        subprocess.run(["python", "csv_processor_2.py"], check=True)
        print("csv_processor_2.py の実行が完了しました。")

        print("\nすべての処理が完了しました。")

    except subprocess.CalledProcessError as e:
        print(f"エラーが発生しました: {e}")
    except FileNotFoundError:
      print("エラー: Pythonファイルが見つかりません")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    run_csv_processors()