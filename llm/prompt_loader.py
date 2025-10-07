#!/usr/bin/env python3

import json
import os
from typing import Dict, Union


class PromptLoader:
    @staticmethod
    def _load_file(
        filename: str, folder: str, is_json: bool = False
    ) -> Union[Dict, str]:
        """Generic file loader with minimal duplication."""
        path = os.path.join(folder, filename)
        try:
            with open(path, encoding="utf-8") as f:
                if is_json:
                    return json.load(f)
                else:
                    return f.read()
        except FileNotFoundError:
            return {} if is_json else ""
        except (json.JSONDecodeError, Exception):
            return {} if is_json else ""

    @staticmethod
    def load_prompt(filename: str) -> str:
        """Loads a text file from the `llm/prompts/` folder."""
        return PromptLoader._load_file(filename, "llm/prompts", is_json=False)
