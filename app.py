"""Review proposed schema changes for compatibility and migration risk."""
import argparse
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen


def load_config():
    values = {}
    path = Path(__file__).parent / 'config/development.env'
    if path.exists():
        for line in path.read_text().splitlines():
            if line and not line.startswith("#") and "=" in line:
                name, value = line.split("=", 1)
                values[name.strip()] = value.strip()
    values.update(os.environ)
    return values


def run(text):
    cfg = load_config()
    payload = {"model": cfg.get("OPENAI_MODEL", 'chat-default'),
               "messages": [{"role": "system", "content": "Perform schema change review. Return concise JSON for human review."},
                            {"role": "user", "content": text}],
               "max_tokens": 256, "temperature": 0}
    req = Request(cfg["OPENAI_BASE_URL"].rstrip("/") + "/chat/completions",
                  json.dumps(payload).encode(),
                  {"Authorization": "Bearer " + cfg["OPENAI_API_KEY"],
                   "Content-Type": "application/json"})
    with urlopen(req, timeout=30) as response:
        return json.load(response)["choices"][0]["message"]["content"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    print(run(args.input.read_text()))
