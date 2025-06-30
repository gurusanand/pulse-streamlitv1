import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="News Intelligence",
    page_icon="📰",
    layout="wide"
)

st.title("📰 News Intelligence")
st.markdown("AI-curated market insights and sentiment analysis")

# Generate sample news data
@st.cache_data
def generate_news_data():
    categories = ['Banking', 'Technology', 'Healthcare', 'Manufacturing', 'Energy', 'Retail']
    sources = ['Financial Times', 'Reuters', 'Bloomberg', 'Wall Street Journal', 'BBC Business', 'CNBC']
    sentiments = ['Positive', 'Negative', 'Neutral']
    
    news_items = []
    for i in range(100):
        news_item = {
            'id': f'NEWS-{1000 + i}',
            'headline': generate_headline(i),
            'category': random.choice(categories),
            'source': random.choice(sources),
            'sentiment': random.choice(sentiments),
            'sentiment_score': random.uniform(-1, 1),
            'relevance_score': random.uniform(0.3, 1.0),
            'published_date': datetime.now() - timedelta(hours=random.randint(1, 168)),
            'impact_level': random.choice(['High', 'Medium', 'Low']),
            'client_mentions': random.randint(0, 5),
            'summary': generate_summary(i),
            'tags': random.sample(['M&A', 'IPO', 'Earnings', 'Regulation', 'Innovation', 'ESG'], random.randint(1, 3))
        }
        news_items.append(news_item)
    
    return pd.DataFrame(news_items)

def generate_headline(i):
    headlines = [
        "Technology Sector Shows Strong Q2 Performance Amid Market Volatility",
        "Central Bank Signals Potential Interest Rate Adjustments",
        "Healthcare Innovation Drives Record Investment Levels",
        "Manufacturing Industry Faces Supply Chain Challenges",
        "ESG Financing Reaches New Heights in Corporate Banking",
        "Digital Banking Transformation Accelerates Post-Pandemic",
        "Energy Sector Transitions Toward Renewable Solutions",
        "Retail Banking Embraces AI for Customer Experience",
        "Regulatory Changes Impact Commercial Lending Practices",
        "Fintech Partnerships Reshape Traditional Banking Models"
    ]
    return headlines[i % len(headlines)] + f" - Update {i//10 + 1}"

def generate_summary(i):
    summaries = [
        "Market analysis reveals significant growth opportunities in the technology sector, with increased demand for digital solutions driving revenue growth across multiple subsectors.",
        "Economic indicators suggest potential monetary policy adjustments, which could impact lending rates and credit availability for commercial clients.",
        "Healthcare sector demonstrates resilience with strong fundamentals, presenting attractive lending opportunities for banks focused on this vertical.",
        "Supply chain disruptions continue to challenge manufacturing companies, requiring flexible financing solutions and risk management approaches.",
        "Environmental, Social, and Governance (ESG) criteria increasingly influence corporate financing decisions, creating new market opportunities.",
        "Digital transformation initiatives accelerate across industries, driving demand for technology financing and innovation funding.",
        "Renewable energy investments surge as companies commit to sustainability goals, opening new financing markets for forward-thinking banks.",
        "Artificial intelligence adoption in banking operations improves efficiency and customer experience while reducing operational costs.",
        "New regulatory frameworks require banks to adapt compliance procedures and risk management practices for commercial lending.",
        "Strategic partnerships between traditional banks and fintech companies create innovative solutions for business banking clients."
    ]
    return summaries[i % len(summaries)]

news_df = generate_news_data()

# News overview metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_articles = len(news_df)
    st.metric(
        label="📰 Total Articles",
        value=total_articles,
        delta="+12 today"
    )

with col2:
    avg_sentiment = news_df['sentiment_score'].mean()
    sentiment_label = "Positive" if avg_sentiment > 0.1 else "Negative" if avg_sentiment < -0.1 else "Neutral"
    st.metric(
        label="📊 Market Sentiment",
        value=sentiment_label,
        delta=f"{avg_sentiment:.2f}"
    )

with col3:
    high_impact_count = len(news_df[news_df['impact_level'] == 'High'])
    st.metric(
        label="⚠️ High Impact News",
        value=high_impact_count,
        delta="+3"
    )

with col4:
    client_mentions = news_df['client_mentions'].sum()
    st.metric(
        label="👥 Client Mentions",
        value=client_mentions,
        delta="+8"
    )

# News filters and search
st.subheader("🔍 News Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    category_filter = st.multiselect(
        "Category",
        options=news_df['category'].unique(),
        default=news_df['category'].unique()
    )

with col2:
    sentiment_filter = st.multiselect(
        "Sentiment",
        options=news_df['sentiment'].unique(),
        default=news_df['sentiment'].unique()
    )

