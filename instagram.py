import json
import instaloader
from pathlib import Path

def load_mock_profile(username):
    """Загрузка тестового профиля из JSON"""
    mock_file = Path(__file__).parent / "mock_profiles.json"
    with open(mock_file, "r", encoding="utf-8") as f:
        profiles = json.load(f)
    username = username.lstrip("@")
    if username in profiles:
        return profiles[username]
    return profiles.get("default", profiles[list(profiles.keys())[0]])

def fetch_instagram_profile(username, config):
    """Загрузка реального профиля через instaloader"""
    if config["USE_MOCK_DATA"]:
        return load_mock_profile(username)
    
    username = username.lstrip("@")
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_comments=False,
        save_metadata=False,
    )
    
    if config["INSTAGRAM_USERNAME"] and config["INSTAGRAM_PASSWORD"]:
        try:
            L.login(config["INSTAGRAM_USERNAME"], config["INSTAGRAM_PASSWORD"])
        except Exception as e:
            print(f"⚠️  Не удалось войти в Instagram: {e}")
    
    try:
        profile = instaloader.Profile.from_username(L.context, username)
    except Exception as e:
        raise RuntimeError(f"Не удалось загрузить @{username}: {e}")
    
    posts_data = []
    for i, post in enumerate(profile.get_posts()):
        if i >= 10:
            break
        posts_data.append({
            "caption": (post.caption or "")[:500],
            "hashtags": list(post.caption_hashtags)[:10],
            "likes": post.likes,
            "is_video": post.is_video,
        })
    
    return {
        "username": profile.username,
        "full_name": profile.full_name,
        "bio": profile.biography,
        "followers": profile.followers,
        "following": profile.followees,
        "posts_count": profile.mediacount,
        "posts": posts_data,
    }
