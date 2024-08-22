from typing import Any, Dict, List
import json

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder

from llm.basellm import BaseLLM
from llm.OpenAI import ChatOpenAIChat
from llm.GPT4ALL import Gpt4AllChat
from .base_component import BaseComponent


def apply_limitations(item):
    if 'n.texts' in item:
        num_texts = len(item['n.texts'])
        # Parameters
        base_cutoff = 200  # Maximum characters when there is only one text
        min_cutoff = 50  # Minimum characters allowed
        reduction_factor = 10  # The reduction in character cutoff per additional text

        # Calculate the character_cutoff dynamically
        character_cutoff = max(min_cutoff, base_cutoff - num_texts * reduction_factor)

        limited_texts = []
        for text in item['n.texts']:
            if len(text) > character_cutoff:
                limited_texts.append(text[:character_cutoff] + '...')
            else:
                limited_texts.append(text)
        item['n.texts'] = limited_texts

    return item


def process_large_object(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Processes a list of dictionaries by removing large lists and truncating long strings.
    """
    return [apply_limitations(item) for item in data]


def format_similars(similars):
    similars = process_large_object(similars)

    formatted_similars = ''
    counter = 1

    for place in similars:
        name = place.get('n.name', 'مکان نامشخص')
        city = place.get('n.city_name', 'شهر نامشخص')
        description = " ".join(place.get('n.texts', ['توضیحاتی در دسترس نیست']))
        location_url = place.get('n.location', 'موقعیت مکانی در دسترس نیست')
        more_info_url = place.get('n.url', 'اطلاعات بیشتری در دسترس نیست')

        formatted_similars += f"{counter}. **{name}** - **{city}**:\n"
        formatted_similars += f"   - **توضیحات**: {description}... [اطلاعات بیشتر]({more_info_url})\n"
        formatted_similars += f"   - **موقعیت مکانی**: [مشاهده روی نقشه]({location_url})\n\n"

        counter += 1

    return formatted_similars


class ResultGenerator(BaseComponent):
    llm: BaseLLM
    exclude_embeddings: bool

    def __init__(self, llm: BaseLLM, exclude_embeddings: bool = True) -> None:
        self.llm = llm
        self.exclude_embeddings = exclude_embeddings

    def generate_prompt(self):
        prompt = None
        if isinstance(self.llm, ChatOpenAIChat):
            messages = [
                ("system", """
                    شما به عنوان یک مشاور سفر هوشمند عمل می‌کنید که به کاربران کمک می‌کند تا برنامه‌های سفر خود را به بهترین شکل ممکن تنظیم کنند. با استفاده از زبان مشاوره به زبان دوستانه پاسخ دهید و کاربر را با پاسخ زیبا جذب کنید.
                    کاربران ممکن است سوالاتی درباره جاهای دیدنی، برنامه‌ریزی سفر، پیشنهادات گردشگری و تفریحات محلی داشته باشند. لطفاً با توجه به مقصد و مدت زمان سفر، یک جدول زمان‌بندی دقیق برای برنامه سفر تهیه کنید که شامل زمان، روز، نوع فعالیت و مکان بازدید و زمان تقریبی  مورد نیاز باشد.
                    سعی کنید تا جای ممکن از کاربر برای مشخص کردن شهر و مقصد دقیق سوال بپرسید.این سوالات باید به گونه ای باشد تا سفر دلخواه کاربر با سلایق و نوع تفریحات مورد نظر هم خوانی داشته باشد. در صورت نیاز مقصد هایی پیشنهاد دهید و به کاربر کمک کنید تا مقصد رو انتخاب کند.
                     """
                 ),
                ("system",
                 "باید تعداد روز های مورد نظر کاربر مشخص شود. یعنی کاربر میخواد چند روز و چند شب در مقصد مورد نظر بماند."),
                ("system",
                 "از دادن برنامه سریع خودداری کنید. باید سوالات کافی بپرسید و تشخیص دهید که هدف کاربر از سفرش چیست. برای مثال وقتی هدف سفر کاری باشد خیلی مکان هایی که از مرکز شهر دور هستند مورد پستد کاربر نیست ولی وقتی هدف سفر توریستی و تفریحی باشد باید در برنامه جاهای دیدنی و تاریخی و معروف مقصد گنجانده شود."),
                ("system", """
                     به جواب های کلی مانند سفر به شمال، ترکیه، جنوب، فرانسه و ... پاسخ ندهید و باید در مورد علایق و فضای مورد نظر کاربر سوال بپرسید و مکان هایی را پیشنهاد دهید و در مورد آن ها توضبح دهید تا کاربر را راهنمایی کنید که مقصد مورد نظرش را انتخاب کند.
                     نکته دیگر در برنامه سفر تنوع است. باید برنامه متنوع باشد تا کاربر از سفر خود لذت ببرد. از تفریحات موجود در آن شهر استان مثلا پارک آبی، استخر، دریا، جنگل، شهرگردی، پیاده روی، ورزش و ... را در نظر بگیرید. البته در نظر بگیرید برنامه باید کارآمد و قابل اجرا باشد و خیلی اغراق آمیز و رویایی نیاشد.
                    این توضیحات و نکات بسیار مهم است پس آن ها را به دقت اجرا کن.
                     """
                 ),
                ("system",
                 "برنامه های سفری که به کاربران میدهید نباید از یک الگو ثابت پیروی کند و میبایست در زمان شروع و پایان روزهای مختلف بر اساس برنامه های مورد نظر و مقصد داده شده متفاوت باشد"
                 ),
                ("system", """"شما باید فقط بر اساس اطلاعات زیر، برنامه سفر خود را تنظیم کنید. اگر داده زیر خالی بود از دادن برنامه به کاربر خودداری کنید به جای آن در مورد سفر سوال بپرسید تا داده زیر به شما داده شود و سپس برنامه سفر را تولید کنید. از لینک‌ها و موقعیت‌های مکانی که در داده‌ها آمده است، برای ارائه راهنمایی دقیق به کاربر استفاده کنید. این اطلاعات شامل نام مکان‌ها، توصیفات آن‌ها، و همچنین لینک‌های دسترسی به موقعیت مکانی دقیق در نقشه‌های آنلاین است. شما باید با استفاده از این داده‌ها، برای کامل کردن جدول و تکمیل اطلاعات و لینک های لازم برای سفر استفاده کنید: 
                            {similars}
                            """
                 ),
                ("system",
                 "برای هر جاذبه لینک برای اطلاعات بیشتر و موقعیت مکانی داده شده است. از لینک های اطلاعات بیشتر در دانش برای دادن ارجاع دادن کاربر برای کسب اطلاعات بیشتر و همچنین در ستون لینک از موقعیت مکانی های داده شده حتما حتما استفاده کنید"),
                ("system",
                 "تا جای ممکن از ذکر رستوران محلی خودداری کنید، سعی کنید اسم رستوران و همچنین یا حداقل نام غذای معروف مقصد را ذکر کنید."),
                ("system", """
                    نکته مهم دیگر در برنامه ریزی این است که زمان تقریبی است و کاریر را توجیح کنید و نیز باید مسافت نقاط پیشنهادی ملاحظه شود و یک زمانی برای رسیدن کاربر به مقصد و جا به جایی او و همچنین زمانی برای استراحت او در نظر بگیرید.
                    قبل از برنامه ریزی سفر خود زمان مناسب سفر و توضیحات مربوط به شلوغی مقصد و پیشنهادی برای حمل و نقل به کاربر بدهید.
                    """
                 ),

                ("system", """
                    مثال سفر پیشنهادی:
تشخیص داده شده است که کاربر قصد دارد به مدت 1 روز به یک سفر تفریحی به اصفهان برود و علاقه‌مند به بازدید از مکان‌های تاریخی، بازار و رستوران‌های محلی است.

### برنامه سفر تفریحی دو روزه به اصفهان

| **روز** | **زمان**         | **فعالیت**                           | **توضیحات**                                                                                                                                              | **زمان تقریبی رسیدن** | **لینک**                                                                                                                                                                          |
|:-------:|:----------------:|:------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------:|:-----------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| روز اول | 08:00 - 09:00    | صبحانه در هتل                        | شروع روز با صبحانه‌ای مفصل در هتل                                                                                                                        | -                       | -                                                                                                                                                                                |
|         | 09:15 - 11:45    | بازدید از میدان نقش جهان            | گردش در میدان تاریخی نقش جهان، خرید از بازار سنتی و بازدید از مسجد جامع عباسی. برای اطلاعات بیشتر می‌توانید به [لینک میدان نقش جهان](https://www.kojaro.com/attraction/7611-%D9%85%DB%8C%D8%AF%D8%A7%D9%86-%D9%86%D9%82%D8%B4-%D8%AC%D9%87%D8%A7%D9%86/) مراجعه کنید. | 15 دقیقه                | [مشاهده موقعیت مکانی](https://www.google.com/maps/dir/?api=1&destination=32.6573066756645,51.6775189340115)                                                                        |
|         | 12:00 - 13:30    | ناهار در رستوران شاندیز              | لذت بردن از غذاهای محلی اصفهان در رستوران معروف                                                                                                          | 10 دقیقه                | -                                                                                                                                                                                |
|         | 13:45 - 15:15    | بازدید از مسجد شیخ لطف الله          | دیدن معماری فوق‌العاده مسجد شیخ لطف الله. برای اطلاعات بیشتر می‌توانید به [لینک مسجد شیخ لطف الله](https://www.kojaro.com/attraction/7425-%D9%85%D8%B3%D8%AC%D8%AF-%D9%84%D8%B7%D9%81-%D8%A7%D9%84%D9%84%D9%87/) مراجعه کنید.                                           | 5 دقیقه                 | [مشاهده موقعیت مکانی](https://www.google.com/maps/dir/?api=1&destination=32.6573942,51.6787139)                                                                                    |
|         | 15:30 - 16:45    | استراحت در کافه                      | نوشیدن چای و استراحت در کافه‌ای دنج نزدیک میدان نقش جهان                                                                                                  | 10 دقیقه                | -                                                                                                                                                                                |
|         | 17:00 - 18:30    | گشت و گذار در بازار قیصریه           | خرید صنایع دستی و سوغاتی از بازار قیصریه                                                                                                                | 5 دقیقه                 | [مشاهده موقعیت مکانی](https://www.google.com/maps/dir/?api=1&destination=32.6573066756645,51.6775189340115)                                                                        |
|         | 19:00 - 20:30    | شام در هتل عباسی                     | تجربه صرف شام در هتل تاریخی عباسی                                                                                                                        | 20 دقیقه                | -                                                                                                                                                                                |

                    لطفاً یک جدول مشابه برای برنامه سفر کاربر تهیه کنید و حتما از لینک ها و موقعیت مکانی ها داده شده در دانش استفاده کنید. و از دانش خود برای تولید لینک ها استفاده نکنید.
                    """
                 ),
                MessagesPlaceholder(variable_name="chat_history"),
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

        formatted_similars = format_similars(similars)

        prompt = self.generate_prompt()

        output = await self.llm.generate_streaming(question, session_id, formatted_similars, prompt)

        return "".join(output)
