import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "stickman-video"


def test_frontmatter():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\nname: ([a-z0-9-]+)\ndescription: .+?\n---\n", text, re.S)
    assert m and m.group(1) == "stickman-video"


def test_links_exist():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for link in re.findall(r"\]\((references/[^)#]+)", text):
        assert (SKILL / link).exists(), link


def test_ten_styles():
    cat = (SKILL / "references" / "style-catalog.md").read_text(encoding="utf-8")
    ids = re.findall(r"^## (S\d+) ·", cat, re.M)
    assert ids == [f"S{i}" for i in range(1, 11)]
    for sec in re.split(r"^## S\d+ ·", cat, flags=re.M)[1:]:
        for key in ("Style anchor", "Character anchor", "Palette", "Negatives"):
            assert key in sec


def test_make_srt():
    with tempfile.TemporaryDirectory() as d:
        src = pathlib.Path(d, "n.txt")
        src.write_text("你知道吗？蚂蚁从来不睡觉。\n5|但它们会打盹，一天上百次。\n", encoding="utf-8")
        out = pathlib.Path(d, "s.srt")
        subprocess.run([sys.executable, str(SKILL / "scripts" / "make_srt.py"), str(src), "-o", str(out)], check=True)
        srt = out.read_text(encoding="utf-8")
        assert "00:00:00,000 -->" in srt and "--> 00:00:13,000" in srt


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok", name)
