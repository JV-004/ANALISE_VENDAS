from utils import load_data, calculate_kpis, get_top_performers, format_currency, format_percentage, generate_insights
from config import DASHBOARD_CONFIG, DATA_DIR, COLORS
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import io
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

sys.path.append(str(Path(__file__).parent))

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Análise de Vendas",
    page_icon="📊",
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .insight-box h4 {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .insight-box ul { list-style: none; padding: 0; }
    .insight-box li {
        background: rgba(255,255,255,0.1);
        margin: 0.5rem 0;
        padding: 0.8rem;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .insight-box strong { color: #FFD700; font-weight: bold; }
    .insight-performance { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
    .insight-temporal { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .recommendations-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #333;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .recommendations-box h3 { color: #d63384; font-size: 1.4rem; font-weight: bold; margin-bottom: 1rem; }
    .recommendations-box ol { font-size: 1.1rem; line-height: 1.8; }
    .recommendations-box li {
        margin: 0.8rem 0;
        padding: 0.5rem;
        background: rgba(255,255,255,0.3);
        border-radius: 8px;
        font-weight: 500;
    }
    .alert-danger {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;
        font-weight: bold; font-size: 1rem;
    }
    .alert-warning {
        background: linear-gradient(135deg, #f9ca24 0%, #f0932b 100%);
        color: #333; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;
        font-weight: bold; font-size: 1rem;
    }
    .alert-success {
        background: linear-gradient(135deg, #6ab04c 0%, #badc58 100%);
        color: #333; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;
        font-weight: bold; font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_sales_data():
    return load_data(DATA_DIR / "sales_data.csv")


def export_excel(df):
    """Exporta dataframe para Excel em memória."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
    return output.getvalue()


def generate_alerts(df, kpis):
    """Gera alertas automáticos baseados nos dados."""
    alerts = []

    # Alerta de margem baixa
    if kpis['avg_margin'] < 15:
        alerts.append(
            ("danger", f"⚠️ Margem média crítica: {kpis['avg_margin']:.1f}% (abaixo de 15%)"))
    elif kpis['avg_margin'] < 20:
        alerts.append(
            ("warning", f"⚡ Margem média baixa: {kpis['avg_margin']:.1f}% (abaixo de 20%)"))
    else:
        alerts.append(
            ("success", f"✅ Margem média saudável: {kpis['avg_margin']:.1f}%"))

    # Alerta de concentração de receita
    top3_revenue = df.groupby('category')['revenue'].sum().nlargest(3).sum()
    total_revenue = df['revenue'].sum()
    concentration = (top3_revenue / total_revenue *
                     100) if total_revenue > 0 else 0
    if concentration > 70:
        alerts.append(
            ("danger", f"⚠️ Alta concentração: Top 3 categorias = {concentration:.1f}% da receita"))
    elif concentration > 55:
        alerts.append(
            ("warning", f"⚡ Concentração moderada: Top 3 categorias = {concentration:.1f}% da receita"))

    # Alerta de ticket médio
    if kpis['avg_ticket'] < 2000:
        alerts.append(
            ("warning", f"⚡ Ticket médio baixo: {format_currency(kpis['avg_ticket'])}"))
    else:
        alerts.append(
            ("success", f"✅ Ticket médio saudável: {format_currency(kpis['avg_ticket'])}"))

    # Alerta de volume de pedidos
    if kpis['total_orders'] < 50:
        alerts.append(
            ("danger", f"⚠️ Volume de pedidos baixo no período: {kpis['total_orders']} pedidos"))

    return alerts


# Carregar dados
try:
    df = load_sales_data()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
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

# ── FILTROS AVANÇADOS ─────────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Filtros Avançados")

# Filtro de produto
all_products = sorted(df['product'].unique())
selected_products = st.sidebar.multiselect(
    "📦 Produtos",
    options=all_products,
    default=all_products,
    help="Filtre por produtos específicos"
)

# Filtro de cliente
all_customers = sorted(df['customer'].unique())
selected_customers = st.sidebar.multiselect(
    "👤 Clientes",
    options=all_customers,
    default=all_customers,
    help="Filtre por clientes específicos"
)

# Filtro de faixa de receita
min_rev = float(df['revenue'].min())
max_rev = float(df['revenue'].max())
revenue_range = st.sidebar.slider(
    "💰 Faixa de Receita por Pedido (R$)",
    min_value=min_rev,
    max_value=max_rev,
    value=(min_rev, max_rev),
    format="R$ %.0f",
    help="Filtre pedidos por valor de receita"
)

# Filtro de quantidade mínima
min_qty = int(df['quantity'].min())
max_qty = int(df['quantity'].max())
qty_filter = st.sidebar.slider(
    "📦 Quantidade Mínima por Pedido",
    min_value=min_qty,
    max_value=max_qty,
    value=min_qty,
    help="Filtre pedidos com quantidade mínima"
)

# ── APLICAR FILTROS ───────────────────────────────────────────────────────────
if len(date_range) == 2:
    df_filtered = df[
        (df['order_date'] >= pd.to_datetime(date_range[0])) &
        (df['order_date'] <= pd.to_datetime(date_range[1])) &
        (df['region'].isin(regions)) &
        (df['category'].isin(categories)) &
        (df['product'].isin(selected_products)) &
        (df['customer'].isin(selected_customers)) &
        (df['revenue'] >= revenue_range[0]) &
        (df['revenue'] <= revenue_range[1]) &
        (df['quantity'] >= qty_filter)
    ]
else:
    df_filtered = df[
        (df['region'].isin(regions)) &
        (df['category'].isin(categories)) &
        (df['product'].isin(selected_products)) &
        (df['customer'].isin(selected_customers)) &
        (df['revenue'] >= revenue_range[0]) &
        (df['revenue'] <= revenue_range[1]) &
        (df['quantity'] >= qty_filter)
    ]

if df_filtered.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros aplicados.")
    st.stop()

# ── TÍTULO ────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="main-header">📊 Dashboard de Análise de Vendas</h1>',
            unsafe_allow_html=True)
st.markdown(
    f"*Exibindo **{len(df_filtered):,}** de **{len(df):,}** registros com os filtros aplicados*")
st.markdown("---")

# ── KPIs ──────────────────────────────────────────────────────────────────────
kpis = calculate_kpis(df_filtered)
st.subheader("📈 Indicadores Principais")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label="💰 Receita Total", value=format_currency(
        kpis['total_revenue']), delta=f"{kpis['total_orders']} pedidos")
with col2:
    st.metric(label="📈 Lucro Total", value=format_currency(
        kpis['total_profit']), delta=format_percentage(kpis['avg_margin']))
with col3:
    st.metric(label="🎯 Ticket Médio",
              value=format_currency(kpis['avg_ticket']))
with col4:
    st.metric(label="👥 Clientes",
              value=f"{kpis['unique_customers']:,}", delta=f"{kpis['total_orders']} pedidos")
with col5:
    st.metric(label="📦 Produtos",
              value=f"{kpis['unique_products']:,}", delta=f"{kpis['avg_quantity']:.1f} qtd média")

st.markdown("---")

# ── ALERTAS AUTOMÁTICOS ───────────────────────────────────────────────────────
st.subheader("🔔 Alertas Automáticos")
alerts = generate_alerts(df_filtered, kpis)
cols = st.columns(len(alerts))
for i, (level, msg) in enumerate(alerts):
    with cols[i]:
        st.markdown(
            f'<div class="alert-{level}">{msg}</div>', unsafe_allow_html=True)

st.markdown("---")

# ── GRÁFICOS PRINCIPAIS ───────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Performance por Categoria")
    category_revenue = get_top_performers(df_filtered, 'category', 'revenue')
    fig_category = px.bar(
        x=category_revenue.values, y=category_revenue.index, orientation='h',
        title="Receita por Categoria", labels={'x': 'Receita (R$)', 'y': 'Categoria'},
        color=category_revenue.values, color_continuous_scale='viridis'
    )
    fig_category.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_category, width='stretch')

with col2:
    st.subheader("🌎 Análise Regional")
    region_stats = df_filtered.groupby('region').agg(
        {'revenue': 'sum', 'profit': 'sum', 'order_id': 'count'}
    ).reset_index()
    fig_region = px.scatter(
        region_stats, x='revenue', y='profit', size='order_id', color='region',
        title="Receita vs Lucro por Região",
        labels={
            'revenue': 'Receita (R$)', 'profit': 'Lucro (R$)', 'order_id': 'Nº Pedidos'},
        hover_data=['order_id']
    )
    fig_region.update_layout(height=400)
    st.plotly_chart(fig_region, width='stretch')

# ── ANÁLISE TEMPORAL ──────────────────────────────────────────────────────────
st.subheader("📈 Evolução Temporal")
monthly_data = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M')).agg(
    {'revenue': 'sum', 'profit': 'sum', 'order_id': 'count'}
).reset_index()
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
fig_temporal.add_trace(go.Scatter(x=monthly_data['order_date'], y=monthly_data['revenue'],
                       mode='lines+markers', name='Receita', line=dict(color=COLORS['primary'])), row=1, col=1)
fig_temporal.add_trace(go.Scatter(x=monthly_data['order_date'], y=monthly_data['profit'],
                       mode='lines+markers', name='Lucro', line=dict(color=COLORS['success'])), row=1, col=2)
fig_temporal.add_trace(go.Bar(x=monthly_data['order_date'], y=monthly_data['order_id'],
                       name='Pedidos', marker_color=COLORS['info']), row=2, col=1)
fig_temporal.add_trace(go.Scatter(x=monthly_data['order_date'], y=monthly_data['margin'],
                       mode='lines+markers', name='Margem %', line=dict(color=COLORS['warning'])), row=2, col=2)
fig_temporal.update_layout(height=600, showlegend=False)
st.plotly_chart(fig_temporal, width='stretch')

# ── RANKINGS ──────────────────────────────────────────────────────────────────
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Produtos")
    top_products = get_top_performers(df_filtered, 'product', 'revenue', 10)
    st.dataframe(pd.DataFrame({'Produto': top_products.index, 'Receita': [
                 format_currency(x) for x in top_products.values]}), width='stretch', hide_index=True)

with col2:
    st.subheader("👥 Top 10 Clientes")
    top_customers = get_top_performers(df_filtered, 'customer', 'revenue', 10)
    st.dataframe(pd.DataFrame({'Cliente': top_customers.index, 'Receita': [
                 format_currency(x) for x in top_customers.values]}), width='stretch', hide_index=True)

# ── INSIGHTS ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<h2 style="text-align: center; color: #1f77b4; font-size: 2rem; margin-bottom: 2rem;">💡 Insights Automáticos</h2>', unsafe_allow_html=True)

insights = generate_insights(df_filtered)
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="insight-box insight-performance">
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
    <div class="insight-box insight-temporal">
    <h4>📊 Análise Temporal</h4>
    <ul>
    <li><strong>Melhor Mês:</strong> {insights['best_month']}</li>
    <li><strong>Pior Mês:</strong> {insights['worst_month']}</li>
    <li><strong>Variação Mensal:</strong> {insights['monthly_variation']:.1f}%</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ── RECOMENDAÇÕES ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div class="recommendations-box">
<h3>🚀 Recomendações Estratégicas</h3>
<ol>
<li><strong>🎯 Foco na Categoria Líder:</strong> Investir mais recursos em {insights['best_category']}</li>
<li><strong>🌎 Expansão Regional:</strong> Replicar estratégias da região {insights['best_region']} em outras áreas</li>
<li><strong>👥 Programa de Fidelidade:</strong> Criar programa especial para top clientes</li>
<li><strong>📦 Gestão de Estoque:</strong> Aumentar estoque de {insights['best_product']}</li>
<li><strong>📊 Análise Sazonal:</strong> Aproveitar picos do mês {insights['best_month']}</li>
</ol>
</div>
""", unsafe_allow_html=True)

# ── PREVISÃO DE VENDAS (ML) ───────────────────────────────────────────────────
st.markdown("---")
st.subheader("🤖 Previsão de Vendas (Machine Learning)")
st.caption("Modelo de Regressão Linear treinado com os dados históricos filtrados para prever receita futura.")

# Preparar dados mensais para treino
ml_monthly = df_filtered.groupby(df_filtered['order_date'].dt.to_period('M'))[
    'revenue'].sum().reset_index()
ml_monthly.columns = ['mes', 'receita']
ml_monthly['mes_num'] = range(len(ml_monthly))

if len(ml_monthly) >= 3:
    X = ml_monthly[['mes_num']].values
    y = ml_monthly['receita'].values

    model = LinearRegression()
    model.fit(X, y)

    # Prever os próximos 3 meses
    n_meses = len(ml_monthly)
    futuros_idx = np.array([[n_meses], [n_meses + 1], [n_meses + 2]])
    previsoes = model.predict(futuros_idx)

    # Gerar labels dos meses futuros
    ultimo_mes = ml_monthly['mes'].iloc[-1]
    meses_futuros = [(ultimo_mes + i + 1).strftime('%Y-%m') for i in range(3)]

    # Montar dataframe de previsão
    df_prev = pd.DataFrame(
        {'Mês': meses_futuros, 'Previsão de Receita': previsoes})

    # Gráfico combinado: histórico + previsão
    fig_ml = go.Figure()
    fig_ml.add_trace(go.Scatter(
        x=ml_monthly['mes'].astype(str), y=ml_monthly['receita'],
        mode='lines+markers', name='Histórico',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6)
    ))
    fig_ml.add_trace(go.Scatter(
        x=meses_futuros, y=previsoes,
        mode='lines+markers', name='Previsão',
        line=dict(color='#ff7f0e', width=2, dash='dash'),
        marker=dict(size=8, symbol='star')
    ))
    fig_ml.update_layout(
        title="Receita Histórica + Previsão para os Próximos 3 Meses",
        xaxis_title="Mês", yaxis_title="Receita (R$)",
        height=400, legend=dict(orientation='h', y=1.1)
    )
    st.plotly_chart(fig_ml, width='stretch')

    col1, col2, col3 = st.columns(3)
    for i, (col, mes, val) in enumerate(zip([col1, col2, col3], meses_futuros, previsoes)):
        with col:
            st.metric(label=f"📅 {mes}", value=format_currency(max(val, 0)))
else:
    st.info("ℹ️ São necessários pelo menos 3 meses de dados para gerar previsões. Ajuste os filtros de data.")

# ── SEGMENTAÇÃO DE CLIENTES (K-MEANS) ─────────────────────────────────────────
st.markdown("---")
st.subheader("🎯 Segmentação de Clientes (K-Means)")
st.caption("Algoritmo K-Means agrupa automaticamente os clientes por comportamento de compra: receita total, número de pedidos e ticket médio.")

# Agregar métricas por cliente
clientes_agg = df_filtered.groupby('customer').agg(
    receita_total=('revenue', 'sum'),
    num_pedidos=('order_id', 'count'),
    ticket_medio=('revenue', 'mean')
).reset_index()

if len(clientes_agg) >= 3:
    n_clusters = st.slider("Número de segmentos (clusters)", min_value=2, max_value=5, value=3,
                           help="Escolha quantos grupos de clientes deseja identificar")

    # Normalizar e aplicar K-Means
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(
        clientes_agg[['receita_total', 'num_pedidos', 'ticket_medio']])

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clientes_agg['segmento'] = kmeans.fit_predict(X_scaled).astype(str)
    clientes_agg['segmento'] = 'Segmento ' + \
        (clientes_agg['segmento'].astype(int) + 1).astype(str)

    col1, col2 = st.columns(2)

    with col1:
        fig_kmeans = px.scatter(
            clientes_agg, x='receita_total', y='num_pedidos',
            color='segmento', size='ticket_medio', hover_data=['customer'],
            title="Clientes por Segmento: Receita vs Pedidos",
            labels={'receita_total': 'Receita Total (R$)', 'num_pedidos': 'Nº de Pedidos',
                    'segmento': 'Segmento'},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_kmeans.update_layout(height=400)
        st.plotly_chart(fig_kmeans, width='stretch')

    with col2:
        # Resumo por segmento
        resumo_seg = clientes_agg.groupby('segmento').agg(
            clientes=('customer', 'count'),
            receita_media=('receita_total', 'mean'),
            pedidos_medio=('num_pedidos', 'mean'),
            ticket_medio=('ticket_medio', 'mean')
        ).reset_index()
        resumo_seg['receita_media'] = resumo_seg['receita_media'].apply(
            format_currency)
        resumo_seg['ticket_medio'] = resumo_seg['ticket_medio'].apply(
            format_currency)
        resumo_seg['pedidos_medio'] = resumo_seg['pedidos_medio'].round(1)
        resumo_seg.columns = ['Segmento', 'Clientes',
                              'Receita Média', 'Pedidos Médios', 'Ticket Médio']
        st.dataframe(resumo_seg, hide_index=True, width='stretch')

        st.markdown("**💡 Como interpretar:**")
        st.markdown("- Segmentos com alta receita e poucos pedidos → clientes de alto valor\n- Segmentos com muitos pedidos e ticket baixo → clientes frequentes\n- Segmentos com baixa receita → oportunidade de reativação")
else:
    st.info("ℹ️ São necessários pelo menos 3 clientes para realizar a segmentação.")

# ── EXPORTAÇÃO ────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📥 Exportar Relatório")
col1, col2, col3 = st.columns(3)

with col1:
    # Exportar dados filtrados em Excel
    excel_data = export_excel(df_filtered)
    st.download_button(
        label="📊 Baixar Excel (Dados Filtrados)",
        data=excel_data,
        file_name="relatorio_vendas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

with col2:
    # Exportar CSV
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Baixar CSV (Dados Filtrados)",
        data=csv_data,
        file_name="relatorio_vendas.csv",
        mime="text/csv",
        use_container_width=True
    )

with col3:
    # Exportar resumo KPIs em Excel
    kpis_df = pd.DataFrame([{
        'Métrica': 'Receita Total', 'Valor': format_currency(kpis['total_revenue'])
    }, {
        'Métrica': 'Lucro Total', 'Valor': format_currency(kpis['total_profit'])
    }, {
        'Métrica': 'Margem Média', 'Valor': format_percentage(kpis['avg_margin'])
    }, {
        'Métrica': 'Ticket Médio', 'Valor': format_currency(kpis['avg_ticket'])
    }, {
        'Métrica': 'Total de Pedidos', 'Valor': str(kpis['total_orders'])
    }, {
        'Métrica': 'Clientes Únicos', 'Valor': str(kpis['unique_customers'])
    }])
    kpis_excel = export_excel(kpis_df)
    st.download_button(
        label="📋 Baixar Resumo KPIs (Excel)",
        data=kpis_excel,
        file_name="resumo_kpis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
📊 Dashboard desenvolvido com Streamlit | Dados atualizados automaticamente
</div>
""", unsafe_allow_html=True)
