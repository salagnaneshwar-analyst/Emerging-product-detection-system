# 🚀 Detect Emerging Products in the Market using NLP

> **MBA Business Analytics Project | Woxsen University**
> **Subject:** Natural Language Processing | **Guide:** Dr. Shyam Krishan
> **Deadline:** 5 May 2026

---

## 📌 Problem Statement

Companies lose first-mover advantage by discovering emerging products too late. Traditional market research is slow and expensive. This project uses **NLP and AI techniques** to automatically detect products gaining market attention by analyzing customer reviews, social media, news, and e-commerce data — enabling companies to launch products early and capture market share.

---

## 🎯 Objective

Analyze unstructured customer text data from multiple digital sources to identify:

- **Emerging products** gaining rapid attention
- **Trending product categories**
- **Rising customer needs and pain points**
- **New market opportunities**
- **Sentiment signals** around products
- **Future demand forecasts** (3-month outlook)

---

## 🏗️ Project Folder Structure

```
emerging_products_nlp/
│
├── app.py                  ← Streamlit Dashboard (main UI)
├── train.py                ← Full NLP pipeline runner
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
│
├── data/
│   ├── generate_data.py           ← Synthetic dataset generator
│   ├── market_reviews.csv         ← Raw dataset (620 rows)
│   ├── market_reviews_clean.csv   ← After preprocessing
│   └── market_reviews_sentiment.csv ← After sentiment analysis
│
├── modules/
│   ├── preprocess.py       ← NLP preprocessing pipeline
│   ├── sentiment.py        ← Lexicon-based sentiment analysis
│   ├── trends.py           ← Growth scoring & forecasting
│   └── utils.py            ← Shared utilities & KPI helpers
│
└── outputs/
    ├── growth_scores.csv       ← Product growth rankings
    ├── product_sentiment.csv   ← Per-product sentiment
    ├── top_keywords.csv        ← Market keyword frequencies
    ├── pain_points.csv         ← Customer complaint detection
    └── business_insights.csv   ← Auto-generated AI insights
```

---

## ⚙️ Setup & Run Instructions

