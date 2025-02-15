from django import forms


class HtmlEditor(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(HtmlEditor, self).__init__(*args, **kwargs)
        self.attrs["class"] = "html-editor"

    class Media:
        css = {
            "all": (
                "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/codemirror.css",
            )
        }
        js = (
            "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/codemirror.js",
            "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/mode/xml/xml.js",
            "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/mode/htmlmixed/htmlmixed.js",
            "/static/codemirror-5.9/init.js",
        )
