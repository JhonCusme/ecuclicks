import os
import glob
import random
import yaml
from datetime import datetime, timedelta
import re

CONTENT_DIR = "content"
TOPICS_FILE = "scripts/topics.yaml"
EXCLUDED_FILES = {"buscar.md", "contacto.md", "sobre-nosotros.md"}

def update_lastmod_dates():
    """Updates the lastmod date in a realistic, randomized subset of guides for natural SEO growth."""
    print("Updating lastmod dates for SEO freshness...")
    all_files = glob.glob(os.path.join(CONTENT_DIR, "**", "*.md"), recursive=True)
    
    # Exclude root static pages
    guide_files = [f for f in all_files if os.path.basename(f) not in EXCLUDED_FILES]
    
    if not guide_files:
        print("No guide files found.")
        return

    # Select 3 to 6 guides randomly so we don't modify everything at once (simulates genuine organic updates)
    sample_size = min(len(guide_files), random.randint(3, 6))
    selected_files = random.sample(guide_files, sample_size)
    print(f"Selected {len(selected_files)} guides to update lastmod.")

    now = datetime.now()
    for file_path in selected_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Add random minutes/seconds offset for natural appearance
        offset_minutes = random.randint(5, 180)
        file_time = (now - timedelta(minutes=offset_minutes)).strftime('%Y-%m-%dT%H:%M:%S-05:00')
        
        # Regex to update lastmod in frontmatter
        new_content = re.sub(r"lastmod:\s*.*", f"lastmod: {file_time}", content)
        
        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated lastmod in: {file_path}")

def create_placeholders_for_new_topics():
    """Reads topics.yaml and creates placeholder markdown files if they don't exist."""
    print("Checking for new topics in topics.yaml...")
    if not os.path.exists(TOPICS_FILE):
        print(f"File {TOPICS_FILE} not found. Skipping.")
        return

    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        topics_data = yaml.safe_load(f)

    if not topics_data or not topics_data.get("topics"):
        print("No new topics to create.")
        return

    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S-05:00')

    for topic in topics_data["topics"]:
        category = topic.get("category", "otros")
        slug = topic.get("slug")
        title = topic.get("title", slug)
        
        if not slug:
            continue
            
        cat_dir = os.path.join(CONTENT_DIR, category)
        os.makedirs(cat_dir, exist_ok=True)
        
        file_path = os.path.join(cat_dir, f"{slug}.md")
        
        if not os.path.exists(file_path):
            print(f"Creating new placeholder for topic: {title}")
            content = f"""---
title: "{title}"
description: "Guía paso a paso sobre {title}"
date: {current_time}
lastmod: {current_time}
categories: ["{category.capitalize().replace('-', ' ')}"]
---

## ¿Qué es este trámite?
[Escribe aquí la descripción]

## Requisitos
- Requisito 1

## Pasos para realizar el trámite
1. Paso 1

## Costos y Tiempos
- Costo:
- Tiempo:

## Preguntas Frecuentes
**Pregunta 1**
Respuesta 1
"""
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == "__main__":
    print("Running Ecucliks Maintenance Script...")
    update_lastmod_dates()
    create_placeholders_for_new_topics()
    print("Maintenance complete.")
