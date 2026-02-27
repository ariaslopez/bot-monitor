# 🤖 Bot Monitor Dashboard

**Monitoreo en tiempo real para bots de Twitter/X con diseño glassmorphism estilo ageek.work**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Twitter API](https://img.shields.io/badge/Twitter%20API-v2-1DA1F2)](https://developer.twitter.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Características

- ✅ **Métricas en tiempo real** - Twitter API v2
- ✅ **Dashboard moderno** - Estilo ageek.work glassmorphism
- ✅ **Status live** - Indicadores visuales de estado
- ✅ **Múltiples bots** - Monitorea todos tus bots
- ✅ **Sparkline charts** - Tendencias visuales
- ✅ **Dark mode** - Optimizado para ojos
- ✅ **Auto-refresh** - Datos actualizados cada 30s

---

## 🚀 Quick Start

### 1. Clonar repositorio

```bash
git clone https://github.com/ariaslopez/bot-monitor.git
cd bot-monitor
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Twitter API

```bash
cp .env.example .env
# Editar .env con tu Bearer Token
```

**Obtener Bearer Token:**
1. Ve a [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Tu proyecto → Keys and tokens
3. Copia el **Bearer Token**

### 4. Configurar bots

Edita `config/bots.yml`:

```yaml
bots:
  - handle: "AdaBotLive"
    display_name: "ADA Bot Live"
    description: "Bot de análisis de Cardano"
    
  - handle: "BTCInsights"
    display_name: "BTC Insights"
    description: "Bot de Bitcoin"
```

### 5. Ejecutar dashboard

```bash
python app.py
```

Abre: http://localhost:5000

---

## 📊 Métricas Disponibles

### Por Bot:
- 📊 **Total tweets**
- 👁️ **Impresiones** (24h)
- ❤️ **Likes** totales
- 🔄 **Retweets** totales
- 💬 **Replies** totales
- 📈 **Engagement rate**
- 👥 **Followers** count
- 🔥 **Top tweet** del día
- ⏰ **Último tweet** (timestamp)
- 🟢 **Status** (Live/Paused/Down)

### Globales:
- 📊 **Total bots activos**
- 📈 **Uptime general**
- 🔥 **Tweets totales hoy**
- 👁️ **Impresiones totales**

---

## 🎨 Diseño

**Inspirado en [ageek.work](https://ageek.work)**

- ✨ Glassmorphism cards
- 🌃 Dark mode default
- 💠 Smooth animations
- 📊 Sparkline charts
- 🟢 Status indicators con glow
- 📱 Responsive design

---

## 🛠️ Stack Tecnológico

- **Backend:** FastAPI (Python)
- **Frontend:** HTML5 + CSS3 + Vanilla JS
- **API:** Twitter API v2
- **Charts:** Chart.js (sparklines)
- **Estilo:** Custom CSS (glassmorphism)

---

## 📝 Estructura

```
bot-monitor/
├── app.py                 # FastAPI server
├── api/
│   ├── twitter.py         # Twitter API v2 client
│   ├── metrics.py         # Métricas processor
│   └── status.py          # Bot health check
├── config/
│   └── bots.yml           # Configuración de bots
├── static/
│   ├── css/
│   │   └── style.css      # Ageek.work vibes
│   └── js/
│       └── dashboard.js   # Real-time updates
├── templates/
│   └── index.html         # Dashboard principal
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Configuración

### `.env`

```env
# Twitter API
TWITTER_BEARER_TOKEN=your_bearer_token_here

# Dashboard
REFRESH_INTERVAL=30  # segundos
PORT=5000
HOST=0.0.0.0

# Debug
DEBUG=True
```

### `config/bots.yml`

```yaml
bots:
  - handle: "AdaBotLive"              # Sin @
    display_name: "ADA Bot Live"       # Nombre en dashboard
    description: "Bot de Cardano"      # Descripción
    color: "#10B981"                    # Color del status indicator
    
  - handle: "BTCInsights"
    display_name: "BTC Insights"
    description: "Bitcoin Analysis"
    color: "#F59E0B"
```

---

## 📊 API Endpoints

### Dashboard
```
GET /                    # Página principal
```

### Métricas
```
GET /api/bots            # Lista de bots con métricas
GET /api/bot/{handle}    # Métricas de un bot específico
GET /api/status          # Status general
```

### Tiempo Real
```
GET /api/live/{handle}   # Stream de datos en vivo
```

---

## 🔥 Preview del Dashboard

```
┌──────────────────────────────────────────────────────┐
│  🤖 BOT MONITOR        🟢 2 Active  🕒 11:30 PM  │
├──────────────────────────────────────────────────────┤
│                                                    │
│  ┌─ @AdaBotLive ────────────────────────────┐  │
│  │ 🟢 LIVE  2min ago                       │  │
│  │                                            │  │
│  │ 📊 247 tweets    👁️ 12.3k impresiones  │  │
│  │ ❤️ 234 likes     🔄 87 retweets        │  │
│  │ 📈 5.2% engagement  👥 1.2k followers  │  │
│  │                                            │  │
│  │ 🔥 TOP: "ADA pump!" • 2.3k impres       │  │
│  │ ⏰ Next: 8 min                            │  │
│  └────────────────────────────────────────────┘  │
│                                                    │
└──────────────────────────────────────────────────────┘
```

---

## 👥 Uso

### Monitor Local
```bash
python app.py
# http://localhost:5000
```

### Monitor Remoto (Deploy)
```bash
# Railway/Render/Vercel
vercel deploy
```

---

## 🔧 Próximos Features

- [ ] Alertas por Discord/Telegram
- [ ] Historial de métricas (24h/7d/30d)
- [ ] Comparación entre bots
- [ ] Export de reportes (CSV/PDF)
- [ ] Dashboard móvil (PWA)
- [ ] Integración con pagos (Cardano)
- [ ] Multi-plataforma (Discord, Telegram)

---

## 👤 Autor

**Daniel H. Arias López**
- GitHub: [@ariaslopez](https://github.com/ariaslopez)
- Twitter: [@CryptoIntelBot](https://twitter.com/CryptoIntelBot)

---

## 📝 Licencia

MIT License - ¡Usa libremente!

---

⭐ **Si te gusta este proyecto, ¡dale una estrella!**
