from aqt import gui_hooks


def replace_by_square_brackets(text: str) -> str:
    """Substitute the text between double square brackets by ' <span class="cloze">[..]</span> '"""
    prefix, cloze, suffix = get_cloze_text(text)
    return prefix + ' <span class="cloze">[..]</span> ' + suffix


def wrap_cloze_with_class(text: str) -> str:
    """Enclose the text between double square brackets with <span class"cloze"> </span>"""
    prefix, cloze, suffix = get_cloze_text(text)
    return prefix + '<span class="cloze">' + cloze + '</span>' + suffix


def get_cloze_text(text):
    """Separate the text in the text before [[, the text between [[ and ]], and the text after ]]"""
    n = text.find("[[")
    m = text.find("]]")

    return text[:n], text[n+2: m], text[m+2:]


def context_cloze(editor):
    text = editor.note["Original Text"]
    _, cloze, _ = get_cloze_text(text)
    editor.note["Word (Not fill)"] = cloze
    editor.note["Cloze (Not fill)"] = replace_by_square_brackets(text)
    editor.note["Hightlighted (Not fill)"] = wrap_cloze_with_class(text)

    # Reload the note
    editor.loadNote()


def wrap_context_cloze(editor):
    editor.web.eval("wrap('[[', ']]');")


def add_context_cloze_button(buttons, editor):
    return buttons.append(editor.addButton(None, "context_cloze", context_cloze))


def add_wrap_context_cloze_button(buttons, editor):
    return buttons.append(editor.addButton(None, "wrap_context_cloze", wrap_context_cloze))


gui_hooks.editor_did_init_buttons.append(add_wrap_context_cloze_button)
gui_hooks.editor_did_init_buttons.append(add_context_cloze_button)
