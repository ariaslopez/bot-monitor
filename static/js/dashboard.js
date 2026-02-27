/**
 * Bot Monitor Dashboard
 * Real-time updates and animations
 */

const REFRESH_INTERVAL = 30000; // 30 seconds
let refreshTimer;

// Format numbers
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k';
    }
    return num.toString();
}

// Update current time
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
    });
    document.getElementById('current-time').textContent = timeString;
}

// Load bots data
async function loadBots() {
    try {
        const response = await fetch('/api/bots');
        const data = await response.json();
        
        if (data.error) {
            showError(data.error);
            return;
        }
        
        // Update summary
        updateSummary(data.summary);
        
        // Render bots
        renderBots(data.bots);
        
    } catch (error) {
        console.error('Error loading bots:', error);
        showError('Error al cargar datos. Verifica que Twitter API esté configurado.');
    }
}

// Update summary cards
function updateSummary(summary) {
    document.getElementById('total-tweets').textContent = formatNumber(summary.total_tweets_today);
    document.getElementById('total-impressions').textContent = formatNumber(summary.total_impressions);
    document.getElementById('uptime-percentage').textContent = summary.uptime_percentage + '%';
    document.getElementById('active-count').textContent = summary.active_bots;
}

// Render bots grid
function renderBots(bots) {
    const grid = document.getElementById('bots-grid');
    
    if (bots.length === 0) {
        grid.innerHTML = `
            <div class="loading-state glass">
                <p>⚠️ No hay bots configurados</p>
                <p style="font-size: 0.9rem; color: var(--text-secondary); margin-top: 1rem;">
                    Edita <code>config/bots.yml</code> para agregar bots
                </p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = bots.map(bot => createBotCard(bot)).join('');
}

// Create bot card HTML
function createBotCard(bot) {
    const metrics = bot.metrics || {};
    const topTweet = bot.top_tweet;
    const lastTweet = bot.last_tweet;
    
    return `
        <div class="bot-card glass status-${bot.status}">
            <div class="bot-header">
                <img src="${bot.profile_image || 'https://abs.twimg.com/sticky/default_profile_images/default_profile_400x400.png'}" 
                     alt="${bot.handle}" 
                     class="bot-avatar">
                <div class="bot-info">
                    <div class="bot-name">
                        ${bot.display_name}
                        <span class="bot-status ${bot.status}">
                            ${bot.status}
                        </span>
                    </div>
                    <div class="bot-handle">@${bot.handle}</div>
                </div>
            </div>
            
            <div class="bot-metrics">
                <div class="metric">
                    <span class="metric-icon">📊</span>
                    <div>
                        <div class="metric-value">${formatNumber(metrics.total_tweets || 0)}</div>
                        <div class="metric-label">Tweets</div>
                    </div>
                </div>
                
                <div class="metric">
                    <span class="metric-icon">👁️</span>
                    <div>
                        <div class="metric-value">${formatNumber(metrics.impressions_recent || 0)}</div>
                        <div class="metric-label">Impresiones</div>
                    </div>
                </div>
                
                <div class="metric">
                    <span class="metric-icon">❤️</span>
                    <div>
                        <div class="metric-value">${formatNumber(metrics.likes_recent || 0)}</div>
                        <div class="metric-label">Likes</div>
                    </div>
                </div>
                
                <div class="metric">
                    <span class="metric-icon">🔄</span>
                    <div>
                        <div class="metric-value">${formatNumber(metrics.retweets_recent || 0)}</div>
                        <div class="metric-label">Retweets</div>
                    </div>
                </div>
                
                <div class="metric">
                    <span class="metric-icon">👥</span>
                    <div>
                        <div class="metric-value">${formatNumber(metrics.followers || 0)}</div>
                        <div class="metric-label">Followers</div>
                    </div>
                </div>
                
                <div class="metric">
                    <span class="metric-icon">📈</span>
                    <div>
                        <div class="metric-value">${metrics.engagement_rate || 0}%</div>
                        <div class="metric-label">Engagement</div>
                    </div>
                </div>
            </div>
            
            ${topTweet ? `
                <div class="top-tweet">
                    <div class="top-tweet-label">🔥 Top Tweet</div>
                    <div class="top-tweet-text">${topTweet.text}</div>
                    <div class="top-tweet-stats">
                        <span>👁️ ${formatNumber(topTweet.impressions)}</span>
                        <span>❤️ ${formatNumber(topTweet.likes)}</span>
                    </div>
                </div>
            ` : ''}
            
            ${lastTweet ? `
                <div class="last-tweet">
                    ⏰ Último tweet: ${lastTweet.time_ago}
                </div>
            ` : ''}
        </div>
    `;
}

// Show error message
function showError(message) {
    const grid = document.getElementById('bots-grid');
    grid.innerHTML = `
        <div class="loading-state glass">
            <p style="color: var(--status-down);">❌ ${message}</p>
        </div>
    `;
}

// Start auto-refresh
function startAutoRefresh() {
    refreshTimer = setInterval(() => {
        console.log('🔄 Auto-refreshing data...');
        loadBots();
    }, REFRESH_INTERVAL);
}

// Initialize dashboard
function init() {
    console.log('🚀 Bot Monitor Dashboard initialized');
    
    // Update clock every second
    updateClock();
    setInterval(updateClock, 1000);
    
    // Load initial data
    loadBots();
    
    // Start auto-refresh
    startAutoRefresh();
}

// Start when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
