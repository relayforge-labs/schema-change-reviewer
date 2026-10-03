# schema-change-reviewer

Review proposed schema changes for compatibility and migration risk.

## Run

Requires Python 3.10+.

```sh
python3 app.py examples/input.txt
```

The tool reads its development gateway settings from `config/development.env`. Override those values in your deployment environment before production use. Review generated output before applying it to another system.
