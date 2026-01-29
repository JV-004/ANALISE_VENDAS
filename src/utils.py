"""
Utilitários para o projeto de Análise de Vendas
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import plotly.express as px
import plotly.graph_objects as go
from config import DATA_CONFIG, COLORS


def load_data(file_path: str) -> pd.DataFrame:
    """
    Carrega e prepara os dados de vendas

    Args:
        file_path (str): Caminho para o arquivo CSV

    Returns:
        pd.DataFrame: DataFrame com dados limpos e preparados
    """
    try:
        df = pd.read_csv(file_path)
        df = prepare_data(df)
        return df
    except Exception as e:
        raise Exception(f"Erro ao carregar dados: {e}")


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara e limpa os dados

    Args:
        df (pd.DataFrame): DataFrame bruto

    Returns:
        pd.DataFrame: DataFrame preparado
    """
    # Cópia dos dados
    df_clean = df.copy()

    # Remover nulos e duplicatas
    df_clean = df_clean.dropna()
    df_clean = df_clean.drop_duplicates()

    # Converter tipos
    df_clean['order_date'] = pd.to_datetime(df_clean['order_date'])

    # Criar features temporais
    df_clean['year'] = df_clean['order_date'].dt.year
    df_clean['month'] = df_clean['order_date'].dt.month
    df_clean['day_of_week'] = df_clean['order_date'].dt.dayofweek
    df_clean['quarter'] = df_clean['order_date'].dt.quarter

    # Criar features de negócio
    df_clean['margin'] = df_clean['profit'] / df_clean['revenue']
    df_clean['revenue_per_unit'] = df_clean['revenue'] / df_clean['quantity']

    # Categorizar tickets
    df_clean['ticket_category'] = pd.cut(
        df_clean['revenue'],
        bins=[0, 1000, 5000, 10000, float('inf')],
        labels=['Baixo', 'Médio', 'Alto', 'Premium']
    )

    return df_clean


def calculate_kpis(df: pd.DataFrame) -> Dict:
    """
    Calcula os principais KPIs

    Args:
        df (pd.DataFrame): DataFrame com dados de vendas

    Returns:
        Dict: Dicionário com KPIs calculados
    """
    kpis = {
        'total_revenue': df['revenue'].sum(),
        'total_profit': df['profit'].sum(),
        'avg_ticket': df['revenue'].mean(),
        'total_orders': len(df),
        'unique_customers': df['customer'].nunique(),
        'unique_products': df['product'].nunique(),
        'avg_margin': (df['profit'].sum() / df['revenue'].sum()) * 100,
        'avg_quantity': df['quantity'].mean()
    }

    return kpis


def get_top_performers(df: pd.DataFrame, column: str, metric: str = 'revenue', top_n: int = 10) -> pd.Series:
    """
    Retorna os top performers por uma métrica

    Args:
        df (pd.DataFrame): DataFrame com dados
        column (str): Coluna para agrupar
        metric (str): Métrica para ordenar
        top_n (int): Número de itens a retornar

    Returns:
        pd.Series: Top performers
    """
    return df.groupby(column)[metric].sum().sort_values(ascending=False).head(top_n)


def format_currency(value: float) -> str:
    """
    Formata valor como moeda brasileira

    Args:
        value (float): Valor a ser formatado

    Returns:
        str: Valor formatado
    """
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def format_percentage(value: float) -> str:
    """
    Formata valor como percentual

    Args:
        value (float): Valor a ser formatado

    Returns:
        str: Valor formatado como percentual
    """
    return f"{value:.1f}%"


def create_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria tabela resumo com principais métricas

    Args:
        df (pd.DataFrame): DataFrame com dados

    Returns:
        pd.DataFrame: Tabela resumo
    """
    kpis = calculate_kpis(df)

    summary_data = {
        'Métrica': [
            'Receita Total',
            'Lucro Total',
            'Margem Média',
            'Ticket Médio',
            'Total de Pedidos',
            'Clientes Únicos',
            'Produtos Únicos'
        ],
        'Valor': [
            format_currency(kpis['total_revenue']),
            format_currency(kpis['total_profit']),
            format_percentage(kpis['avg_margin']),
            format_currency(kpis['avg_ticket']),
            f"{kpis['total_orders']:,}",
            f"{kpis['unique_customers']:,}",
            f"{kpis['unique_products']:,}"
        ]
    }

    return pd.DataFrame(summary_data)


def generate_insights(df: pd.DataFrame) -> Dict:
    """
    Gera insights automáticos dos dados

    Args:
        df (pd.DataFrame): DataFrame com dados

    Returns:
        Dict: Insights gerados
    """
    insights = {}

    # Top performers
    insights['best_category'] = df.groupby(
        'category')['revenue'].sum().idxmax()
    insights['best_region'] = df.groupby('region')['revenue'].sum().idxmax()
    insights['best_product'] = df.groupby('product')['revenue'].sum().idxmax()
    insights['best_customer'] = df.groupby(
        'customer')['revenue'].sum().idxmax()

    # Análise temporal
    monthly_revenue = df.groupby('month')['revenue'].sum()
    insights['best_month'] = monthly_revenue.idxmax()
    insights['worst_month'] = monthly_revenue.idxmin()

    # Variações
    insights['monthly_variation'] = (
        (monthly_revenue.max() - monthly_revenue.min()) / monthly_revenue.min() * 100)

    return insights


def create_plotly_theme():
    """
    Cria tema personalizado para gráficos Plotly

    Returns:
        dict: Configurações de tema
    """
    return {
        'layout': {
            'colorway': list(COLORS.values()),
            'font': {'family': 'Arial, sans-serif', 'size': 12},
            'title': {'font': {'size': 16, 'color': '#2c3e50'}},
            'paper_bgcolor': 'white',
            'plot_bgcolor': 'white'
        }
    }
