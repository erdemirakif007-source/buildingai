"""design/tokens.json -> tokens.css (web) + theme.ts (Expo).

Kullanım (proje kökünden):  python scripts/build_tokens.py
Bağımlılık yok. Çıktı yolları aşağıdaki OUTPUTS listesinde.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "design" / "tokens.json"

# Mobil projenin yolu farklıysa THEME_TS'i değiştir.
CSS_OUTPUTS = [
    ROOT / "static" / "tokens.css",
    ROOT / "react-dashboard" / "src" / "styles" / "tokens.css",
]
THEME_TS = ROOT / "design" / "build" / "theme.ts"

PX_GROUPS = {"space", "radius", "control-height"}
HEADER = "/* OTOMATİK ÜRETİLDİ — elle düzenleme. Kaynak: design/tokens.json */\n"


def load():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    data.pop("_not", None)
    return data


def lookup(data, ref):
    node = data
    for key in ref.split("."):
        node = node[key]
    return node


def resolve(data, value):
    if isinstance(value, str):
        m = re.fullmatch(r"\{(.+)\}", value)
        if m:
            return resolve(data, lookup(data, m.group(1)))
    return value


def flatten(node, prefix=()):
    for key, val in node.items():
        path = prefix + (str(key),)
        if isinstance(val, dict):
            yield from flatten(val, path)
        else:
            yield path, val


def css_value(path, val):
    group = path[0]
    if isinstance(val, (int, float)):
        if group in PX_GROUPS or path[:2] == ("font", "size") or group == "breakpoint":
            return f"{val}px"
        if group == "motion":
            return f"{val}ms"
    return str(val)


def build_css(data):
    lines = [HEADER, ":root {"]
    for path, val in flatten({k: v for k, v in data.items() if k != "semantic"}):
        lines.append(f"  --bai-{'-'.join(path)}: {css_value(path, val)};")
    lines.append("")
    lines.append("  /* Anlamsal katman: bileşenler sadece bunları kullanır */")
    for key, val in data["semantic"].items():
        ref = re.fullmatch(r"\{(.+)\}", val)
        out = f"var(--bai-{ref.group(1).replace('.', '-')})" if ref else val
        lines.append(f"  --bai-{key}: {out};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def to_camel(key):
    parts = re.split(r"[-_]", key)
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def ts_obj(node, data, indent=1):
    pad = "  " * indent
    rows = []
    for key, val in node.items():
        k = to_camel(str(key))
        k = k if re.fullmatch(r"[A-Za-z_]\w*", k) else json.dumps(str(key))
        if isinstance(val, dict):
            rows.append(f"{pad}{k}: {ts_obj(val, data, indent + 1)},")
        else:
            rows.append(f"{pad}{k}: {json.dumps(resolve(data, val), ensure_ascii=False)},")
    return "{\n" + "\n".join(rows) + "\n" + "  " * (indent - 1) + "}"


def build_ts(data):
    body = ts_obj(data, data)
    return (HEADER + "// React Native için: sayılar dp, gölgeler string olduğu için RN'de ayrıca map edilmeli.\n"
            f"export const theme = {body} as const;\n\nexport type Theme = typeof theme;\n")


def main():
    data = load()
    css = build_css(data)
    for out in CSS_OUTPUTS:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(css, encoding="utf-8")
        print("yazıldı:", out.relative_to(ROOT))
    THEME_TS.parent.mkdir(parents=True, exist_ok=True)
    THEME_TS.write_text(build_ts(data), encoding="utf-8")
    print("yazıldı:", THEME_TS.relative_to(ROOT))


if __name__ == "__main__":
    main()
