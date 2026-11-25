import json
import os
import shutil
from pathlib import Path

class Gatekeeper:
    BOUND = 30
    LABEL = "boss-one-word"
    ARTIFACT = ("entry.txt",)  # single shipped artifact, tuple for immutability

    def __init__(self, repo_root):
        self.root = Path(repo_root)
        self.raw = (self.root / "entry.txt").read_text(encoding="utf-8").strip()
        self.words = self.raw.split()

    def legal(self):
        return bool(self.raw) and len(self.raw) <= self.BOUND and len(self.words) == 1

    def report(self):
        return {"label": self.LABEL, "bound": self.BOUND,
                "artifact": self.ARTIFACT[0],
                "len": len(self.raw), "word": self.raw,
                "legal": self.legal()}

    def ship(self):
        if not self.legal():
            return False
        outbox = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
        outbox.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(self.root / "entry.txt", outbox / "entry.txt")
        return True

gk = Gatekeeper(Path(__file__).resolve().parent)
shipped = gk.ship()
print(json.dumps(gk.report(), ensure_ascii=False))
raise SystemExit(0 if shipped else 1)
