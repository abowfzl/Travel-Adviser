from typing import Any, Dict, List
import json

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

from llm.basellm import BaseLLM
from llm.OpenAI import ChatOpenAIChat
from llm.GPT4ALL import Gpt4AllChat
from .base_component import BaseComponent


def remove_large_lists(d: Dict[str, Any]) -> Dict[str, Any]:
    """
    The idea is to remove all properties that have large lists (embeddings) or text as values
    """
    LIST_CUTOFF = 56
    CHARACTER_CUTOFF = 5000
    # iterate over all key-value pairs in the dictionary
    for key, value in d.items():
        # if the value is a list and has more than list cutoff elements
        if isinstance(value, list) and len(value) > LIST_CUTOFF:
            d[key] = None
        # if the value is a string and has more than list cutoff elements
        if isinstance(value, str) and len(value) > CHARACTER_CUTOFF:
            d[key] = d[key][:CHARACTER_CUTOFF]
        # if the value is a dictionary
        elif isinstance(value, dict):
            # recurse into the nested dictionary
            remove_large_lists(d[key])
    return d


class ResultGenerator(BaseComponent):
    llm: BaseLLM
    exclude_embeddings: bool

    def __init__(self, llm: BaseLLM, exclude_embeddings: bool = True) -> None:
        self.llm = llm
        self.exclude_embeddings = exclude_embeddings

    def format_similars(self, similars):
        formatted_similars = ''
        if isinstance(self.llm, Gpt4AllChat):
            # Format the attractions data to include in the prompt
            formatted_similars = "\n".join([f"{sim['name']}: {sim['text']}" for sim in similars])
            return formatted_similars
        elif isinstance(self.llm, ChatOpenAIChat):
            formatted_similars = json.dumps(similars, ensure_ascii=False)

        return formatted_similars

    def generate_prompt(self):
        prompt = None
        if isinstance(self.llm, ChatOpenAIChat):
            messages = [
                ("system", """
                شما به عنوان یک مشاور سفر هوشمند عمل می‌کنید که به کاربران کمک می‌کند تا برنامه‌های سفر خود را به بهترین شکل ممکن تنظیم کنند. کاربران ممکن است سوالاتی درباره جاهای دیدنی، برنامه‌ریزی سفر، پیشنهادات گردشگری و تفریحات محلی داشته باشند. لطفاً با توجه به مقصد و مدت زمان سفر کاربر، یک جدول زمان‌بندی دقیق برای برنامه سفر تهیه کنید که شامل زمان و مکان بازدید باشد.

مثال:
کاربر قصد دارد به مدت ۳ روز به شیراز سفر کند و علاقه‌مند به بازدید از مکان‌های تاریخی، باغ‌ها و رستوران‌های محلی است.

### برنامه سفر به شیراز
| روز | ساعت | مقصد/فعالیت | توضیحات |
| --- | ----- | ------------ | ------- |
| روز اول | 9:00 - 11:00 | بازدید از تخت جمشید | مکان تاریخی و باستانی |
| روز اول | 11:30 - 13:00 | باغ ارم | بازدید از باغ تاریخی |
| روز اول | 13:00 - 14:00 | ناهار در رستوران سنتی | تجربه غذای محلی |
| روز اول | 14:30 - 17:00 | بازار وکیل | خرید و گشت و گذار |
| روز دوم | 9:00 - 11:00 | آرامگاه حافظ | بازدید از آرامگاه شاعر معروف |
| روز دوم | 11:30 - 13:00 | باغ جهان نما | بازدید از باغ تاریخی |
| روز دوم | 13:00 - 14:00 | ناهار در کافه رستوران سنتی | تجربه غذای محلی |
| روز دوم | 14:30 - 17:00 | مسجد نصیرالملک | بازدید از مسجد تاریخی و زیبا |
| روز سوم | 9:00 - 11:00 | باغ دلگشا | بازدید از باغ تاریخی |
| روز سوم | 11:30 - 13:00 | ارگ کریم خان | بازدید از ارگ تاریخی |
| روز سوم | 13:00 - 14:00 | ناهار در رستوران سنتی | تجربه غذای محلی |
| روز سوم | 14:30 - 17:00 | خرید سوغات | گشت و گذار و خرید سوغات |

لطفاً یک جدول مشابه برای برنامه سفر کاربر تهیه کنید.

                """),
                ("system", "با استفاده از نتایج زیر به عنوان دانش خود به سوال پاسخ دهید: {similars}"),
                ("user", "سوال: {question}")
            ]
            prompt = ChatPromptTemplate.from_messages(messages)

        elif isinstance(self.llm, Gpt4AllChat):
            template = """
                        پیام سیستم:
            شما یک دستیار مشاور سفر هستید و درباره جاذبه‌های شهرها، در برنامه‌ریزی و سازماندهی سفرهایشان وهمچنین راهنمایی درباره انتخاب یک مقصد گردشگری مناسب برای کاربران گفتگو می‌کنید. با استفاده از زبان مشاوره پاسخ دهید.            
                        به سوال به زبان فارسی پاسخ بدهید و به هیچ وجه از کلمات و حروف انگلیسی استفاده نکنید.
                        سوال کاربر:
                        {question}
                    جاذبه های زیر در شهر وجود دارند:    
                        {similars}
                        تاریخجه پیام ها با این کاربر:
                        {chat_history}
                        """

            prompt = PromptTemplate.from_template(template)

        return prompt

    def run(
        self,
        question: str,
        session_id: str,
        similars: List[Dict[str, Any]]
    ) -> str:
        pass

    async def run_async(
        self,
        question: str,
        session_id: str,
        similars: List[Dict[str, Any]]
    ) -> [str]:

        formatted_similars = self.format_similars(similars)

        prompt = self.generate_prompt()

        output = await self.llm.generate_streaming(question, session_id, formatted_similars, prompt)

        return "".join(output)
