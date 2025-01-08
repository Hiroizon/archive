import os
from pathlib import Path

def split_log_file(input_file: str, chunk_size_mb: int = 100) -> list[str]:
    """
    ログファイルを指定されたサイズで分割します。

    Args:
        input_file: 入力ファイルのパス（.logファイルを想定）
        chunk_size_mb: 分割後の1ファイルあたりの最大サイズ（MB単位）

    Returns:
        作成された分割ファイルのパスのリスト
    """
    chunk_size = chunk_size_mb * 1024 * 1024  # MBをバイトに変換
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {input_file}")
    
    # ファイルサイズをチェック
    file_size = input_path.stat().st_size
    print(f"入力ファイルサイズ: {file_size / (1024*1024):.2f} MB")
    
    # 出力ファイル名のベース部分を作成
    base_name = input_path.stem
    extension = input_path.suffix  # 元の拡張子（.log）を保持
    output_files = []
    
    try:
        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            file_number = 1
            current_size = 0
            current_content = []
            
            for line in f:
                line_size = len(line.encode('utf-8'))
                
                # 現在のチャンクが指定サイズを超える場合、新しいファイルに書き出し
                if current_size + line_size > chunk_size:
                    output_file = f"{base_name}_part{file_number}{extension}"
                    with open(output_file, 'w', encoding='utf-8') as out_f:
                        out_f.writelines(current_content)
                    output_files.append(output_file)
                    print(f"作成: {output_file} ({current_size / (1024*1024):.2f} MB)")
                    
                    # 変数をリセット
                    current_content = [line]
                    current_size = line_size
                    file_number += 1
                else:
                    current_content.append(line)
                    current_size += line_size
            
            # 残りのコンテンツを最後のファイルに書き出し
            if current_content:
                output_file = f"{base_name}_part{file_number}{extension}"
                with open(output_file, 'w', encoding='utf-8') as out_f:
                    out_f.writelines(current_content)
                output_files.append(output_file)
                print(f"作成: {output_file} ({current_size / (1024*1024):.2f} MB)")
    
    except UnicodeDecodeError:
        print("警告: ファイルの読み込み中にエンコーディングエラーが発生しました。")
        print("バイナリモードで再試行します...")
        
        # バイナリモードでの読み込みを試行
        with open(input_file, 'rb') as f:
            file_number = 1
            current_size = 0
            current_content = bytearray()
            
            while True:
                chunk = f.read(8192)  # 8KBずつ読み込み
                if not chunk:
                    break
                
                if current_size + len(chunk) > chunk_size:
                    output_file = f"{base_name}_part{file_number}{extension}"
                    with open(output_file, 'wb') as out_f:
                        out_f.write(current_content)
                    output_files.append(output_file)
                    print(f"作成: {output_file} ({current_size / (1024*1024):.2f} MB)")
                    
                    current_content = bytearray(chunk)
                    current_size = len(chunk)
                    file_number += 1
                else:
                    current_content.extend(chunk)
                    current_size += len(chunk)
            
            if current_content:
                output_file = f"{base_name}_part{file_number}{extension}"
                with open(output_file, 'wb') as out_f:
                    out_f.write(current_content)
                output_files.append(output_file)
                print(f"作成: {output_file} ({current_size / (1024*1024):.2f} MB)")
    
    return output_files

# 使用例
if __name__ == "__main__":
    try:
        # .logファイルを100MBごとに分割
        result_files = split_log_file("db.log", chunk_size_mb=100)
        print(f"\n分割完了。作成されたファイル: {len(result_files)}個")
    except Exception as e:
        print(f"エラーが発生しました: {e}")