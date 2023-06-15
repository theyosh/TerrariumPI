# coding=utf8

import json
import re
import shutil
from potojson import pofile_to_json
from pathlib import Path

from time import sleep
from googletrans import Translator

translator = Translator()

BASE_LANGUAGE = "en_US"
PO_DOMAIN = "terrariumpi"
JSON_FOLDER = "../gui/locale"
PO_FOLDER = "."


def getAvailableLanguages():
    folders = []
    for folder in Path(PO_FOLDER).iterdir():
        if folder.is_dir():
            folders.append(folder)

    return folders


def loadPOLanguage(locale):
    # Create a copy of the original, so we can manipulate the PO contents without loosing the original file

    po_file = getPOPath(str(locale)) + ".tmp.po"
    shutil.copyfile(getPOPath(str(locale)), po_file)

    file = Path(po_file)
    data = file.read_text()
    data = data.replace("#~ ", "")
    file.write_text(data)

    data = pofile_to_json(
        po_file,
        fallback_to_msgid=False,
        fuzzy=True,
        pretty=False,
        indent=2,
        language=None,
        plural_forms=None,
        as_dict=True,
    )
    file.unlink()

    return data


def loadJSONLanguage(locale):
    return json.load(Path(getJSONPath(str(locale), JSON_FOLDER)).open())


def getPOPath(locale, localeDir=PO_FOLDER):
    return localeDir + "/" + locale + "/LC_MESSAGES/" + PO_DOMAIN + ".po"


def getJSONPath(locale, localeDir):
    return localeDir + "/" + locale + ".json"


def saveJSONFile(locale, content):
    json_file = Path(getJSONPath(str(locale), JSON_FOLDER))
    json_file.write_text(json.dumps(content, indent=2, ensure_ascii=False))


def google_translate(source, dest_lang):
    destination_string = ""
    plural = "plural" in source
    source_variable_regex = r"{([^{}]+)}"

    if plural:
        # Uploaded {amount, plural, =1 {# audio file} other {# audio files}}
        prefix = variables = suffix = ""

        text_parts = re.match(r"^(?P<prefix>[^{}]*)(?P<variables>{.*}})(?P<suffix>[^{}]*)$", source)

        if text_parts.group("prefix"):
            sleep(0.1)
            prefix = translator.translate(text_parts.group("prefix"), dest=dest_lang).text.strip() + " "

        if text_parts.group("suffix"):
            sleep(0.1)
            suffix = " " + translator.translate(text_parts.group("suffix"), dest=dest_lang).text.strip()

        if text_parts.group("variables"):
            variables = text_parts.group("variables")
            source_variables = re.findall(source_variable_regex, text_parts.group("variables"))
            for source_variable in source_variables:
                sleep(0.1)
                trans = translator.translate(source_variable, dest=dest_lang).text.strip()
                variables = variables.replace(source_variable, trans)

        destination_string = (prefix + variables + suffix).strip()

    else:
        # Replace newlines '\n' to '||'
        source_translate_string = source.replace("\\n", "||")
        source_variables = re.findall(source_variable_regex, source_translate_string)

        variables = []

        if source_variables:
            for variable in source_variables:
                replace_variable = "{" + "".join([f"{character}_" for character in variable]) + "}"

                variable = "{" + variable + "}"
                variables.append((variable, replace_variable))

                source_translate_string = source_translate_string.replace(variable, replace_variable)

        # try:
        sleep(0.1)
        destination_string = translator.translate(source_translate_string, dest=dest_lang).text

        destination_string = destination_string.strip("-")

        # Strange spaces in variables due to Google translation
        destination_string = re.sub(r" ?_ ?", "_", destination_string)

        # Strange space missing in multiple sentences
        if len(destination_string) > 10:
            destination_string = re.sub(r"(\S)\.(\S)", r"\1. \2", destination_string)

        # except Exception as ex:
        #   print(ex)

        for variable in variables:
            destination_string = re.sub(variable[1], variable[0], destination_string, flags=re.I)

        destination_string = re.sub(r"\s*\|\|\s*", "\\\\n", destination_string).strip()

    # print(f'Google translate: {source} -> {destination_string}')
    # print(destination_string)
    return destination_string


def walk(node, key, source, dest):
    if isinstance(node, dict):
        return {k: walk(v, k, source, dest) for k, v in node.items()}
    elif isinstance(node, list):
        return [walk(x, key, source, dest) for x in node]
    else:
        translation = translate(node, source, dest)
        print(f"{dest}: Translated {node} -> {translation}")
        return translation


def case_sensitive_replace(s, before, after):
    regex = re.compile(re.escape(before), re.I)
    return regex.sub(lambda x: "".join(d.upper() if c.isupper() else d.lower() for c, d in zip(x.group(), after)), s)


def translate(node, source, dest):
    copy = dest[:2] == "en"

    if node == "":
        return None

    translation = ""
    regex = r"(?P<var>\{[^ \}]+\})"
    matches = re.findall(regex, str(node), re.IGNORECASE) or []

    fullstopend = node.endswith(".")

    # Replace variables back to '%s' so we can match it in the PO file
    for match in matches:
        node = node.replace(match, "%s", 1)

    if node in source:
        # Found translation
        translation = source[node]

    elif fullstopend and node[:-1] in source:
        #    print('Found translation missing a full stop. So add it')
        translation = source[node[:-1]] + "."

    elif not fullstopend and node + "." in source:
        #    print('Found translation that has a full stop. FIX??')
        translation = source[node + "."]

    elif node != "":
        # Find case insensitive versions
        for key, value in source.items():
            if key.lower() == node.lower():
                translation = value
                break

    if copy and translation == "":
        translation = node

    # Convert '%s' back to the original variables
    for match in matches:
        translation = translation.replace("%s", match, 1)
        node = node.replace("%s", match, 1)

    if translation == "":
        # Google fallback
        try:
            translation = google_translate(node, dest)
        except Exception as ex:
            print(f"Error translating with Google: {node}")
            print(ex)

    return translation


# Disabled
# if __name__ == '__main__':
#   language_filter = ['fr_BE']
#   locales     = getAvailableLanguages()
#   source_json = loadJSONLanguage(BASE_LANGUAGE)

#   for locale in locales:
#     if str(locale) == BASE_LANGUAGE or str(locale) not in language_filter:
#       continue


#     locale_source = loadPOLanguage(locale)
#     locale_json   = walk(source_json, None, locale_source, str(locale)[:2])

#     # existing_locale = loadJSONLanguage(locale)
#     # locale_json.update(existing_locale)

#     saveJSONFile(locale,locale_json)
