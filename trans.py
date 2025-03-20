import re
import yaml
from googletrans import Translator

def translate_text_segments(text, translator, target_language='zh-CN'):
    """
    翻译文本片段，跳过站位符和换行符。

    Args:
        text (str): 要处理的文本。
        translator (googletrans.Translator): Google翻译器实例。
        target_language (str, optional): 目标语言代码，默认为中文简体 (zh-CN)。

    Returns:
        str: 翻译后的文本。
    """
    placeholder_pattern = r'(#[^#]*#|\$[^\$]*\$|\[[^\]]*\]|\n)'
    segments = re.split(placeholder_pattern, text)
    translated_segments =
    for segment in segments:
        if segment:  # 忽略空字符串
            if re.fullmatch(placeholder_pattern, segment):
                translated_segments.append(segment)
            else:
                try:
                    translation = translator.translate(segment, dest=target_language, src='en')
                    translated_segments.append(translation.text)
                except Exception as e:
                    print(f"翻译文本片段 '{segment}' 时发生错误：{e}")
                    translated_segments.append(segment)  # 保留原文如果翻译失败
    return "".join(translated_segments)

def translate_yaml_inplace(filepath, target_language='zh-CN', target_filepath=None):
    """
    读取 .yml 文件，使用 Google Translate 翻译引号内的英文文本（跳过站位符和换行符），
    并将结果写入目标文件（或覆盖源文件）。

    注意：此脚本使用非官方的 googletrans 库，可能不稳定。
          对于生产环境，建议使用官方翻译 API。

    Args:
        filepath (str): 要翻译的 .yml 文件的路径。
        target_language (str, optional): 目标语言代码，默认为中文简体 (zh-CN)。
        target_filepath (str, optional): 保存翻译后内容的目标文件路径。
                                        如果为 None，则会覆盖原始文件。默认为 None。
    """
    translator = Translator()
    modified_lines =
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                modified_line = line
                # 查找引号内的文本
                matches = re.findall(r'"([^"]*)"', line)
                for original_quoted_text in matches:
                    text_inside_quotes = original_quoted_text
                    translated_text = translate_text_segments(text_inside_quotes, translator, target_language)
                    # 使用字符串替换来更新行
                    modified_line = modified_line.replace(f'"{original_quoted_text}"', f'"{translated_text}"', 1)
                modified_lines.append(modified_line)

        output_filepath = target_filepath if target_filepath else filepath
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.writelines(modified_lines)

        print(f"文件 '{filepath}' 已尝试翻译并保存到 '{output_filepath}'。")

    except FileNotFoundError:
        print(f"错误：文件 '{filepath}' 未找到。")
    except yaml.YAMLError as e:
        print(f"错误：无法解析文件 '{filepath}'：{e}")
    except Exception as e:
        print(f"发生其他错误：{e}")

if __name__ == "__main__":
    source_file = input("请输入要翻译的 .yml 文件路径：")
    target_lang = input(f"请输入目标语言代码（默认为 zh-CN）：") or 'zh-CN'
    overwrite = input("是否直接覆盖源文件？ (yes/no): ").lower()

    target_file = None
    if overwrite != 'yes':
        target_file = input("请输入保存翻译后内容的目标文件路径（如果不想覆盖源文件）：")

    translate_yaml_inplace(source_file, target_lang, target_file)