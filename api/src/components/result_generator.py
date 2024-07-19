from typing import Any, Dict, List

from langchain_core.prompts import ChatPromptTemplate

from llm.basellm import BaseLLM
from .base_component import BaseComponent

system = f"""
شما یک دستیار مشاور سفر هستید و درباره جاذبه‌های شهرها گفتگو می‌کنید. با استفاده از زبان مشاوره پاسخ دهید.
آخرین پیام شامل اطلاعات است و شما باید پاسخی قابل خواندن توسط انسان بر اساس اطلاعات داده شده تولید کنید.
پاسخ را طوری بسازید که به عنوان پاسخ به سوال به نظر برسد. اشاره نکنید که نتیجه بر اساس اطلاعات داده شده است.
هیچ اطلاعات اضافی که به صراحت در آخرین پیام ارائه نشده است را اضافه نکنید.
تکرار می‌کنم، هیچ اطلاعاتی که به صراحت داده نشده است را اضافه نکنید.
لطفاً به تمام سوالات به زبان فارسی پاسخ دهید.
"""


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

    def run(
        self,
        question: str,
        session_id: str,
        similars: List[Dict[str, Any]]
    ) -> str:

        messages = [
            ("system", "شما یک دستیار سفر آنلاین هستید که به کاربران در برنامه‌ریزی و سازماندهی سفرهایشان کمک می‌کنید. شما باید مودب، مفید و آگاه باشید."),
            ("system", system),
            ("user", "سلام! من به کمک در برنامه‌ریزی سفر نیاز دارم."),
            ("user", "می‌خواهم به یک مقصد گردشگری خوب برای تعطیلات بروم."),
            ("system", f"با استفاده از نتایج زیر به عنوان دانش خود به سوال پاسخ دهید: {similars}"),
            ("user", f"سوال: {question}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)

        output = self.llm.generate(question, session_id, prompt)
        return output

    async def run_async(
        self,
        question: str,
        session_id: str,
        similars: List[Dict[str, Any]]
    ) -> [str]:

        messages = [
            ("system", "شما یک دستیار سفر آنلاین هستید که به کاربران در برنامه‌ریزی و سازماندهی سفرهایشان کمک می‌کنید. شما باید مودب، مفید و آگاه باشید."),
            ("system", system),
            ("user", "سلام! من به کمک در برنامه‌ریزی سفر نیاز دارم."),
            ("user", "می‌خواهم به یک مقصد گردشگری خوب برای تعطیلات بروم."),
            ("system", "با استفاده از نتایج زیر به عنوان دانش خود به سوال پاسخ دهید: {similars}"),
            ("user", "سوال: {question}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)

        output = await self.llm.generate_streaming(question, session_id, similars, prompt)

        return "".join(output)
