# 📋 Documentação Técnica - Dashboard de Análise de Vendas

## 🏗️ Arquitetura do Sistema

### Componentes Principais

#### 1. **Módulo de Configuração (`config.py`)**

- Centraliza configurações do projeto
- Define caminhos, cores, métricas e parâmetros

#### 2. **Módulo de Utilitários (`utils.py`)**

- Funções para carregamento e preparação de dados
- Cálculos de KPIs e métricas de negócio
- Formatação e transformação de dados

#### 3. **Dashboard Principal (`dashboard.py`)**

- Interface web interativa com Streamlit
- Visualizações dinâmicas com Plotly
- Filtros e controles de usuário

## 📊 Estrutura de Dados

### Schema do Dataset

```python
{
    'order_id': str,      # Identificador único
    'order_date': date,   # Data da transação
    'customer': str,      # Nome do cliente
    'product': str,       # Nome do produto
    'category': str,      # Categoria do produto
    'region': str,        # Região da venda
    'quantity': int,      # Quantidade vendida
    'price': float,       # Preço unitário
    'revenue': float,     # Receita total
    'profit': float       # Lucro obtido
}
```

## 🔄 Fluxo de Dados

1. **Carregamento**: `load_data(file_path)`
2. **Preparação**: `prepare_data(df)`
3. **Análise**: `calculate_kpis(df_clean)`
4. **Visualização**: `create_visualization(df_clean)`

## 🧪 Testes

### Execução

```bash
set PYTHONPATH=src && python -m pytest tests/ -v
```

## 🚀 Deploy e Execução

### Ambiente Local

```bash
streamlit run src/dashboard.py
jupyter notebook notebooks/
```

## 🔧 Configuração

### Personalização de Cores

```python
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c"
}
```