with col3:
    impact_filter = st.multiselect(
        "Impact Level",
        options=news_df['impact_level'].unique(),
        default=news_df['impact_level'].unique()
    )

with col4:
    time_filter = st.selectbox(
        "Time Range",
        options=["Last 24 hours", "Last 3 days", "Last week", "Last month"],
        index=2
    )

# Search functionality
search_query = st.text_input("🔍 Search news articles...", placeholder="Enter keywords, company names, or topics")

# Apply filters
filtered_df = news_df[
    (news_df['category'].isin(category_filter)) &
    (news_df['sentiment'].isin(sentiment_filter)) &
    (news_df['impact_level'].isin(impact_filter))
]

# Apply time filter
time_mapping = {
    "Last 24 hours": 1,
    "Last 3 days": 3,
    "Last week": 7,
    "Last month": 30
}
time_threshold = datetime.now() - timedelta(days=time_mapping[time_filter])
filtered_df = filtered_df[filtered_df['published_date'] >= time_threshold]

# Apply search filter
if search_query:
    search_mask = (
        filtered_df['headline'].str.contains(search_query, case=False, na=False) |
        filtered_df['summary'].str.contains(search_query, case=False, na=False)
    )
    filtered_df = filtered_df[search_mask]

# News analytics
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Sentiment Analysis")
    
    # Sentiment distribution
    sentiment_counts = filtered_df['sentiment'].value_counts()
    
    fig_sentiment = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title="News Sentiment Distribution",
        color_discrete_map={
            'Positive': '#28a745',
            'Negative': '#dc3545',
            'Neutral': '#6c757d'
        }
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)

with col2:
    st.subheader("📈 Sentiment Trends")
    
    # Sentiment over time
    filtered_df['date'] = filtered_df['published_date'].dt.date
    daily_sentiment = filtered_df.groupby('date')['sentiment_score'].mean().reset_index()
    
    fig_trend = px.line(
        daily_sentiment,
        x='date',
        y='sentiment_score',
        title="Daily Sentiment Trend"
    )
    fig_trend.add_hline(y=0, line_dash="dash", line_color="gray")
    st.plotly_chart(fig_trend, use_container_width=True)

# Category analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏷️ News by Category")
    
    category_counts = filtered_df['category'].value_counts()
    
    fig_category = px.bar(
        x=category_counts.values,
        y=category_counts.index,
        orientation='h',
        title="Article Count by Category"
    )
    st.plotly_chart(fig_category, use_container_width=True)

with col2:
    st.subheader("📊 Impact Analysis")
    
    impact_sentiment = filtered_df.groupby(['impact_level', 'sentiment']).size().reset_index(name='count')
    
    fig_impact = px.bar(
        impact_sentiment,
        x='impact_level',
        y='count',
        color='sentiment',
        title="Impact Level vs Sentiment",
        color_discrete_map={
            'Positive': '#28a745',
            'Negative': '#dc3545',
            'Neutral': '#6c757d'
        }
    )
    st.plotly_chart(fig_impact, use_container_width=True)

# News feed
st.subheader("📰 News Feed")

# Sort options
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"**Showing {len(filtered_df)} articles**")

with col2:
    sort_option = st.selectbox(
        "Sort by",
        options=["Relevance", "Date", "Sentiment", "Impact"],
        index=0
    )

# Sort the dataframe
if sort_option == "Relevance":
    filtered_df = filtered_df.sort_values('relevance_score', ascending=False)
elif sort_option == "Date":
    filtered_df = filtered_df.sort_values('published_date', ascending=False)
elif sort_option == "Sentiment":
    filtered_df = filtered_df.sort_values('sentiment_score', ascending=False)
elif sort_option == "Impact":
    impact_order = {'High': 3, 'Medium': 2, 'Low': 1}
    filtered_df['impact_numeric'] = filtered_df['impact_level'].map(impact_order)
    filtered_df = filtered_df.sort_values('impact_numeric', ascending=False)

