from utils import load_data, calculate_kpis, get_top_performers, format_currency, format_percentage, generate_insights
from config import DASHBOARD_CONFIG, DATA_DIR, COLORS
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent))


# Configuração da página
st.set_page_config(
    page_title=DASHBOARD_CONFIG["title"],
    page_icon=DASHBOARD_CONFIG["page_icon"],
    layout=DASHBOARD_CONFIG["layout"],
    initial_sidebar_state=DASHBOARD_CONFIG["initial_sidebar_state"]
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Função para carregar dados


@st.cache_data
def load_sales_data():
    return load_data(DATA_DIR / "sales_data.csv")


# Carregar dados
try:
    df = load_sales_data()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# Sidebar para filtros
st.sidebar.header("🔍 Filtros de Análise")

# Filtro de data
date_range = st.sidebar.date_input(
    "📅 Período de Análise",
    value=(df['order_date'].min(), df['order_date'].max()),
    min_value=df['order_date'].min(),
    max_value=df['order_date'].max()
)

# Filtro de região
regions = st.sidebar.multiselect(
    "🌎 Regiões",
    options=sorted(df['region'].unique()),
    default=sorted(df['region'].unique())
)

# Filtro de categoria
categories = st.sidebar.multiselect(
    "📊 Categorias",
    options=sorted(df['category'].unique()),
    default=sorted(df['category'].unique())
)

# Aplicar filtros
if len(date_range) == 2:
    df_filtered = df[
        (df['order_date'] >= pd.to_datetime(date_range[0])) &
        (df['order_date'] <= pd.to_datetime(date_range[1])) &
        (df['region'].isin(regions)) &
        (df['category'].isin(categories))
    ]
else:
    df_filtered = df[
        (df['region'].isin(regions)) &
        (df['category'].isin(categories))
    ]

# Verificar se há dados após filtros
if df_filtered.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros aplicados.")
    st.stop()

# Título principal
st.markdown('<h1 class="main-header">📊 Dashboard de Análise de Vendas</h1>',
            unsafe_allow_html=True)
st.markdown("---")

# Calcular KPIs
kpis = calculate_kpis(df_filtered)

# Seção de KPIs
st.subheader("📈 Indicadores Principais")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="💰 Receita Total",
        value=format_currency(kpis['total_revenue']),
        delta=f"{kpis['total_orders']} pedidos"
    )

with col2:
    st.metric(
        label="📈 Lucro Total",
        value=format_currency(kpis['total_profit']),
        delta=format_percentage(kpis['avg_margin'])
    )

with col3:
    st.metric(
        label="🎯 Ticket Médio",
        value=format_currency(kpis['avg_ticket'])
    )

with col4:
    st.metric(
        label="👥 Clientes",
        value=f"{kpis['unique_customers']:,}",
        delta=f"{kpis['total_orders']} pedidos"
    )

with col5:
    st.metric(
        label="📦 Produtos",
        value=f"{kpis['unique_products']:,}",
        delta=f"{kpis['avg_quantity']:.1f} qtd média"
    )

st.markdown("---")

# Seção de gráficos principais
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Performance por Categoria")
    category_revenue = get_top_performers(df_filtered, 'category', 'revenue')

    fig_category = px.bar(
        x=category_revenue.values,
        y=category_revenue.index,
        orientation='h',
        title="Receita por Categoria",
        labels={'x': 'Receita (R$)', 'y': 'Categoria'},
        color=category_revenue.values,
        color_continuous_scale='viridis'
    )
    fig_category.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_category, width='stretch')

with col2:
    st.subheader("🌎 Análise Regional")
    region_stats = df_filtered.groupby('region').agg({
        'revenue': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    }).reset_index()

    fig_region = px.scatter(
        region_stats,
        x='revenue',
        y='profit',
        size='order_id',
        color='region',
        title="Receita vs Lucro por Região",
        labels={
            'revenue': 'Receita (R$)', 'profit': 'Lucro (R$)', 'order_id': 'Nº Pedidos'},
        hover_data=['order_id']
    )
    fig_region.update_layout(height=400)
    st.plotly_chart(fig_region, width='stretch')

