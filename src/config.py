"""
Configurações do projeto de Análise de Vendas
"""

import os
from pathlib import Path

# Diretórios do projeto
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
SRC_DIR = PROJECT_ROOT / "src"
DOCS_DIR = PROJECT_ROOT / "docs"
ASSETS_DIR = PROJECT_ROOT / "assets"
TESTS_DIR = PROJECT_ROOT / "tests"

# Arquivos de dados
SALES_DATA_FILE = DATA_DIR / "sales_data.csv"

# Configurações do dashboard
DASHBOARD_CONFIG = {
    "title": "📊 Dashboard de Análise de Vendas",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Configurações de visualização
PLOT_CONFIG = {
    "style": "default",
    "palette": "husl",
    "figure_size": (12, 8),
    "dpi": 100
}

# Configurações de dados
DATA_CONFIG = {
    "date_format": "%Y-%m-%d",
    "decimal_places": 2,
    "currency": "R$"
}

# Cores do projeto
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "warning": "#d62728",
    "info": "#9467bd"
}

# Métricas principais
METRICS = {
    "revenue": "Receita",
    "profit": "Lucro",
    "margin": "Margem",
    "quantity": "Quantidade",
    "orders": "Pedidos"
}