# Display news articles
for idx, article in filtered_df.head(20).iterrows():
    with st.container():
        # Article header
        col1, col2, col3 = st.columns([6, 2, 2])
        
        with col1:
            # Sentiment color coding
            sentiment_color = {
                'Positive': '#28a745',
                'Negative': '#dc3545',
                'Neutral': '#6c757d'
            }
            
            st.markdown(f"""
            <div style="border-left: 4px solid {sentiment_color[article['sentiment']]}; padding-left: 10px;">
                <h4 style="margin: 0; color: #333;">{article['headline']}</h4>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            impact_color = {'High': '#dc3545', 'Medium': '#ffc107', 'Low': '#28a745'}
            st.markdown(f"""
            <span style="background-color: {impact_color[article['impact_level']]}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;">
                {article['impact_level']} Impact
            </span>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"**{article['source']}**")
        
        # Article details
        col1, col2, col3, col4 = st.columns([3, 2, 2, 3])
        
        with col1:
            st.markdown(f"📅 {article['published_date'].strftime('%Y-%m-%d %H:%M')}")
        
        with col2:
            st.markdown(f"🏷️ {article['category']}")
        
        with col3:
            sentiment_emoji = {'Positive': '😊', 'Negative': '😟', 'Neutral': '😐'}
            st.markdown(f"{sentiment_emoji[article['sentiment']]} {article['sentiment']}")
        
        with col4:
            if article['client_mentions'] > 0:
                st.markdown(f"👥 {article['client_mentions']} client mentions")
        
        # Article summary
        st.markdown(f"**Summary:** {article['summary']}")
        
        # Tags
        if article['tags']:
            tag_html = " ".join([f"<span style='background-color: #e9ecef; padding: 2px 6px; border-radius: 8px; font-size: 0.8em; margin-right: 5px;'>{tag}</span>" for tag in article['tags']])
            st.markdown(f"**Tags:** {tag_html}", unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📖 Read Full", key=f"read_{article['id']}"):
                st.info("Opening full article...")
        
        with col2:
            if st.button("📧 Share", key=f"share_{article['id']}"):
                st.success("Article shared!")
        
        with col3:
            if st.button("🔖 Save", key=f"save_{article['id']}"):
                st.success("Article saved!")
        
        with col4:
            if st.button("🚨 Alert", key=f"alert_{article['id']}"):
                st.info("Alert created for similar news")
        
        st.markdown("---")

# AI Insights sidebar
with st.sidebar:
    st.subheader("🧠 AI News Insights")
    
    # Key insights
    insights = [
        {
            "type": "trend",
            "title": "Emerging Trend",
            "content": "ESG financing mentions increased 45% this week",
            "icon": "📈"
        },
        {
            "type": "risk",
            "title": "Risk Alert",
            "content": "Manufacturing sector showing negative sentiment trend",
            "icon": "⚠️"
        },
        {
            "type": "opportunity",
            "title": "Opportunity",
            "content": "Healthcare sector positive coverage suggests growth potential",
            "icon": "🎯"
        },
        {
            "type": "client",
            "title": "Client Impact",
            "content": "3 portfolio clients mentioned in recent regulatory news",
            "icon": "👥"
        }
    ]
    
    for insight in insights:
        st.markdown(f"""
        <div style="border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 8px; background: grey">
            <div style="font-weight: bold;">{insight['icon']} {insight['title']}</div>
            <div style="font-size: 0.9em; margin-top: 5px;">{insight['content']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # News alerts setup
    st.subheader("🔔 News Alerts")
    
    alert_keywords = st.text_input("Keywords", placeholder="e.g., regulation, fintech")
    alert_categories = st.multiselect("Categories", options=news_df['category'].unique())
    alert_sentiment = st.selectbox("Sentiment", options=["Any", "Positive", "Negative", "Neutral"])
    
    if st.button("🔔 Create Alert"):
        st.success("News alert created successfully!")
    
    # Saved articles
    st.subheader("🔖 Saved Articles")
    
    saved_articles = [
        "Central Bank Policy Update",
        "Technology Sector Analysis",
        "ESG Financing Trends"
    ]
    
    for article in saved_articles:
        if st.button(f"📖 {article}", key=f"saved_{article}"):
            st.info(f"Opening {article}...")

# Market intelligence summary
st.subheader("📊 Market Intelligence Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🏆 Top Performing Sectors**")
    top_sectors = filtered_df[filtered_df['sentiment'] == 'Positive']['category'].value_counts().head(3)
    for i, (sector, count) in enumerate(top_sectors.items(), 1):
        st.markdown(f"{i}. **{sector}** ({count} positive articles)")

with col2:
    st.markdown("**⚠️ Sectors Under Pressure**")
    pressure_sectors = filtered_df[filtered_df['sentiment'] == 'Negative']['category'].value_counts().head(3)
    for i, (sector, count) in enumerate(pressure_sectors.items(), 1):
        st.markdown(f"{i}. **{sector}** ({count} negative articles)")

with col3:
    st.markdown("**🔥 Trending Topics**")
    all_tags = []
    for tags in filtered_df['tags']:
        all_tags.extend(tags)
    
    from collections import Counter
    trending_tags = Counter(all_tags).most_common(3)
    for i, (tag, count) in enumerate(trending_tags, 1):
        st.markdown(f"{i}. **{tag}** ({count} mentions)")

# Export functionality
st.subheader("📤 Export Options")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Export Analytics Report"):
        st.success("Analytics report exported to PDF!")

with col2:
    if st.button("📰 Export News Summary"):
        st.success("News summary exported to Excel!")

with col3:
    if st.button("📧 Email Daily Digest"):
        st.success("Daily digest sent to your email!")