### Step 1: Clone / Download the project
```bash
cd emerging_products_nlp
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Generate the dataset
```bash
python data/generate_data.py
```

### Step 4: Run the NLP pipeline
```bash
python train.py
```

### Step 5: Launch the dashboard
```bash
streamlit run app.py
```

The dashboard opens at: **http://localhost:8501**

---

## 🔬 Methodology

### 1. Data Collection
- Simulated data from: Twitter, Reddit, Amazon, Flipkart, News, YouTube
- 620 rows with date, source, customer text, product name, category

### 2. NLP Preprocessing Pipeline
| Step | Action |
|------|--------|
| Lowercasing | Normalize case |
| Punctuation Removal | Clean symbols |
| Stopword Removal | Remove noise words |
| Lemmatization | Reduce to root form |
| Tokenization | Split into words |

### 3. Sentiment Analysis
- Lexicon-based approach (no paid API)
- Domain-enriched word lists (positive/negative/intensifiers/negators)
- Polarity score: −1.0 to +1.0

### 4. Trend & Growth Detection
- Monthly mention frequency aggregation
- Growth Score = (Recent 3 months − Prior 3 months) / Prior 3 months × 100%
- Labels: 🚀 Rapidly Emerging (>40%) | 📈 Growing (>15%) | ➡️ Stable | 📉 Declining

### 5. Forecasting
- Linear regression on monthly mention time series
- 3-month ahead prediction per product

### 6. Pain Point Detection
- Keyword matching for complaint-related terms
- Ranked by product with highest complaint density

---

## 📊 Dashboard Features

| Feature | Description |
|---------|-------------|
| **KPI Cards** | Total reviews, products, categories, positive % |
| **Growth Leaderboard** | Ranked bar chart of emerging products |
| **Mention Timeline** | Line chart of top 5 products over time |
| **Sentiment Pie** | Overall positive/negative/neutral distribution |
| **Platform Sentiment** | Grouped bar by source platform |
| **Keyword Bar Chart** | Top 20 market keywords |
| **Word Cloud** | Visual frequency map of key terms |
| **Pain Point Chart** | Products with most complaints |
| **Forecast Charts** | 3-month demand prediction per product |
| **Business Insights** | Auto-generated AI recommendations |
| **Download Buttons** | Export CSV reports |
| **File Upload** | Upload your own dataset |

---

## 💡 Sample Business Insights

- 🚀 **Smart Ring** demand surging 38% — early launch recommended
- 📈 **AI Earbuds** showing 22% steady growth — market interest building
- 🌿 **Eco Water Bottle** gaining traction among sustainability-conscious consumers
- ⚠️ **Wireless Charger** customer complaints rising around battery compatibility
- 🔮 **Plant-based Protein** forecasted to peak in Q3 2025

---

## 🚀 Deployment Guide

### Option 1: Streamlit Cloud (Recommended — Free)
1. Push project to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Click **Deploy**

### Option 2: Render (Free tier)
1. Push to GitHub
2. Create new **Web Service** on [render.com](https://render.com)
3. Build command: `pip install -r requirements.txt && python train.py`
4. Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

### Option 3: Hugging Face Spaces (Free)
1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select **Streamlit** as the SDK
3. Upload all project files
4. Add `requirements.txt` — Space auto-builds and deploys

---

## 📊 Power BI Dashboard KPIs

| KPI | DAX Measure |
|-----|-------------|
| Growth % | `DIVIDE([Recent] - [Prior], [Prior]) * 100` |
| Positive % | `DIVIDE(COUNTROWS(FILTER(..., Sentiment="positive")), Total) * 100` |
| Avg Polarity | `AVERAGE(Reviews[polarity_score])` |
| Top Emerging Product | `TOPN(1, Products, [Growth %])` |

---

## 🎓 MBA Viva Questions & Answers

**Q1: What is NLP and how is it applied here?**
A: NLP (Natural Language Processing) is the branch of AI that helps computers understand human text. Here, we apply it to customer reviews and social media text to extract sentiment, keywords, product mentions, and trends — automating what would take analysts weeks to do manually.

**Q2: What is sentiment analysis and which approach did you use?**
A: Sentiment analysis classifies text as positive, negative, or neutral. We used a **lexicon-based approach** — matching words to a curated list of positive/negative terms with intensifier and negator handling. This requires no training data or paid APIs.

**Q3: How is "emerging" defined in your project?**
A: A product is "emerging" if its mention frequency in the most recent 3 months is significantly higher than the prior 3 months. A growth score above 40% triggers the "Rapidly Emerging" label.

**Q4: What is the business value of this project?**
A: Companies can use this system to detect rising consumer demand before competitors, enabling early product development, optimized inventory, and targeted marketing — reducing time-to-market by weeks or months.

**Q5: What is the difference between lemmatization and stemming?**
A: Stemming crudely cuts word endings ("running" → "run", but "better" → "better"). Lemmatization maps words to their root dictionary form ("better" → "good", "running" → "run"). We use rule-based lemmatization for efficiency.

**Q6: How does topic modeling (LDA) work conceptually?**
A: LDA (Latent Dirichlet Allocation) assumes each document is a mix of topics, and each topic is a distribution of words. It learns these distributions to discover hidden themes — like identifying that reviews mentioning "battery, charge, portable" cluster into a "portable electronics" topic.

**Q7: What are the limitations of your approach?**
A: Our lexicon-based sentiment analysis may miss sarcasm, slang, and domain-specific language. The dataset is synthetic. Real deployment would need live API connectors and continuous model retraining.

**Q8: How would you scale this project for production?**
A: Replace synthetic data with live APIs (Twitter, Reddit, Amazon). Use Kafka or Airflow for real-time ingestion. Deploy sentiment with a BERT model. Host on cloud (AWS/GCP) with scheduled pipeline runs. Connect Power BI to the live database.

**Q9: What is a Growth Score and how is it calculated?**
A: Growth Score = (Recent 3-month mentions − Prior 3-month mentions) / Prior 3-month mentions × 100. A positive score means the product is being talked about more — a strong early signal of emerging market demand.

**Q10: How is this relevant to Customer and Market Insights?**
A: This project directly converts raw customer voice — reviews, posts, comments — into structured market intelligence. It answers: What products are customers excited about? What are their pain points? Which categories will grow next quarter? — all critical for business strategy.

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Core programming |
| Pandas / NumPy | Data manipulation |
| Streamlit | Interactive dashboard |
| Plotly | Interactive charts |
| WordCloud | Visual keyword map |
| Matplotlib | Static plotting |
| Custom NLP | Preprocessing + Sentiment |

**All free. No paid APIs. Runs 100% locally.**

---

## 👤 Author

**Nishanth** — MBA Business Analytics, Woxsen University (2027)
Skills: Python · Pandas · SQL · Power BI · NLP

---

*"The best time to detect a trend is before everyone else does."*
