cd ~/iptv-termux/kick-addon 2>/dev/null || mkdir -p ~/iptv-termux/kick-addon && cd ~/iptv-termux/kick-addon
cat << 'INNER_EOF' > server.js
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

const MY_CHANNELS = [
    { username: "We11y", name: "We11y" },
    { username: "ogabdullah", name: "ogabdullah" },
    { username: "TheWitty21", name: "TheWitty21" },
    { username: "PLAYAWAY", name: "PLAYAWAY" },
    { username: "abu_abeer16", name: "abu_abeer16" },
    { username: "ko3ib", name: "ko3ib" },
    { username: "LLE", name: "LLE" },
    { username: "ibrahim_dos", name: "ibrahim_dos" },
    { username: "Aziz", name: "Aziz" }
];

const manifest = {
    "id": "org.kick.custom.streamer",
    "version": "1.5.0",
    "name": "Kick Live & VODs",
    "description": "قنوات كيك البث المباشر والإعادات",
    "resources": ["catalog", "stream"],
    "types": ["tv", "other"],
    "catalogs": [
        { "type": "tv", "id": "kick_live_channels", "name": "🔴 قنوات كيك - البث المباشر" },
        { "type": "tv", "id": "kick_vod_channels", "name": "📹 قنوات كيك - الإعادات (VODs)" }
    ],
    "idPrefixes": ["kicklive_", "kickvod_"]
};

app.get('/manifest.json', (req, res) => {
    res.json(manifest);
});

app.get('/catalog/:type/:id.json', (req, res) => {
    const catalogId = req.params.id;
    if (catalogId === 'kick_live_channels') {
        const metas = MY_CHANNELS.map(ch => ({
            id: `kicklive_${ch.username}`,
            type: 'tv',
            name: `🔴 ${ch.name}`,
            poster: 'https://kick.com/favicon.ico',
            posterShape: 'square',
            description: `بث مباشر لقناة ${ch.name}`
        }));
        return res.json({ metas });
    }
    if (catalogId === 'kick_vod_channels') {
        const metas = MY_CHANNELS.map(ch => ({
            id: `kickvod_${ch.username}`,
            type: 'tv',
            name: `📹 إعادة: ${ch.name}`,
            poster: 'https://kick.com/favicon.ico',
            posterShape: 'square',
            description: `إعادات البث لقناة ${ch.name}`
        }));
        return res.json({ metas });
    }
    res.json({ metas: [] });
});

app.get('/stream/:type/:id.json', (req, res) => {
    const streamId = req.params.id;
    let cleanId = streamId.replace('.json', '');
    
    if (cleanId.startsWith('kicklive_')) {
        const channel = cleanId.replace('kicklive_', '');
        return res.json({
            streams: [
                { title: '💎 1080p60 (أعلى جودة)', url: `https://stream.kick.com/livestream/${channel}/index.m3u8` },
                { title: '🔵 720p60', url: `https://stream.kick.com/livestream/${channel}/720p/index.m3u8` },
                { title: '🟡 480p', url: `https://stream.kick.com/livestream/${channel}/480p/index.m3u8` },
                { title: '🟢 360p', url: `https://stream.kick.com/livestream/${channel}/360p/index.m3u8` },
                { title: '⚪ 160p (أقل جودة)', url: `https://stream.kick.com/livestream/${channel}/160p/index.m3u8` }
            ]
        });
    }
    if (cleanId.startsWith('kickvod_')) {
        const channel = cleanId.replace('kickvod_', '');
        return res.json({
            streams: [
                { title: '📼 آخر إعادة بث (1080p)', url: `https://stream.kick.com/vod/${channel}/latest/index.m3u8` },
                { title: '📼 آخر إعادة بث (720p)', url: `https://stream.kick.com/vod/${channel}/latest/720p/index.m3u8` },
                { title: '📼 آخر إعادة بث (480p)', url: `https://stream.kick.com/vod/${channel}/latest/480p/index.m3u8` }
            ]
        });
    }
    // Fallback مباشر لأي اسم مستخدم
    return res.json({
        streams: [
            { title: '💎 1080p60 (مباشر)', url: `https://stream.kick.com/livestream/${cleanId}/index.m3u8` }
        ]
    });
});

app.listen(7000, '0.0.0.0', () => {
    console.log('Server running on port 7000');
});
INNER_EOF
npm init -y >/dev/null 2>&1
npm install express cors >/dev/null 2>&1
node server.js
