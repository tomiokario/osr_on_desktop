"""
引数で受け取った画像を文字起こしするスクリプト

使い方
 python osr_arg.py 画像PATH [言語オプション(jp/jp_v)]
 - 第一引数：画像PATH
 - 第二引数：言語オプション
    - jp            ：日本語横書き
    - jp_v          ：日本語横書き
    - その他(未指定)：英語
"""

# ライブラリ
from PIL import Image               # Python Image Library(画像処理)
import sys                          # system
sys.path.append('/path/to/dir')     # PATHの指定
import pyocr                        # PyOCR(OSRラッパー)
import pyocr.builders
import pyperclip                    # クリップボード


# 引数の取得
args    = sys.argv                  # 配列で受け取る

# 引数が不足の場合の処理
if len(args)<2:
    print("第一引数に文字起こししたい画像ファイルのPATHを入力してください")


# 画像PATHの取得
img_path = args[1]

# 言語設定
lang    = 'eng'                 # デフォルトは英語
if len(args)>2:
    if args[2]=='jp':           # jp->日本語横書き
        lang = 'jpn'
    elif args[2]=='jp_v':    # jp_v->日本語縦書き
        lang = 'jpn_vert'


# 文字起こし
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))

txt = tool.image_to_string(		# テキストの取得
    Image.open(img_path),
    lang,
    builder=pyocr.builders.TextBuilder()
)

# テキストを整形
txt = txt.replace('.\n','.\t')
txt = txt.replace('\n',' ')
txt = txt.replace('.\t','.\n')
txt = txt + '\n'

# クリップボードに保存
print("クリップボードにコピーしました．")
pyperclip.copy(txt)
