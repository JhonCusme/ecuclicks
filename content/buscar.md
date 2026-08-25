---
title: "Buscar Guías"
description: "Encuentra el trámite que necesitas rápidamente."
layout: "search"
---

<div class="search-container">
    <input type="text" id="searchInput" placeholder="Escribe lo que buscas (ej. Cédula, RUC)..." autofocus>
    <div id="searchResults" class="guide-grid" style="margin-top: 30px;">
        <!-- Los resultados aparecerán aquí -->
    </div>
</div>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');
        let indexData = [];

        // Obtener el parámetro 'q' de la URL si existe
        const urlParams = new URLSearchParams(window.location.search);
        const query = urlParams.get('q');

        fetch('/index.json')
            .then(response => response.json())
            .then(data => {
                indexData = data;
                if(query) {
                    searchInput.value = query;
                    performSearch(query);
                }
            });

        searchInput.addEventListener('input', function() {
            performSearch(this.value);
        });

        function performSearch(query) {
            searchResults.innerHTML = '';
            if (query.length < 2) return;
            
            const lowerQuery = query.toLowerCase();
            const results = indexData.filter(item => 
                item.title.toLowerCase().includes(lowerQuery) || 
                item.content.toLowerCase().includes(lowerQuery)
            );

            if(results.length === 0) {
                searchResults.innerHTML = '<p>No se encontraron resultados para "'+ query +'". Intenta con otras palabras.</p>';
                return;
            }

            results.forEach(item => {
                const article = document.createElement('article');
                article.className = 'guide-card';
                article.innerHTML = `
                    <h3><a href="${item.url}">${item.title}</a></h3>
                    <p class="card-excerpt">${item.summary.substring(0, 120)}...</p>
                    <div class="card-footer">
                        <a href="${item.url}" class="card-link">Leer guía →</a>
                    </div>
                `;
                searchResults.appendChild(article);
            });
        }
    });
</script>

<style>
    .search-container input {
        width: 100%;
        padding: 15px 20px;
        font-size: 1.1rem;
        border: 2px solid var(--border);
        border-radius: var(--radius-sm);
        outline: none;
        transition: border-color var(--transition);
    }
    .search-container input:focus {
        border-color: var(--primary);
    }
</style>
