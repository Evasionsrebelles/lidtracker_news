#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour ajouter des news au fichier news.json avec traduction automatique
Usage: python add_news.py
"""

import json
import os
from datetime import datetime, timezone
import sys

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Chemin du fichier news.json
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NEWS_FILE = os.path.join(SCRIPT_DIR, "news.json")


def load_news():
    """Charge le fichier news.json"""
    if not os.path.exists(NEWS_FILE):
        print(f"❌ Erreur : {NEWS_FILE} introuvable!")
        sys.exit(1)
    
    try:
        with open(NEWS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        print("❌ Erreur : news.json n'est pas un JSON valide!")
        sys.exit(1)


def save_news(data):
    """Sauvegarde le fichier news.json"""
    try:
        with open(NEWS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Fichier {NEWS_FILE} mis à jour avec succès!")
    except IOError as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")
        sys.exit(1)


def translate_text(text, target_lang):
    """Traduit un texte en utilisant l'API MyMemory (gratuit, sans clés)"""
    if not REQUESTS_AVAILABLE:
        print(f"⚠️  Impossible de traduire (requests non disponible)")
        return None
    
    try:
        # Utiliser MyMemory API (gratuit, pas besoin de clés)
        url = "https://api.mymemory.translated.net/get"
        params = {
            'q': text,
            'langpair': f'fr|{target_lang}'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('responseStatus') == 200:
            translated = data['responseData']['translatedText']
            return translated
        else:
            print(f"⚠️  Erreur de traduction : {data.get('responseDetails')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Erreur de connexion : {e}")
        return None
    except Exception as e:
        print(f"⚠️  Erreur lors de la traduction : {e}")
        return None


def input_news_text():
    """Demande le texte de la news à l'utilisateur"""
    print("\n📝 Entrez le texte de la news (terminé par Entrée deux fois) :")
    print("(Appuyez sur Entrée deux fois pour terminer)")
    
    lines = []
    empty_count = 0
    
    while True:
        line = input()
        if line == "":
            empty_count += 1
            if empty_count >= 2:
                break
            lines.append("")
        else:
            empty_count = 0
            lines.append(line)
    
    text = "\n".join(lines).strip()
    
    if not text:
        print("❌ Erreur : la news ne peut pas être vide!")
        return None
    
    return text


def add_news():
    """Ajoute une news au fichier avec traduction automatique"""
    # Charger les données
    data = load_news()
    
    # Saisir le texte en français
    print("\n📝 Entrez la news en FRANÇAIS")
    news_text_fr = input_news_text()
    if news_text_fr is None:
        return
    
    print("\n⏳ Traduction en cours...")
    
    # Traduire automatiquement
    news_text_en = translate_text(news_text_fr, 'en')
    news_text_jp = translate_text(news_text_fr, 'ja')
    
    if not news_text_en:
        news_text_en = news_text_fr
        print("⚠️  Traduction EN impossible - utilisation du texte français")
    
    if not news_text_jp:
        news_text_jp = news_text_fr
        print("⚠️  Traduction JP impossible - utilisation du texte français")
    
    # Ajouter les news au début de chaque liste
    for lang, text in [('fr', news_text_fr), ('en', news_text_en), ('jp', news_text_jp)]:
        if lang not in data:
            data[lang] = []
        data[lang].insert(0, text)
    
    # Mettre à jour l'horodatage (ISO 8601 avec fuseau horaire UTC)
    data["timestamp"] = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    
    # Sauvegarder
    save_news(data)
    
    # Afficher confirmation
    print(f"\n✅ News ajoutée dans les 3 langues!")
    print(f"   Horodatage : {data['timestamp']}")
    print(f"\n🇫🇷 Français :")
    print(f"   {news_text_fr[:60]}..." if len(news_text_fr) > 60 else f"   {news_text_fr}")
    print(f"\n🇬🇧 English :")
    print(f"   {news_text_en[:60]}..." if len(news_text_en) > 60 else f"   {news_text_en}")
    print(f"\n🇯🇵 日本語 :")
    print(f"   {news_text_jp[:60]}..." if len(news_text_jp) > 60 else f"   {news_text_jp}")


def show_current_news():
    """Affiche les news actuelles"""
    data = load_news()
    
    print("\n📋 News actuelles :")
    print(f"Dernière mise à jour : {data.get('timestamp', '—')}\n")
    
    for lang in ['fr', 'en', 'jp']:
        if lang in data and data[lang]:
            lang_names = {'fr': '🇫🇷 Français', 'en': '🇬🇧 English', 'jp': '🇯🇵 日本語'}
            print(f"{lang_names[lang]} ({lang}) :")
            for i, news in enumerate(data[lang], 1):
                preview = news[:60] + "..." if len(news) > 60 else news
                print(f"  {i}. {preview}")
            print()


def main():
    """Fonction principale"""
    print("=" * 60)
    print("📰 Gestionnaire de News - Pokelids")
    print("=" * 60)
    
    if not REQUESTS_AVAILABLE:
        print("\n⚠️  ATTENTION : Le module 'requests' n'est pas installé.")
        print("   Installez-le avec : pip install requests")
        print("   La traduction automatique ne fonctionnera pas.\n")
        response = input("Continuer quand même ? (o/n) : ").strip().lower()
        if response != 'o':
            print("Au revoir! 👋")
            sys.exit(0)
    
    # Afficher les news actuelles
    show_current_news()
    
    # Demander l'action
    print("Options :")
    print("  [1] Ajouter une news")
    print("  [2] Quitter")
    
    choice = input("\nChoix (1/2) : ").strip()
    
    if choice == "1":
        add_news()
    elif choice == "2":
        print("Au revoir! 👋")
    else:
        print("❌ Choix invalide.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterruption de l'utilisateur. Au revoir! 👋")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        sys.exit(1)
