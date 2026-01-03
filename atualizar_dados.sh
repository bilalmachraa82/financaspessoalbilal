#!/bin/bash

echo "=== Atualização de Dados Financeiros ==="
echo ""

echo "1. Verificando se há novos CSVs..."
if [ ! -d "data/raw" ]; then
    echo "ERRO: Pasta data/raw/ não encontrada!"
    exit 1
fi

echo "2. Processando CSVs..."
python3 preparar_csvs_nov_dez.py

if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao processar CSVs"
    exit 1
fi

echo "3. Consolidando dados..."
python3 processar_novembro_dezembro_2025.py

if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao consolidar dados"
    exit 1
fi

echo ""
echo "4. Dados processados com sucesso!"
echo ""
echo "Resumo:"
python3 << 'EOF'
import pandas as pd
df = pd.read_csv('data/processed/novembro_dezembro_2025_classificado.csv')
print(f"Total de transações: {len(df)}")
print(f"Classificadas: {len(df[df['Categoria'] != 'Nao Categorizado'])}")
print(f"Por classificar: {len(df[df['Categoria'] == 'Nao Categorizado'])}")
print(f"\nDatas: {df['Date'].min()} a {df['Date'].max()}")
print(f"Bancos: {', '.join(df['Bank'].unique())}")
EOF

echo ""
echo "5. Para atualizar no GitHub, execute:"
echo "   git add data/"
echo "   git commit -m 'Atualização de dados'"
echo "   git push"
echo ""
echo "Para abrir o dashboard:"
echo "   streamlit run dashboard_validacao_novembro_dezembro.py"
