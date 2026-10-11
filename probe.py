import asyncio
import json

async def get_stream_metrics(stream_url: str) -> dict:
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_streams', '-show_format', '-analyzeduration', '1000000', '-probesize', '1000000',
        stream_url
    ]
    
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=4.0)
        data = json.loads(stdout.decode())
        
        v_stream = next((s for s in data.get('streams', []) if s.get('codec_type') == 'video'), None)
        if not v_stream:
            return {"fps": "N/A", "bitrate": "N/A", "resolution": "N/A"}

        fps_raw = v_stream.get('r_frame_rate', '0/1').split('/')
        fps = round(int(fps_raw[0]) / int(fps_raw[1]), 1) if len(fps_raw) == 2 and int(fps_raw[1]) > 0 else "N/A"
        
        bitrate_raw = data.get('format', {}).get('bit_rate') or v_stream.get('bit_rate', '0')
        bitrate = f"{int(bitrate_raw) // 1000} Kbps" if str(bitrate_raw).isdigit() and int(bitrate_raw) > 0 else "متغير / Live"

        res = f"{v_stream.get('width', '?')}x{v_stream.get('height', '?')}"
        return {"fps": str(fps), "bitrate": bitrate, "resolution": res, "codec": v_stream.get('codec_name', 'N/A')}
    except Exception:
        return {"fps": "غير معروف", "bitrate": "غير معروف", "resolution": "غير معروف", "codec": "N/A"}

