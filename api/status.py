"""
Status Checker

Verifica el estado de los bots y el sistema.
"""

import logging
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class StatusChecker:
    """
    Verificador de estado del sistema.
    """
    
    def __init__(self, twitter_client):
        """
        Inicializa el status checker.
        
        Args:
            twitter_client: Instancia de TwitterClient
        """
        self.twitter_client = twitter_client
    
    async def get_system_status(self) -> Dict:
        """
        Obtiene el estado general del sistema.
        
        Returns:
            Dict con status del sistema
        """
        # Verificar conexión con Twitter API
        twitter_status = "ok"
        try:
            # Test simple: intentar obtener info de Twitter oficial
            test_user = await self.twitter_client.get_user_info("Twitter")
            if not test_user:
                twitter_status = "error"
        except Exception as e:
            logger.error(f"Twitter API check failed: {e}")
            twitter_status = "error"
        
        return {
            "status": "ok" if twitter_status == "ok" else "degraded",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "twitter_api": twitter_status,
                "dashboard": "ok"
            },
            "uptime": "99.9%",  # TODO: Implementar tracking real
            "version": "1.0.0"
        }
