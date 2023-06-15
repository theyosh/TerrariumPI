# pip install googletrans==4.0.0rc1

from googletrans import Translator
from pathlib import Path
import re
from time import sleep

destination_language = "ja"

translator = Translator(proxies=None)

source_string_regex = r"\":\s*\"(?P<source>.*)\",?$"
source_variable_regex = r"{([^{}]+)}"

source_translation = Path("../gui/locale/en_GB.json").read_text()
destination_translation = source_translation
source_translation_strings = re.findall(source_string_regex, source_translation, re.MULTILINE)

source_translation_strings = list(set(source_translation_strings))

source_counter = 0.0
total_source_lines = float(len(source_translation_strings))

print(f"Start translating {total_source_lines:.0f} strings.")

for source_string in source_translation_strings:
    # if 'plural' in source_string:
    #   source_translation_strings.extend(re.findall(source_variable_regex, source_string))
    #   continue

    source_counter += 1

    print(
        f"{source_counter:3.0f}/{total_source_lines:3.0f} ({(source_counter/total_source_lines)*100.0:6.2f}%): {source_string}",
        end=" -> ",
    )

    # Replace newlines '\n' to '||'
    source_translate_string = source_string.replace("\\n", "||")
    source_variables = re.findall(source_variable_regex, source_translate_string)

    variables = []

    if source_variables:
        for variable in source_variables:
            replace_variable = "{" + "".join([f"{character}_" for character in variable]) + "}"

            variable = "{" + variable + "}"
            variables.append((variable, replace_variable))

            source_translate_string = source_translate_string.replace(variable, replace_variable)

    try:
        sleep(0.5)
        destination_string = translator.translate(source_translate_string, dest=destination_language).text

        destination_string = destination_string.strip("-")

        # Strange spaces in variables due to Google translation
        destination_string = re.sub(r" ?_ ?", "_", destination_string)

        # Strange space missing in multiple sentences
        if len(destination_string) > 10:
            destination_string = re.sub(r"(\S)\.(\S)", r"\1. \2", destination_string)

    except Exception as ex:
        print(ex)
        continue

    for variable in variables:
        destination_string = re.sub(variable[1], variable[0], destination_string, flags=re.I)

    destination_string = re.sub(r"\s*\|\|\s*", "\\\\n", destination_string).strip()

    print(destination_string)

    destination_translation = destination_translation.replace(f': "{source_string}"', f': "{destination_string}"')

print("Final translation")
print(destination_translation.strip())
Path(f"../gui/locale/{destination_language}_TEST.json").write_text(destination_translation)
