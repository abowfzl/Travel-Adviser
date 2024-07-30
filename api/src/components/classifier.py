from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import numpy as np

training_data = [
    ("من می‌خواهم به شیراز بروم. چه جاهایی را پیشنهاد می‌دهید؟", "attraction_query"),
    ("جاذبه‌های گردشگری شهر اصفهان", "attraction_query"),
    ("آب و هوای تهران چگونه است؟", "weather_query"),
    ("رستوران‌های خوب در اصفهان کجا هستند؟", "attraction_query"),
    ("امروز چندمه؟", "date_query"),
    ("بهترین هتل‌ها در مشهد کدامند؟", "attraction_query"),
    ("مسافت بین تهران و اصفهان چقدر است؟", "distance_query"),
    ("پروازهای امروز از شیراز به تهران چیست؟", "flight_query"),
    ("مکان‌های دیدنی نزدیک به من کجا هستند؟", "attraction_query"),
    ("پارک‌های معروف در تهران کدامند؟", "attraction_query"),
    ("امروز هوا چطور خواهد بود؟", "weather_query"),
    ("ساعت پرواز به دبی چه زمانی است؟", "flight_query"),
    ("جاهای تاریخی تبریز کجا هستند؟", "attraction_query"),
    ("پیش‌بینی آب و هوا برای فردا چیست؟", "weather_query"),
    ("چه موزه‌هایی در اصفهان هستند؟", "attraction_query"),
    ("مراکز خرید معروف در تهران کدامند؟", "attraction_query"),
    ("هوای اصفهان امروز چطور است؟", "weather_query"),
    ("از کجا بلیط هواپیما بخرم؟", "flight_query"),
    ("آیا امروز باران می‌بارد؟", "weather_query"),
    ("جاهای دیدنی کیش کجا هستند؟", "attraction_query"),
    ("باغ‌های معروف در شیراز کدامند؟", "attraction_query"),
    ("کدام هتل‌ها نزدیک به میدان نقش جهان هستند؟", "attraction_query"),
    ("فاصله بین تهران و شیراز چقدر است؟", "distance_query"),
    ("ساعت حرکت قطار از مشهد به تهران؟", "distance_query"),
    ("چگونه به برج میلاد برسم؟", "distance_query"),
    ("چه رستوران‌هایی در نزدیکی من هستند؟", "attraction_query"),
    ("آیا امشب هوا سرد می‌شود؟", "weather_query"),
    ("تاریخ امروز چیست؟", "date_query"),
    ("چه زمانی پرواز به پاریس است؟", "flight_query"),
    ("آیا هتل‌های خوب در کیش وجود دارند؟", "attraction_query"),
    ("چگونه بلیط قطار بخرم؟", "distance_query"),
    ("برای سفر کردن به جاهایی که گفتی یه برنامه برای دو روز آینده به من بده", "plan_trip"),
    ("برای آخر هفته چه برنامه‌ای پیشنهاد می‌دهید؟", "plan_trip"),
    ("چگونه می‌توانم یک برنامه سفر برای تعطیلات داشته باشم؟", "plan_trip"),
    ("بهترین مکان‌ها برای دیدن در دو روز چیست؟", "plan_trip"),
    ("برای یک هفته در تهران چه برنامه‌ای دارید؟", "plan_trip"),
    ("سلام", "greeting"),
    ("خداحافظ", "farewell"),
    ("متشکرم", "thanks"),
    ("مرسی", "thanks"),
    ("ببخشید", "apology"),
    ("کمک", "help"),
    ("لطفا", "request"),
    ("آیا می‌توانید کمک کنید؟", "help_request"),
    ("دیدنی‌های مشهد", "attraction_query"),
    ("جاذبه‌های توریستی تبریز", "attraction_query"),
    ("معرفی مکان‌های دیدنی اصفهان", "attraction_query"),
    ("بهترین جاذبه‌های تهران", "attraction_query"),
    ("رستوران‌های معروف تهران", "attraction_query"),
    ("جاهای توریستی شیراز", "attraction_query"),
    ("هتل‌های اصفهان", "attraction_query"),
    ("دیدنی‌های تبریز", "attraction_query"),
]

training_texts, training_labels = zip(*training_data)

pipeline = make_pipeline(TfidfVectorizer(stop_words='english'), LogisticRegression(max_iter=1000))

pipeline.fit(training_texts, training_labels)

attraction_keywords = ["جاهای دیدنی", "جاذبه‌ها", "جاذبه", "مکان‌های دیدنی", "رستوران", "بازار", "موزه", "هتل", "پارک", "باغ", "مراکز خرید"]


def is_attraction_query(user_input):
    for keyword in attraction_keywords:
        if keyword in user_input:
            return True

    proba = pipeline.predict_proba([user_input])
    intent = pipeline.predict([user_input])[0]

    threshold = 0.6
    dynamic_threshold = max(threshold, np.mean(proba[0]))

    if max(proba[0]) < dynamic_threshold:
        return False

    if intent == "attraction_query":
        return True

    return False
