# 📊 Dashboard de Análise de Vendas

## 🎯 Descrição do Projeto

Este projeto implementa um **Dashboard Interativo de Análise de Vendas** utilizando Python, focado em transformar dados brutos de vendas em insights acionáveis para tomada de decisão comercial.

### 🚀 Objetivo

Construir uma solução completa de análise de dados que responda às principais perguntas de negócio:

- Quais produtos vendem mais?
- Qual período gera mais lucro?
- Quais regiões performam melhor?
- Onde existem oportunidades de melhoria?

## 🛠️ Tecnologias Utilizadas

| Tecnologia           | Uso                            |
| -------------------- | ------------------------------ |
| **Python 3.11**      | Linguagem principal            |
| **Pandas**           | Manipulação e análise de dados |
| **NumPy**            | Computação numérica            |
| **Matplotlib**       | Visualizações estáticas        |
| **Seaborn**          | Visualizações estatísticas     |
| **Plotly**           | Gráficos interativos           |
| **Streamlit**        | Dashboard web interativo       |
| **Jupyter Notebook** | Análise exploratória           |

## 📊 Dataset

### Estrutura dos Dados

- **Registros**: 1.000 transações
- **Período**: Janeiro 2025 - Janeiro 2026
- **Colunas**: 10 variáveis principais

| Coluna       | Tipo   | Descrição            |
| ------------ | ------ | -------------------- |
| `order_id`   | string | ID único do pedido   |
| `order_date` | date   | Data da venda        |
| `customer`   | string | Nome do cliente      |
| `product`    | string | Nome do produto      |
| `category`   | string | Categoria do produto |
| `region`     | string | Região da venda      |
| `quantity`   | int    | Quantidade vendida   |
| `price`      | float  | Preço unitário       |
| `revenue`    | float  | Receita total        |
| `profit`     | float  | Lucro obtido         |

### Características

- ✅ Dados temporais para análise de tendências
- ✅ Dados categóricos para segmentação
- ✅ Métricas financeiras calculadas
- ✅ Distribuição geográfica (5 regiões)
- ✅ 20 produtos em 13 categorias

## 🚀 Como Executar

### 1. Pré-requisitos

```bash
Python 3.11+
pip (gerenciador de pacotes)
```

### 2. Instalação

```bash
# Clonar o repositório
git clone <url-do-repositorio>
cd analise-vendas

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## 🚀 Como Executar

### 1. Pré-requisitos

```bash
Python 3.11+
pip (gerenciador de pacotes)
```

### 2. Instalação

```bash
# Clonar o repositório
git clone <url-do-repositorio>
cd analise-vendas

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Executar Projeto

```bash
# Dashboard Streamlit (Principal)
streamlit run src/dashboard.py

# Análise Exploratória (Jupyter)
jupyter notebook notebooks/analise_vendas_completa.ipynb

# Testes Automatizados
set PYTHONPATH=src && python -m pytest tests/ -v
```

### 4. Acessar Dashboard

- **URL**: http://localhost:8501
- **Interface**: Web interativa com filtros e gráficos
- **Funcionalidades**: KPIs, análise temporal, rankings e insights

## 📈 Principais Resultados

### 💰 KPIs Principais

- **Receita Total**: R$ 4.049.199,70
- **Lucro Total**: R$ 835.355,30
- **Margem Média**: 20,6%
- **Ticket Médio**: R$ 4.049,20
- **Total de Pedidos**: 1.000

### 🏆 Top Performers

- **Categoria Líder**: Celulares (R$ 1.185.221,73)
- **Produto Top**: Smartphone iPhone
- **Região Destaque**: Sul (R$ 851.596,48)
- **Cliente VIP**: Carlos Ferreira (R$ 303.674,82)

### 📊 Insights Principais

1. **Sazonalidade**: Variação de 15% entre melhor e pior mês
2. **Concentração**: Top 3 categorias representam 60% da receita
3. **Regionalização**: Sul e Norte lideram em performance
4. **Fidelização**: 20 clientes únicos com alta recorrência

## 🎨 Visualizações

### Dashboard Interativo

- 📊 KPIs em tempo real
- 📈 Gráficos temporais
- 🌎 Análise geográfica
- 🔍 Filtros dinâmicos
- 📱 Interface responsiva

### Análise Exploratória

- 📊 Distribuições estatísticas
- 📈 Correlações entre variáveis
- 🎯 Segmentação de clientes
- 📉 Análise de tendências

## 📁 Estrutura do Projeto

```
analise-vendas/
│
├── 📊 data/                          # Dados do projeto
│   └── sales_data.csv               # Dataset principal (1.000 registros)
│
├── 📓 notebooks/                     # Análise exploratória
│   └── analise_vendas_completa.ipynb # Notebook completo com insights
│
├── 🔧 src/                          # Código fonte modular
│   ├── __init__.py                  # Pacote Python
│   ├── dashboard.py                 # Dashboard Streamlit principal
│   ├── utils.py                     # Funções utilitárias
│   ├── config.py                    # Configurações do projeto
│   └── generate_dataset.py          # Gerador de dados sintéticos
│
├── 🧪 tests/                        # Testes automatizados
│   └── test_utils.py               # Suite de testes (5 testes)
│
├── 📖 docs/                         # Documentação técnica
│   └── TECHNICAL_DOCUMENTATION.md  # Documentação completa
│
├── 📋 README.md                     # Este arquivo
└── 📋 requirements.txt              # Dependências do projeto
```

## 🔍 Funcionalidades

### Análise Exploratória (Jupyter)

- [x] Limpeza e tratamento de dados
- [x] Estatísticas descritivas
- [x] Análise temporal
- [x] Segmentação por categoria/região
- [x] Identificação de padrões
- [x] Insights automáticos

### Dashboard Interativo (Streamlit)

- [x] KPIs em tempo real
- [x] Filtros dinâmicos (data, região, categoria)
- [x] Gráficos interativos (Plotly)
- [x] Tabelas de ranking (produtos e clientes)
- [x] Insights automáticos
- [x] Interface responsiva e profissional

## 🎯 Próximas Melhorias

### Básico

- [ ] Exportação de relatórios (PDF/Excel)
- [ ] Mais filtros avançados
- [ ] Alertas automáticos

### Intermediário

- [ ] Previsão de vendas (Machine Learning)
- [ ] Segmentação de clientes (K-Means)
- [ ] Análise de coorte
- [ ] Detecção de anomalias

### Avançado

- [ ] Deploy na nuvem (Heroku/AWS)
- [ ] Integração com APIs
- [ ] Atualização automática de dados
- [ ] Sistema de notificações

## 📚 Conceitos Aplicados

- **ETL**: Extração, transformação e carregamento de dados
- **EDA**: Análise exploratória de dados
- **KPIs**: Indicadores-chave de performance
- **Data Visualization**: Visualização de dados
- **Business Intelligence**: Inteligência de negócios
- **Statistical Analysis**: Análise estatística

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Seu Nome**

- LinkedIn: [seu-linkedin]
- GitHub: [seu-github]
- Email: [seu-email]

---

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐
