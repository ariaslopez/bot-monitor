import tweepy
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'CryptoIntelHub')  # Tu bot

# Cliente de Twitter
client = tweepy.Client(bearer_token=BEARER_TOKEN)


def get_bot_tweets():
    """Obtiene los últimos tweets del bot"""
    try:
        # Obtener user ID del bot
        user = client.get_user(username=BOT_USERNAME)
        if not user.data:
            print(f"❌ No se encontró el usuario @{BOT_USERNAME}")
            return None

        user_id = user.data.id

        # Obtener últimos 10 tweets
        tweets = client.get_users_tweets(
            user_id,
            max_results=10,
            tweet_fields=['public_metrics', 'created_at']
        )

        return tweets.data if tweets.data else []
    except Exception as e:
        print(f"❌ Error obteniendo tweets: {e}")
        return None


def display_metrics(tweets):
    """Muestra las métricas de los tweets"""
    if not tweets:
        print("📭 No hay tweets para mostrar")
        return

    print(f"\n📊 ÚLTIMOS {len(tweets)} TWEETS DE @{BOT_USERNAME}")
    print("=" * 80)

    for i, tweet in enumerate(tweets, 1):
        metrics = tweet.public_metrics
        created = tweet.created_at.strftime('%Y-%m-%d %H:%M')
        text = tweet.text[:60] + "..." if len(tweet.text) > 60 else tweet.text

        print(f"\n{i}. {text}")
        print(f"   📅 {created}")
        print(f"   ❤️  Likes: {metrics['like_count']:,} | "
              f"🔁 Retweets: {metrics['retweet_count']:,} | "
              f"💬 Replies: {metrics['reply_count']:,} | "
              f"👁️  Views: {metrics.get('impression_count', 'N/A')}")
        print(f"   🔗 https://twitter.com/{BOT_USERNAME}/status/{tweet.id}")


def main():
    """Función principal del monitor"""
    print("🚀 MONITOR DE BOT INICIADO")
    print(f"🤖 Monitoreando: @{BOT_USERNAME}")
    print(f"🔄 Actualizando cada 5 minutos")
    print("=" * 80)

    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n⏰ Actualización: {timestamp}")

        tweets = get_bot_tweets()
        display_metrics(tweets)

        print(f"\n⏳ Próxima actualización en 5 minutos...")
        print("=" * 80)

        time.sleep(300)  # 5 minutos


if __name__ == "__main__":
    main()
