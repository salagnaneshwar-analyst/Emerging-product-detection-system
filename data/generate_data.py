import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

products = [
    "Smart Ring", "AI Earbuds", "Portable Blender", "Eco Water Bottle",
    "Mini Projector", "Wireless Charger", "Smart Glasses", "Foldable Keyboard",
    "Air Purifier", "UV Sanitizer", "Sleep Tracker", "Smart Insole",
    "Portable Solar Panel", "Plant-based Protein", "Blue Light Glasses",
    "Bamboo Toothbrush", "Smart Pillowcase", "Dog GPS Tracker",
    "Noise Cancelling Earbuds", "Posture Corrector", "Smart Water Bottle",
    "Compression Socks", "AI Camera", "Mechanic Keyboard",
    "Ergonomic Chair", "Standing Desk", "LED Strip Lights",
    "Smart Plug", "Robot Vacuum", "Air Fryer"
]

categories = {
    "Smart Ring": "Wearables", "AI Earbuds": "Audio",
    "Portable Blender": "Kitchen", "Eco Water Bottle": "Lifestyle",
    "Mini Projector": "Electronics", "Wireless Charger": "Electronics",
    "Smart Glasses": "Wearables", "Foldable Keyboard": "Accessories",
    "Air Purifier": "Home", "UV Sanitizer": "Health",
    "Sleep Tracker": "Health", "Smart Insole": "Wearables",
    "Portable Solar Panel": "Green Tech", "Plant-based Protein": "Nutrition",
    "Blue Light Glasses": "Eyewear", "Bamboo Toothbrush": "Eco Living",
    "Smart Pillowcase": "Sleep Tech", "Dog GPS Tracker": "Pet Tech",
    "Noise Cancelling Earbuds": "Audio", "Posture Corrector": "Health",
    "Smart Water Bottle": "Health", "Compression Socks": "Health",
    "AI Camera": "Photography", "Mechanic Keyboard": "Accessories",
    "Ergonomic Chair": "Office", "Standing Desk": "Office",
    "LED Strip Lights": "Home", "Smart Plug": "Smart Home",
    "Robot Vacuum": "Home Automation", "Air Fryer": "Kitchen"
}

sources = ["Twitter", "Reddit", "Amazon", "Flipkart", "News", "YouTube"]

review_templates = {
    "positive": [
        "I absolutely love my new {product}! It changed my daily routine completely.",
        "Best purchase of the year the {product} is incredible value for money.",
        "{product} works flawlessly. Highly recommend to everyone!",
        "The {product} exceeded all my expectations. 5 stars!",
        "Just got the {product} and I am already obsessed. Game changer!",
        "Everyone in my office is asking about my {product}. So impressed.",
        "The {product} is worth every rupee. Quality is top notch.",
        "My {product} arrived and I am blown away. Would buy again.",
        "The {product} is trending for a reason it is brilliant!",
        "Cannot imagine my life without the {product} now. So useful.",
        "The {product} has amazing battery life and premium build quality.",
        "Gifted the {product} to my friend and they loved it too!",
        "The {product} is exactly what young professionals need today.",
        "Unboxing the {product} was such a premium experience. Love it.",
        "The {product} app is intuitive and the hardware is solid."
    ],
    "negative": [
        "Disappointed with my {product}. Stopped working after a week.",
        "The {product} is overpriced for what it offers. Not worth it.",
        "Expected more from the {product}. Build quality is poor.",
        "My {product} arrived damaged. Customer service was unhelpful.",
        "Do not waste money on the {product}. Better alternatives exist.",
        "The {product} is a gimmick. Returned it immediately.",
        "Too many bugs in the {product} app. Very frustrating experience.",
        "The {product} battery life is terrible. Very disappointed.",
        "{product} packaging was fine but product itself is mediocre.",
        "Not happy with my {product} purchase. Instructions are confusing."
    ],
    "neutral": [
        "Got the {product} last week. Still figuring out all the features.",
        "The {product} is okay. Nothing exceptional but gets the job done.",
        "Comparing the {product} with alternatives before deciding to keep it.",
        "My {product} seems fine but needs more time to evaluate.",
        "The {product} is decent. Has pros and cons. Will update later.",
        "Just unboxed the {product}. First impressions are average.",
        "The {product} trend seems interesting. Let us see if it lasts.",
        "Trying out the {product} for a month before giving full review.",
        "{product} seems to be everywhere lately. Curious to understand why.",
        "Mixed feelings about {product}. Some features are great others not."
    ]
}

emerging = [
    "Smart Ring", "AI Earbuds", "Eco Water Bottle", "Plant-based Protein",
    "Smart Glasses", "Portable Solar Panel", "Sleep Tracker", "Dog GPS Tracker",
    "Smart Water Bottle", "AI Camera"
]

rows = []
start_date = datetime(2024, 1, 1)

for i in range(620):
    product = random.choice(products)
    category = categories[product]
    source = random.choice(sources)

    if product in emerging:
        days_offset = random.randint(250, 730)
        sentiment = random.choices(
            ["positive", "negative", "neutral"], weights=[0.65, 0.15, 0.20])[0]
    else:
        days_offset = random.randint(0, 730)
        sentiment = random.choices(
            ["positive", "negative", "neutral"], weights=[0.50, 0.28, 0.22])[0]

    date = start_date + timedelta(days=days_offset)
    text = random.choice(review_templates[sentiment]).format(product=product)

    rows.append({
        "date": date.strftime("%Y-%m-%d"),
        "source": source,
        "customer_text": text,
        "platform": source,
        "product_category": category,
        "product_name": product,
        "sentiment_label": sentiment
    })

df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
df.to_csv("data/market_reviews.csv", index=False)
print(f"Dataset generated: {len(df)} rows")
print(df["product_name"].value_counts().head(10))