# Análise temporal
st.subheader("📈 Evolução Temporal")
monthly_data = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M')).agg({
    'revenue': 'sum',
    'profit': 'sum',
    'order_id': 'count'
}).reset_index()
monthly_data['order_date'] = monthly_data['order_date'].astype(str)
monthly_data['margin'] = (monthly_data['profit'] /
                          monthly_data['revenue'] * 100).fillna(0)

fig_temporal = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Receita Mensal', 'Lucro Mensal',
                    'Pedidos Mensais', 'Margem Mensal'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}]]
)

# Adicionar traces
fig_temporal.add_trace(
    go.Scatter(x=monthly_data['order_date'], y=monthly_data['revenue'],
               mode='lines+markers', name='Receita', line=dict(color=COLORS['primary'])),
    row=1, col=1
)

fig_temporal.add_trace(
    go.Scatter(x=monthly_data['order_date'], y=monthly_data['profit'],
               mode='lines+markers', name='Lucro', line=dict(color=COLORS['success'])),
    row=1, col=2
)

fig_temporal.add_trace(
    go.Bar(x=monthly_data['order_date'], y=monthly_data['order_id'],
           name='Pedidos', marker_color=COLORS['info']),
    row=2, col=1
)

fig_temporal.add_trace(
    go.Scatter(x=monthly_data['order_date'], y=monthly_data['margin'],
               mode='lines+markers', name='Margem %', line=dict(color=COLORS['warning'])),
    row=2, col=2
)

fig_temporal.update_layout(height=600, showlegend=False)
st.plotly_chart(fig_temporal, width='stretch')

# Seção de rankings
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Produtos")
    top_products = get_top_performers(df_filtered, 'product', 'revenue', 10)
    top_products_df = pd.DataFrame({
        'Produto': top_products.index,
        'Receita': [format_currency(x) for x in top_products.values]
    })
    st.dataframe(top_products_df, width='stretch', hide_index=True)

with col2:
    st.subheader("👥 Top 10 Clientes")
    top_customers = get_top_performers(df_filtered, 'customer', 'revenue', 10)
    top_customers_df = pd.DataFrame({
        'Cliente': top_customers.index,
        'Receita': [format_currency(x) for x in top_customers.values]
    })
    st.dataframe(top_customers_df, width='stretch', hide_index=True)

# Insights automáticos
st.markdown("---")
st.subheader("💡 Insights Automáticos")

insights = generate_insights(df_filtered)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="insight-box">
    <h4>🎯 Destaques de Performance</h4>
    <ul>
    <li><strong>Categoria Líder:</strong> {insights['best_category']}</li>
    <li><strong>Região Destaque:</strong> {insights['best_region']}</li>
    <li><strong>Produto Top:</strong> {insights['best_product']}</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="insight-box">
    <h4>📊 Análise Temporal</h4>
    <ul>
    <li><strong>Melhor Mês:</strong> {insights['best_month']}</li>
    <li><strong>Pior Mês:</strong> {insights['worst_month']}</li>
    <li><strong>Variação Mensal:</strong> {insights['monthly_variation']:.1f}%</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Recomendações
st.subheader("🚀 Recomendações Estratégicas")
st.markdown(f"""
1. **🎯 Foco na Categoria Líder**: Investir mais recursos em {insights['best_category']}
2. **🌎 Expansão Regional**: Replicar estratégias da região {insights['best_region']} em outras áreas
3. **👥 Programa de Fidelidade**: Criar programa especial para top clientes
4. **📦 Gestão de Estoque**: Aumentar estoque de {insights['best_product']}
5. **📊 Análise Sazonal**: Aproveitar picos do mês {insights['best_month']}
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
📊 Dashboard desenvolvido com Streamlit | Dados atualizados automaticamente
</div>
""", unsafe_allow_html=True)
