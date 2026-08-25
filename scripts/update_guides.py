import os
import glob
import yaml
from datetime import datetime
import re

CONTENT_DIR = "content"
TOPICS_FILE = "scripts/topics.yaml"

def update_lastmod_dates():
    """Updates the lastmod date in all markdown files in content directory."""
    print("Updating lastmod dates for SEO freshness...")
    md_files = glob.glob(os.path.join(CONTENT_DIR, "**", "*.md"), recursive=True)
    
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S-05:00')
    
    for file_path in md_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Regex to update lastmod in frontmatter
        new_content = re.sub(r"lastmod:\s*.*", f"lastmod: {current_time}", content)
        
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

    if not topics_data or "topics" not in topics_data:
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
