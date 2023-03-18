import aqt.editor
from aqt import mw
from aqt import gui_hooks

import os.path

PATH = os.path.dirname(os.path.realpath(__file__))
config = mw.addonManager.getConfig(__name__)


def delete_cloze_text(text: str) -> str:
    """Substitute the text between double square brackets by ' <span class="cloze">[..]</span> '"""
    prefix, cloze, suffix = get_cloze_text(text)
    return prefix + ' <span class="cloze">[..]</span> ' + suffix


def wrap_cloze_text(text: str) -> str:
    """Enclose the text between double square brackets with <span class"cloze"> </span>"""
    prefix, cloze, suffix = get_cloze_text(text)
    return prefix + '<span class="cloze">' + cloze + '</span>' + suffix


def get_cloze_text(text: str) -> tuple[str, str, str]:
    """Separate the text in the text before [[, the text between [[ and ]], and the text after ]]"""
    n = text.find("[[")
    m = text.find("]]")

    return text[:n], text[n+2: m], text[m+2:]


def context_cloze(editor: aqt.editor.Editor):
    """Main function of context cloze. Takes the original text and use it to fill the other fields"""
    text = editor.note[config["text"]]
    _, cloze, _ = get_cloze_text(text)
    editor.note[config["word"]] = cloze
    editor.note[config["deleted_text"]] = delete_cloze_text(text)
    editor.note[config["highlighted_text"]] = wrap_cloze_text(text)

    # Reload the note window
    editor.loadNote()


def wrap_context_cloze(editor: aqt.editor.Editor):
    """Wrap the selected text between [[ and ]]"""
    editor.web.eval("wrap('[[', ']]');")


def add_context_cloze_button(buttons, editor):
    """Function for 'editor_did_init_buttons' hook to add a button that executes context_cloze"""
    hotkey = config["cc_hotkey"]
    tooltip = f"Generate the context cloze fields ({hotkey})"
    return buttons.append(editor.addButton(os.path.join(PATH, config["media_dir"], config["cc_icon"]),
                                           "context_cloze",
                                           context_cloze,
                                           tip=tooltip,
                                           keys=hotkey))


def add_wrap_context_cloze_button(buttons, editor):
    """Function for 'editor_did_init_buttons' hook to add a button that executes wrap_context_cloze"""
    hotkey = config["wrap_hotkey"]
    tooltip = f"Wrap the text with [[]] ({hotkey})"
    return buttons.append(editor.addButton(os.path.join(PATH, config["media_dir"], config["wrap_icon"]),
                                           "wrap_context_cloze",
                                           wrap_context_cloze,
                                           tip=tooltip,
                                           keys=hotkey))


gui_hooks.editor_did_init_buttons.append(add_wrap_context_cloze_button)
gui_hooks.editor_did_init_buttons.append(add_context_cloze_button)
