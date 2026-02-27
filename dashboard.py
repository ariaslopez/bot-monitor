from flask import Flask, render_template, jsonify
import tweepy
import os
from datetime import datetime
from dotenv import load_dotenv
import plotly.graph_objs as go
import plotly
import json

load_dotenv()

app = Flask(__name__)

BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'ADA_HBAR')

client = tweepy.Client(bearer_token=BEARER_TOKEN)


def get_bot_metrics():
    """Obtiene métricas del bot"""
    try:
        user = client.get_user(username=BOT_USERNAME)
        if not user.data:
            return None

        user_id = user.data.id
        tweets = client.get_users_tweets(
            user_id,
            max_results=10,
            tweet_fields=['public_metrics', 'created_at']
        )

        if not tweets.data:
            return None

        metrics_data = []
        for tweet in tweets.data:
            metrics = tweet.public_metrics
            metrics_data.append({
                'id': tweet.id,
                'text': tweet.text[:80] + "..." if len(tweet.text) > 80 else tweet.text,
                'created_at': tweet.created_at.strftime('%Y-%m-%d %H:%M'),
                'likes': metrics['like_count'],
                'retweets': metrics['retweet_count'],
                'replies': metrics['reply_count'],
                'views': metrics.get('impression_count', 0),
                'url': f"https://twitter.com/{BOT_USERNAME}/status/{tweet.id}"
            })

        return metrics_data
    except Exception as e:
        print(f"Error: {e}")
        return None


def create_charts(metrics_data):
    """Crea gráficas con Plotly"""
    if not metrics_data:
        return None, None, None

    metrics_data = list(reversed(metrics_data))

    tweets = [f"Tweet {i+1}" for i in range(len(metrics_data))]
    likes = [m['likes'] for m in metrics_data]
    retweets = [m['retweets'] for m in metrics_data]
    views = [m['views'] for m in metrics_data]

    engagement_chart = go.Figure()
    engagement_chart.add_trace(go.Bar(
        x=tweets, y=likes, name='Likes',
        marker_color='#1DA1F2'
    ))
    engagement_chart.add_trace(go.Bar(
        x=tweets, y=retweets, name='Retweets',
        marker_color='#17BF63'
    ))
    engagement_chart.update_layout(
        title='Engagement por Tweet',
        barmode='group',
        template='plotly_dark',
        height=400
    )

    views_chart = go.Figure()
    views_chart.add_trace(go.Scatter(
        x=tweets, y=views,
        mode='lines+markers',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=10)
    ))
    views_chart.update_layout(
        title='Views por Tweet',
        template='plotly_dark',
        height=400
    )

    total_engagement = [likes[i] + retweets[i] for i in range(len(likes))]
    total_chart = go.Figure()
    total_chart.add_trace(go.Bar(
        x=tweets, y=total_engagement,
        marker_color='#9B59B6'
    ))
    total_chart.update_layout(
        title='Engagement Total (Likes + Retweets)',
        template='plotly_dark',
        height=400
    )

    return (
        json.dumps(engagement_chart, cls=plotly.utils.PlotlyJSONEncoder),
        json.dumps(views_chart, cls=plotly.utils.PlotlyJSONEncoder),
        json.dumps(total_chart, cls=plotly.utils.PlotlyJSONEncoder)
    )


@app.route('/')
def index():
    """Página principal"""
    metrics = get_bot_metrics()
    engagement_chart, views_chart, total_chart = create_charts(metrics)

    total_likes = sum(m['likes'] for m in metrics) if metrics else 0
    total_retweets = sum(m['retweets'] for m in metrics) if metrics else 0
    total_views = sum(m['views'] for m in metrics) if metrics else 0

    return render_template('dashboard.html',
                           bot_username=BOT_USERNAME,
                           metrics=metrics,
                           engagement_chart=engagement_chart,
                           views_chart=views_chart,
                           total_chart=total_chart,
                           total_likes=total_likes,
                           total_retweets=total_retweets,
                           total_views=total_views,
                           last_update=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                           )


@app.route('/api/metrics')
def api_metrics():
    """API endpoint para actualización en tiempo real"""
    metrics = get_bot_metrics()
    return jsonify(metrics if metrics else [])


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=True)
