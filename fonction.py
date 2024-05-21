def bind_tree(widget, event, callback, add=''):
    "Binds an event to a widget and all its descendants."

    widget.bind(event, callback, add)

    for child in widget.children.values():
        bind_tree(child, event, callback)