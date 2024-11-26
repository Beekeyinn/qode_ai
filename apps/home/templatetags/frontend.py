import json
import os

from django import template
from django.conf import settings
from django.utils.safestring import SafeText, mark_safe

register = template.Library()

STATIC_URL = getattr(settings, "STATIC_URL")


def get_styles_import(manifest_root):
    imports = ""
    style = "style.css" if "style.css" in manifest_root.keys() else "styles.css"
    if manifest_root.get(style, False):
        imports = f"""
        <link rel='stylesheet' type='text/css' href='{STATIC_URL}reactUI/{manifest_root[style]['file']}' />
        """
    return imports


def get_imports(manifest, root):
    imports = ""
    if manifest.get("imports", False):
        imports = "".join(
            [
                f'<script rel="modulepreload" type="module" crossorigin src="{STATIC_URL}reactUI/{root[file]["file"]}"></script>'
                for file in manifest.get("imports", [])
            ]
        )
    return imports


def get_assets_imports(manifest):
    imports = ""
    if manifest.get("assets", False):
        imports = "".join(
            [
                f"<link rel='prefetch' href='{STATIC_URL}reactUI/{file}' as='image' >"
                for file in manifest["assets"]
            ]
        )
    return imports


def get_css_preload_imports(manifest):
    imports = ""
    if manifest.get("css", False):
        imports = "".join(
            [
                f'<link rel="preload" href="{STATIC_URL}reactUI/{file}" as="style" />'
                for file in manifest["css"]
            ]
        )
    return imports


def get_css_imports(manifest):
    imports = ""
    if manifest.get("css", False):
        imports = "".join(
            [
                f'<link rel="stylesheet" type="text/css" href="{STATIC_URL}reactUI/{file}" />'
                for file in manifest["css"]
            ]
        )
    return imports


def prefetch_all_files(manifest):
    html = manifest.get("index.html", {})
    style = "style.css" if "style.css" in manifest.keys() else "styles.css"
    import_files = [manifest[file]["file"] for file in html.get("imports", [])]
    css_files = html.get("css", [])
    assets_files = html.get("assets", [])
    ignored_files = (
        import_files + css_files + assets_files + [manifest.get(style, {}).get("file")]
    )

    js_files = [
        f"<link rel='prefetch' href='{STATIC_URL}reactUI/{path}'/>"
        for path in os.listdir(settings.VITE_APP_DIR)
        if "gz" not in path
        and path.split(".")[-1] in ["png", "jpg", "js", "css", "svg"]
        and path not in ignored_files
    ]
    return "\n".join(js_files)


def get_main_js_file(manifest):
    imports = f'<script type="module" defer src="{STATIC_URL}reactUI/{manifest["file"]}"></script>'
    return imports


@register.simple_tag
def render_vite_bundle() -> SafeText:
    try:
        fd = open(f"{settings.VITE_APP_DIR}/.vite/manifest.json", "r")
        manifest = json.load(fd)
    except:
        raise Exception(
            f"Vite manifest file not found or invalid. Maybe your {settings.VITE_APP_DIR}/.vite/manifest.json file is empty?"
        )
    index_manifest = manifest["index.html"]
    imports_files = get_imports(index_manifest, manifest)
    assets_imports = get_assets_imports(index_manifest)
    css_prefetch_import = get_css_preload_imports(index_manifest)
    css_import = get_css_imports(index_manifest)
    main_file = get_main_js_file(index_manifest)
    styles_import = get_styles_import(manifest)
    prefetch_files = prefetch_all_files(manifest)
    return mark_safe(
        f"""
        {main_file}
        {css_prefetch_import}
        {assets_imports}
        {prefetch_files}
        {imports_files}
        {styles_import}
        {css_import}
        """
    )
