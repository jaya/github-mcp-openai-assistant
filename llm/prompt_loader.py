import json
import os


class PromptLoader:
    @staticmethod
    def _load_file(filename: str, folder: str, is_json: bool = False) -> dict | str:
        path = os.path.join(folder, filename)
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f) if is_json else f.read()
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if is_json else ""

    @staticmethod
    def load_prompt(filename: str) -> str:
        return PromptLoader._load_file(filename, "llm/prompts", is_json=False)
