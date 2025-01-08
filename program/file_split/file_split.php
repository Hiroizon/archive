<?php

class LogFileSplitter {
    private string $inputFile;
    private int $chunkSizeMB;
    private array $outputFiles = [];
    
    public function __construct(string $inputFile, int $chunkSizeMB = 100) {
        $this->inputFile = $inputFile;
        $this->chunkSizeMB = $chunkSizeMB;
    }
    
    public function split(): array {
        if (!file_exists($this->inputFile)) {
            throw new Exception("ファイルが見つかりません: {$this->inputFile}");
        }
        
        $fileSize = filesize($this->inputFile);
        $fileSizeMB = round($fileSize / (1024 * 1024), 2);
        echo "入力ファイルサイズ: {$fileSizeMB} MB\n";
        
        // 入力ファイルの情報を取得
        $pathInfo = pathinfo($this->inputFile);
        $baseName = $pathInfo['filename'];
        $extension = isset($pathInfo['extension']) ? '.' . $pathInfo['extension'] : '';
        
        $handle = fopen($this->inputFile, 'r');
        if ($handle === false) {
            throw new Exception("ファイルを開けません: {$this->inputFile}");
        }
        
        try {
            $partNumber = 1;
            $currentSize = 0;
            $currentContent = '';
            $chunkSizeBytes = $this->chunkSizeMB * 1024 * 1024;
            
            while (!feof($handle)) {
                $line = fgets($handle);
                if ($line === false) {
                    break;
                }
                
                $lineSize = strlen($line);
                
                // チャンクサイズを超える場合、新しいファイルに書き出し
                if ($currentSize + $lineSize > $chunkSizeBytes) {
                    $outputFile = "{$baseName}_part{$partNumber}{$extension}";
                    $this->writeChunk($outputFile, $currentContent);
                    $this->outputFiles[] = $outputFile;
                    
                    // リセット
                    $currentContent = $line;
                    $currentSize = $lineSize;
                    $partNumber++;
                } else {
                    $currentContent .= $line;
                    $currentSize += $lineSize;
                }
            }
            
            // 残りのコンテンツを書き出し
            if ($currentContent !== '') {
                $outputFile = "{$baseName}_part{$partNumber}{$extension}";
                $this->writeChunk($outputFile, $currentContent);
                $this->outputFiles[] = $outputFile;
            }
            
        } finally {
            fclose($handle);
        }
        
        echo "\n分割完了。作成されたファイル: " . count($this->outputFiles) . "個\n";
        return $this->outputFiles;
    }
    
    private function writeChunk(string $outputFile, string $content): void {
        if (file_put_contents($outputFile, $content) === false) {
            throw new Exception("ファイルの書き込みに失敗しました: {$outputFile}");
        }
        
        $sizeMB = round(strlen($content) / (1024 * 1024), 2);
        echo "作成: {$outputFile} ({$sizeMB} MB)\n";
    }
    
    public function getOutputFiles(): array {
        return $this->outputFiles;
    }
}

// 使用例
try {
    $splitter = new LogFileSplitter('db.log', 100);  // 100MBごとに分割
    $files = $splitter->split();
    
    echo "分割されたファイル:\n";
    foreach ($files as $file) {
        echo "- {$file}\n";
    }
} catch (Exception $e) {
    echo "エラーが発生しました: " . $e->getMessage() . "\n";
}

?>