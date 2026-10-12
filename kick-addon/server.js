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

app.get('/manifest.json', (req, res) => {
    res.json({
        "id": "org.kick.custom.streamer",
        "version": "3.0.0",
        "name": "Kick Live Streams",
        "description": "قنوات كيك مباشر",
        "resources": ["catalog", "meta", "stream"],
        "types": ["tv"],
        "catalogs": [
            { "type": "tv", "id": "kick_live", "name": "🔴 قنوات كيك المباشرة" }
        ],
        "idPrefixes": ["kick_"]
    });
});

app.get('/catalog/tv/kick_live.json', (req, res) => {
    const metas = MY_CHANNELS.map(ch => ({
        id: `kick_${ch.username}`,
        type: 'tv',
        name: ch.name,
        poster: 'https://kick.com/favicon.ico',
        description: `بث مباشر لقناة ${ch.name}`
    }));
    res.json({ metas });
});

app.get('/meta/tv/:id.json', (req, res) => {
    const cleanId = req.params.id.replace('.json', '').replace('kick_', '');
    res.json({
        meta: {
            id: `kick_${cleanId}`,
            type: 'tv',
            name: cleanId,
            poster: 'https://kick.com/favicon.ico',
            description: `بث مباشر لقناة ${cleanId}`
        }
    });
});

app.get('/stream/tv/:id.json', (req, res) => {
    const cleanId = req.params.id.replace('.json', '').replace('kick_', '');
    res.json({
        streams: [
            { title: '💎 بث مباشر (1080p60)', url: `https://stream.kick.com/livestream/${cleanId}/index.m3u8` },
            { title: '🔵 بث مباشر (720p)', url: `https://stream.kick.com/livestream/${cleanId}/720p/index.m3u8` }
        ]
    });
});

app.listen(7000, '0.0.0.0', () => {
    console.log('Server running on port 7000');
});
