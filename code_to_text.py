import os
import argparse
from pathlib import Path

# --- 設定 ---
MAX_SIZE_MB = 9.5  # 10MB制限に対し、余裕を持って9.5MB
MAX_BYTES = int(MAX_SIZE_MB * 1024 * 1024)

IGNORE_DIRS = {
    '.git', '__pycache__', 'node_modules', 'venv', '.venv', 
    '.vscode', '.idea', 'dist', 'build', 'out'
}
IGNORE_EXTS = {
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.pyc', '.exe', 
    '.dll', '.so', '.pdf', '.zip', '.tar', '.gz', '.pkl'
}
IGNORE_FILES = {'.DS_Store', 'package-lock.json', 'yarn.lock'}

def get_project_tree(root_path, output_name):
    """ディレクトリ構造を文字列として生成"""
    lines = [f"=== PROJECT STRUCTURE: {root_path.name} ==="]
    for path in sorted(root_path.rglob('*')):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.name == output_name or path.name in IGNORE_FILES or path.suffix in IGNORE_EXTS:
            continue
            
        depth = len(path.relative_to(root_path).parts)
        spacer = '  ' * (depth - 1)
        if path.is_dir():
            lines.append(f"{spacer}📁 {path.name}/")
        else:
            lines.append(f"{spacer}📄 {path.name}")
    return "\n".join(lines) + "\n" + "="*50 + "\n\n"

def generate_project_summary(target_dir, output_name):
    root_path = Path(target_dir).resolve()
    if not root_path.exists():
        print(f"エラー: ディレクトリが見つかりません: {root_path}")
        return

    # 1. 共通のヘッダー情報（ツリー構造）を作成
    tree_str = get_project_tree(root_path, output_name)
    
    # 2. 全ファイルの内容をメモリに集約（分割計算のため）
    file_entries = []
    for path in sorted(root_path.rglob('*')):
        if (path.is_file() and 
            not any(part in IGNORE_DIRS for part in path.parts) and
            path.name != output_name and
            path.name not in IGNORE_FILES and
            path.suffix not in IGNORE_EXTS):
            
            relative_path = path.relative_to(root_path)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    entry = f"--- START OF FILE: {relative_path} ---\n{content}\n--- END OF FILE: {relative_path} ---\n\n"
                    file_entries.append(entry)
            except (UnicodeDecodeError, PermissionError):
                continue

    # 3. 分割内容のシミュレーション
    parts = []
    current_part_content = []
    current_size = 0
    
    # ヘッダー（説明・ツリー）の概算サイズ（Part ◯/◻︎ は後で入れるため少し余裕を持つ）
    fixed_header_base = (
        "【ファイル説明】\n"
        "このファイルはプロジェクト全体のソースコードを分割して集約したものです。\n"
        "冒頭にディレクトリ構造を記載し、その後に各ファイルの内容を記述しています。\n\n"
    )

    for entry in file_entries:
        entry_size = len(entry.encode('utf-8'))
        # ヘッダー＋ツリー＋現在の内容＋新しいエントリ が制限を超えるか確認
        if current_size + entry_size > MAX_BYTES - (len(tree_str.encode('utf-8')) + 1000):
            if current_part_content:
                parts.append("".join(current_part_content))
                current_part_content = []
                current_size = 0
        
        current_part_content.append(entry)
        current_size += entry_size
    
    if current_part_content:
        parts.append("".join(current_part_content))

    # 4. 最終的なファイル書き出し
    total_parts = len(parts)
    output_files = []
    
    base_path = Path(os.getcwd()) / output_name
    stem = base_path.stem
    suffix = base_path.suffix

    for i, content in enumerate(parts, 1):
        part_file_name = f"{stem}_part{i:02d}{suffix}"
        part_path = base_path.parent / part_file_name
        
        with open(part_path, "w", encoding="utf-8") as f:
            # 各ファイルの冒頭に情報を集約
            f.write(f"【ファイル情報】パート {i} / {total_parts}\n")
            f.write(fixed_header_base)
            f.write(tree_str)
            f.write(content)
            
        output_files.append(part_path)

    # 結果表示
    print("-" * 30)
    print(f"✅ 処理が完了しました。")
    print(f"📂 対象ディレクトリ: {root_path}")
    print(f"📦 合計分割数: {total_parts}")
    print("📝 生成ファイル一覧:")
    for f in output_files:
        print(f"   - {f.absolute()}")
    print("-" * 30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM用のコード集約スクリプト（分割・ツリー・説明付き）")
    parser.add_argument("path", nargs="?", default=".", help="対象パス")
    parser.add_argument("-o", "--output", default="project_context.txt", help="出力名")
    
    args = parser.parse_args()
    generate_project_summary(args.path, args.output)
