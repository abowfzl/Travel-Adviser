from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


training_data = [
    ("من می‌خواهم به شیراز بروم. چه جاهایی را پیشنهاد می‌دهید؟", "attraction_query"),
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
    ("برای یک هفته در تهران چه برنامه‌ای دارید؟", "plan_trip")
]

training_texts, training_labels = zip(*training_data)

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(training_texts)

classifier = LogisticRegression()
classifier.fit(X_train, training_labels)

attraction_keywords = ["جاهای دیدنی", "جاذبه‌ها", "جاذبه", "مکان‌های دیدنی", "رستوران", "بازار", "موزه", "هتل", "پارک", "باغ", "مراکز خرید"]


def is_attraction_query(user_input):
    X_input = vectorizer.transform([user_input])
    intent = classifier.predict(X_input)[0]

    if intent == "attraction_query":
        return True

    for keyword in attraction_keywords:
        if keyword in user_input:
            return True

    return False
