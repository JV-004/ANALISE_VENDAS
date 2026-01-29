"""
Testes para as funções utilitárias
"""

from utils import prepare_data, calculate_kpis, get_top_performers, format_currency, format_percentage
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent / "src"))


class TestUtils:

    @pytest.fixture
    def sample_data(self):
        """Dados de exemplo para testes"""
        data = {
            'order_id': ['ORD-001', 'ORD-002', 'ORD-003'],
            'order_date': ['2025-01-01', '2025-01-02', '2025-01-03'],
            'customer': ['Cliente A', 'Cliente B', 'Cliente A'],
            'product': ['Produto X', 'Produto Y', 'Produto X'],
            'category': ['Cat A', 'Cat B', 'Cat A'],
            'region': ['Norte', 'Sul', 'Norte'],
            'quantity': [2, 1, 3],
            'price': [100.0, 200.0, 100.0],
            'revenue': [200.0, 200.0, 300.0],
            'profit': [40.0, 50.0, 60.0]
        }
        return pd.DataFrame(data)

    def test_prepare_data(self, sample_data):
        """Testa a preparação dos dados"""
        df_prepared = prepare_data(sample_data)

        # Verificar se as colunas foram criadas
        expected_columns = ['year', 'month', 'day_of_week',
                            'quarter', 'margin', 'revenue_per_unit', 'ticket_category']
        for col in expected_columns:
            assert col in df_prepared.columns

        # Verificar se order_date foi convertido para datetime
        assert pd.api.types.is_datetime64_any_dtype(df_prepared['order_date'])

        # Verificar se margin foi calculado corretamente
        expected_margin = (
            df_prepared['profit'] / df_prepared['revenue']).rename('margin')
        pd.testing.assert_series_equal(df_prepared['margin'], expected_margin)

    def test_calculate_kpis(self, sample_data):
        """Testa o cálculo de KPIs"""
        df_prepared = prepare_data(sample_data)
        kpis = calculate_kpis(df_prepared)

        # Verificar se todos os KPIs estão presentes
        expected_kpis = ['total_revenue', 'total_profit', 'avg_ticket', 'total_orders',
                         'unique_customers', 'unique_products', 'avg_margin', 'avg_quantity']
        for kpi in expected_kpis:
            assert kpi in kpis

        # Verificar valores específicos
        assert kpis['total_revenue'] == 700.0
        assert kpis['total_profit'] == 150.0
        assert kpis['total_orders'] == 3
        assert kpis['unique_customers'] == 2
        assert kpis['unique_products'] == 2

    def test_get_top_performers(self, sample_data):
        """Testa a função de top performers"""
        df_prepared = prepare_data(sample_data)
        top_customers = get_top_performers(
            df_prepared, 'customer', 'revenue', 2)

        # Verificar se retorna o número correto de itens
        assert len(top_customers) == 2

        # Verificar se está ordenado corretamente
        assert top_customers.iloc[0] >= top_customers.iloc[1]

    def test_format_currency(self):
        """Testa a formatação de moeda"""
        assert format_currency(1000.50) == "R$ 1.000,50"
        assert format_currency(1234567.89) == "R$ 1.234.567,89"

    def test_format_percentage(self):
        """Testa a formatação de percentual"""
        assert format_percentage(25.5) == "25.5%"
        assert format_percentage(100.0) == "100.0%"


if __name__ == "__main__":
    pytest.main([__file__])
