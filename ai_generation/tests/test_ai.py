from openai import OpenAI

from resume_builder.settings import OPENAI_API_KEY


class TestAICall:
    def test_api_key_worksself(self):
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "please repeat the word 'banana'"},
            ],
        )
        assert "banana" in response.choices[0].message.content
