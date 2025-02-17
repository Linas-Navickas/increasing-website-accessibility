import json
import re


class LLM_Client:
    def __init__(self, model):
        self.model = model

    def clean_json_string(self, json_string):
        pattern_opening = r"^(?:```json|json)\s*"
        pattern_closing = r"\s*```$"
        cleaned_string = re.sub(
            pattern_opening, "", json_string, flags=re.DOTALL | re.MULTILINE
        )
        cleaned_string = re.sub(
            pattern_closing, "", cleaned_string, flags=re.DOTALL | re.MULTILINE
        )
        return cleaned_string.strip()

    def clean_text_list(self, text, prompt):
        try:
            text_list = json.loads(text)
        except Exception:
            llm_response = self.model.generate_content(prompt)
            cleaned_text = self.clean_json_string(llm_response.text)
            text_list = json.loads(cleaned_text)
        return text_list