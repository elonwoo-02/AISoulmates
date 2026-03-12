import os


def mask_api_key(api_key: str) -> str:
    if not api_key:
        return ''
    visible = api_key[-4:] if len(api_key) > 4 else api_key
    return f'{"*" * max(len(api_key) - len(visible), 4)}{visible}'


def resolve_ai_config(user_profile=None) -> dict:
    user_api_key = (getattr(user_profile, 'api_key', '') or '').strip()
    user_api_base = (getattr(user_profile, 'api_base', '') or '').strip()

    default_api_key = (os.getenv('API_KEY') or '').strip()
    default_api_base = (os.getenv('API_BASE') or '').strip()

    api_key = user_api_key or default_api_key
    api_base = user_api_base or default_api_base

    if not api_key:
        raise ValueError('API key is not configured')
    if not api_base:
        raise ValueError('API base URL is not configured')

    return {
        'api_key': api_key,
        'api_base': api_base,
        'api_key_configured': bool(user_api_key),
        'api_key_masked': mask_api_key(user_api_key),
        'api_base_configured': bool(user_api_base),
        'api_base_value': user_api_base,
        'using_default_api_key': not bool(user_api_key),
        'using_default_api_base': not bool(user_api_base),
    }


def resolve_model_config() -> dict:
    def _get(name: str, default: str) -> str:
        value = (os.getenv(name) or '').strip()
        return value or default

    return {
        'chat_model': _get('CHAT_MODEL', 'qwen3.5-flash'),
        'memory_model': _get('MEMORY_MODEL', 'qwen3.5-flash'),
        'tts_model': _get('TTS_MODEL', 'cosyvoice-v3-flash'),
        'stt_model': _get('STT_MODEL', 'gummy-realtime-v1'),
    }
