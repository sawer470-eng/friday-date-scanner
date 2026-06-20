import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from config import load_config
from instagram import fetch_instagram_profile
from analyzer import analyze_profile

console = Console()

def render_recommendations(profile, recommendations):
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]@{profile['username']}[/bold cyan] · {profile.get('full_name','')}\n"
        f"👥 {profile.get('followers',0):,} подписчиков · 📸 {profile.get('posts_count',0)} постов",
        title="📱 Профиль",
        border_style="cyan"
    ))
    
    for i, rec in enumerate(recommendations, 1):
        platforms_str = " · ".join(f"[green]{p}[/green]" for p in rec.get("platforms", []))
        if "Не найдено" in str(rec.get("platforms", [])):
            platforms_str = "[yellow]⚠️  Платформа не определена[/yellow]"
        
        content = (
            f"[bold]{rec['title']}[/bold] ({rec.get('year','—')})\n"
            f"🎭 {rec.get('genre','—')}  ·  💫 {rec.get('mood','—')}\n\n"
            f"{rec.get('reason','')}\n\n"
            f"📺 Доступно: {platforms_str}"
        )
        console.print(Panel(content, title=f"#{i}", border_style="magenta"))

def cmd_scan(args):
    config = load_config()
    
    with Progress(SpinnerColumn(), TextColumn("[cyan]{task.description}"), transient=True) as p:
        t = p.add_task("Загружаем профиль Instagram...", total=None)
        profile = fetch_instagram_profile(args.username, config)
        p.update(t, description="Анализируем интересы через Groq...")
        recommendations = analyze_profile(profile, config)
    
    render_recommendations(profile, recommendations)
    console.print("\n[bold green]✅ Готово! Приятного свидания 🍿[/bold green]\n")

def main():
    parser = argparse.ArgumentParser(description="Friday Date Scanner — рекомендации для свидания")
    sub = parser.add_subparsers(dest="command", required=True)
    
    scan = sub.add_parser("scan", help="Сканировать Instagram профиль")
    scan.add_argument("--username", "-u", required=True, help="Instagram username (с @ или без)")
    scan.set_defaults(func=cmd_scan)
    
    args = parser.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        console.print("\n[yellow]Отменено[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]❌ Ошибка:[/bold red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
