"""
Twitter API v2 Client

Wrapper para tweepy con métodos específicos para monitoreo.
"""

import tweepy
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class TwitterClient:
    """
    Cliente de Twitter API v2.
    """
    
    def __init__(self, bearer_token: str):
        """
        Inicializa el cliente de Twitter.
        
        Args:
            bearer_token: Bearer token de Twitter API v2
        """
        self.bearer_token = bearer_token
        self.client = tweepy.Client(bearer_token=bearer_token)
    
    async def get_user_info(self, username: str) -> Optional[Dict]:
        """
        Obtiene información de un usuario.
        
        Args:
            username: Handle del usuario (sin @)
        
        Returns:
            Dict con información del usuario o None si hay error
        """
        try:
            response = self.client.get_user(
                username=username,
                user_fields=[
                    "created_at",
                    "description",
                    "public_metrics",
                    "profile_image_url"
                ]
            )
            
            if response.data:
                user = response.data
                return {
                    "id": user.id,
                    "username": user.username,
                    "name": user.name,
                    "description": user.description,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "profile_image_url": user.profile_image_url,
                    "metrics": user.public_metrics
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting user info for {username}: {e}")
            return None
    
    async def get_recent_tweets(self, user_id: str, max_results: int = 10) -> List[Dict]:
        """
        Obtiene tweets recientes de un usuario.
        
        Args:
            user_id: ID del usuario
            max_results: Número máximo de tweets
        
        Returns:
            Lista de tweets
        """
        try:
            response = self.client.get_users_tweets(
                id=user_id,
                max_results=max_results,
                tweet_fields=[
                    "created_at",
                    "public_metrics",
                    "text"
                ]
            )
            
            if response.data:
                tweets = []
                for tweet in response.data:
                    tweets.append({
                        "id": tweet.id,
                        "text": tweet.text,
                        "created_at": tweet.created_at.isoformat() if tweet.created_at else None,
                        "metrics": tweet.public_metrics
                    })
                return tweets
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting tweets for user {user_id}: {e}")
            return []
    
    async def get_user_by_username(self, username: str) -> Optional[str]:
        """
        Obtiene el ID de un usuario por su username.
        
        Args:
            username: Handle del usuario (sin @)
        
        Returns:
            User ID o None
        """
        try:
            response = self.client.get_user(username=username)
            if response.data:
                return str(response.data.id)
            return None
        except Exception as e:
            logger.error(f"Error getting user ID for {username}: {e}")
            return None
