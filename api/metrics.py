"""
Metrics Collector

Recopila y procesa métricas de bots.
"""

import yaml
from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Recolector de métricas de bots.
    """
    
    def __init__(self, twitter_client):
        """
        Inicializa el collector.
        
        Args:
            twitter_client: Instancia de TwitterClient
        """
        self.twitter_client = twitter_client
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """
        Carga configuración de bots desde YAML.
        """
        config_path = Path("config/bots.yml")
        
        if not config_path.exists():
            logger.warning("config/bots.yml no encontrado")
            return {"bots": []}
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {"bots": []}
    
    async def get_bot_metrics(self, handle: str) -> Dict:
        """
        Obtiene métricas de un bot específico.
        
        Args:
            handle: Handle del bot (sin @)
        
        Returns:
            Dict con métricas del bot
        """
        # Buscar config del bot
        bot_config = None
        for bot in self.config.get("bots", []):
            if bot["handle"] == handle:
                bot_config = bot
                break
        
        if not bot_config:
            return {"error": f"Bot {handle} no encontrado en config"}
        
        # Obtener info del usuario
        user_info = await self.twitter_client.get_user_info(handle)
        
        if not user_info:
            return {
                "handle": handle,
                "status": "error",
                "error": "No se pudo obtener información del usuario"
            }
        
        # Obtener tweets recientes
        user_id = user_info["id"]
        recent_tweets = await self.twitter_client.get_recent_tweets(user_id, max_results=10)
        
        # Calcular métricas
        metrics = user_info["metrics"]
        total_tweets = metrics.get("tweet_count", 0)
        followers = metrics.get("followers_count", 0)
        following = metrics.get("following_count", 0)
        
        # Métricas de tweets recientes
        total_impressions = 0
        total_likes = 0
        total_retweets = 0
        total_replies = 0
        top_tweet = None
        last_tweet = None
        
        if recent_tweets:
            last_tweet = recent_tweets[0]
            
            for tweet in recent_tweets:
                tweet_metrics = tweet.get("metrics", {})
                total_impressions += tweet_metrics.get("impression_count", 0)
                total_likes += tweet_metrics.get("like_count", 0)
                total_retweets += tweet_metrics.get("retweet_count", 0)
                total_replies += tweet_metrics.get("reply_count", 0)
                
                # Encontrar top tweet
                if not top_tweet or tweet_metrics.get("impression_count", 0) > top_tweet.get("metrics", {}).get("impression_count", 0):
                    top_tweet = tweet
        
        # Calcular engagement rate
        engagement_rate = 0
        if total_impressions > 0:
            total_engagement = total_likes + total_retweets + total_replies
            engagement_rate = (total_engagement / total_impressions) * 100
        
        # Determinar status
        status = "live"
        if last_tweet:
            last_tweet_time = datetime.fromisoformat(last_tweet["created_at"].replace("Z", "+00:00"))
            time_since_last = datetime.now(last_tweet_time.tzinfo) - last_tweet_time
            
            if time_since_last > timedelta(hours=2):
                status = "paused"
            if time_since_last > timedelta(days=1):
                status = "down"
        else:
            status = "no_tweets"
        
        return {
            "handle": handle,
            "display_name": bot_config.get("display_name", handle),
            "description": bot_config.get("description", ""),
            "color": bot_config.get("color", "#10B981"),
            "status": status,
            "profile_image": user_info.get("profile_image_url"),
            "metrics": {
                "total_tweets": total_tweets,
                "followers": followers,
                "following": following,
                "impressions_recent": total_impressions,
                "likes_recent": total_likes,
                "retweets_recent": total_retweets,
                "replies_recent": total_replies,
                "engagement_rate": round(engagement_rate, 2)
            },
            "top_tweet": {
                "text": top_tweet.get("text", "")[:100] if top_tweet else "",
                "impressions": top_tweet.get("metrics", {}).get("impression_count", 0) if top_tweet else 0,
                "likes": top_tweet.get("metrics", {}).get("like_count", 0) if top_tweet else 0
            } if top_tweet else None,
            "last_tweet": {
                "text": last_tweet.get("text", "")[:100] if last_tweet else "",
                "created_at": last_tweet.get("created_at", "") if last_tweet else "",
                "time_ago": self._time_ago(last_tweet.get("created_at")) if last_tweet else "nunca"
            } if last_tweet else None,
            "recent_tweets": len(recent_tweets)
        }
    
    async def get_all_bots_metrics(self) -> Dict:
        """
        Obtiene métricas de todos los bots configurados.
        
        Returns:
            Dict con métricas de todos los bots
        """
        bots_data = []
        
        for bot_config in self.config.get("bots", []):
            if not bot_config.get("enabled", True):
                continue
            
            handle = bot_config["handle"]
            metrics = await self.get_bot_metrics(handle)
            bots_data.append(metrics)
        
        # Calcular totales
        total_bots = len(bots_data)
        active_bots = sum(1 for bot in bots_data if bot.get("status") == "live")
        total_tweets_today = sum(bot.get("metrics", {}).get("total_tweets", 0) for bot in bots_data)
        total_impressions = sum(bot.get("metrics", {}).get("impressions_recent", 0) for bot in bots_data)
        
        return {
            "bots": bots_data,
            "summary": {
                "total_bots": total_bots,
                "active_bots": active_bots,
                "total_tweets_today": total_tweets_today,
                "total_impressions": total_impressions,
                "uptime_percentage": round((active_bots / total_bots * 100) if total_bots > 0 else 0, 1)
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def _time_ago(self, timestamp_str: str) -> str:
        """
        Convierte timestamp a formato "X tiempo atrás".
        """
        if not timestamp_str:
            return "nunca"
        
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            now = datetime.now(timestamp.tzinfo)
            delta = now - timestamp
            
            if delta.days > 0:
                return f"{delta.days}d ago"
            elif delta.seconds >= 3600:
                hours = delta.seconds // 3600
                return f"{hours}h ago"
            elif delta.seconds >= 60:
                minutes = delta.seconds // 60
                return f"{minutes}m ago"
            else:
                return "just now"
        except Exception as e:
            logger.error(f"Error parsing timestamp: {e}")
            return "unknown"
