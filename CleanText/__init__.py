import aqt.editor
from aqt import gui_hooks

import os.path

PATH = os.path.dirname(os.path.realpath(__file__))


def delete_br_tag(text: str) -> str:
    split_text = text.split("<br>")
    return " ".join(split_text)


def clean_text(editor: aqt.editor.Editor):
    text = editor.note.values()[editor.currentField]
    editor.note[editor.note.keys()[editor.currentField]] = delete_br_tag(text)

    # Reload the note window
    editor.loadNote()


def add_clean_text_button(buttons, editor):
    """Function for 'editor_did_init_buttons' hook to add a button that executes context_cloze"""
    hotkey = "Ctrl+Alt+C"
    tooltip = f"Clean the text"
    return buttons.append(editor.addButton(os.path.join(PATH, "media", "clean.svg"),
                                           "clean_text",
                                           clean_text,
                                           tip=tooltip,
                                           keys=hotkey))


gui_hooks.editor_did_init_buttons.append(add_clean_text_button)
