from django import forms

from apps.assistants.models import AssistantTool
from apps.core import widgets
from django_ace import AceWidget


class AssistantToolCreateForm(forms.ModelForm):
    function_logic = forms.CharField(
        widget=AceWidget(
            mode="python",
            theme="twilight",
            wordwrap=False,
            width="500px",
            height="300px",
            showprintmargin=True,
            usesofttabs=True,
            toolbar=True,
            showgutter=True,
            behaviours=True,
            extensions=["emmet", "beautify", "language_tools", "settings_menu"],
        )
    )
    function_descriptor = forms.CharField(
        widget=AceWidget(
            mode="json",
            wordwrap=False,
            width="500px",
            height="300px",
            showprintmargin=True,
            usesofttabs=True,
            toolbar=True,
            showgutter=True,
            behaviours=True,
        )
    )

    class Meta:
        model = AssistantTool
        fields = "__all__"
