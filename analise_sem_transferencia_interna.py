import pandas as pd

processed_file = '/Users/bilal/Programaçao/financas pessoais/data/processed/novembro_dezembro_2025_classificado.csv'
df = pd.read_csv(processed_file)

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

transferencias = df[df['Categoria'] == 'Transferência Interna'].sort_values('Date')

print("=" * 80)
print("LISTA DE TODAS AS TRANSFERÊNCIAS INTERNAS")
print("=" * 80)
print()

for idx, row in transferencias.iterrows():
    tipo = "SAÍDA" if row['Debit'] > 0 else "ENTRADA"
    valor = row['Debit'] if row['Debit'] > 0 else row['Credit']
    print(f"Data: {row['Date'].strftime('%Y-%m-%d')}")
    print(f"Descrição: {row['Description']}")
    print(f"Tipo: {tipo}")
    print(f"Valor: €{valor:.2f}")
    print("-" * 80)

print()
print("=" * 80)
print("TOTAL DE TRANSFERÊNCIAS INTERNAS")
print("=" * 80)
total_saida = transferencias['Debit'].sum()
total_entrada = transferencias['Credit'].sum()
print(f"Total Saídas: €{total_saida:.2f}")
print(f"Total Entradas: €{total_entrada:.2f}")
print(f"Líquido: €{total_entrada - total_saida:.2f}")
print()

df_sem_transferencias = df[df['Categoria'] != 'Transferência Interna']

df_novembro = df_sem_transferencias[df_sem_transferencias['Date'].dt.month == 11]
df_dezembro = df_sem_transferencias[df_sem_transferencias['Date'].dt.month == 12]

total_novembro_debit = df_novembro['Debit'].sum()
total_novembro_credit = df_novembro['Credit'].sum()
saldo_novembro = total_novembro_credit - total_novembro_debit

total_dezembro_debit = df_dezembro['Debit'].sum()
total_dezembro_credit = df_dezembro['Credit'].sum()
saldo_dezembro = total_dezembro_credit - total_dezembro_debit

total_geral_debit = df_sem_transferencias['Debit'].sum()
total_geral_credit = df_sem_transferencias['Credit'].sum()
saldo_geral = total_geral_credit - total_geral_debit

print("=" * 80)
print("TOTAIS SEM TRANSFERÊNCIAS INTERNAS")
print("=" * 80)
print()
print("NOVEMBRO 2025:")
print(f"  Despesas: €{total_novembro_debit:.2f}")
print(f"  Receitas: €{total_novembro_credit:.2f}")
print(f"  Saldo: €{saldo_novembro:.2f}")
print()
print("DEZEMBRO 2025:")
print(f"  Despesas: €{total_dezembro_debit:.2f}")
print(f"  Receitas: €{total_dezembro_credit:.2f}")
print(f"  Saldo: €{saldo_dezembro:.2f}")
print()
print("TOTAL GERAL (Nov + Dez):")
print(f"  Despesas: €{total_geral_debit:.2f}")
print(f"  Receitas: €{total_geral_credit:.2f}")
print(f"  Saldo: €{saldo_geral:.2f}")
print()
print("=" * 80)
print("COMPARAÇÃO")
print("=" * 80)
print(f"Com Transferência Interna:")
print(f"  Saldo Novembro: -€473.82")
print(f"  Saldo Dezembro: -€553.05")
print(f"  Saldo Total: -€1,026.87")
print()
print(f"Sem Transferência Interna:")
print(f"  Saldo Novembro: €{saldo_novembro:.2f}")
print(f"  Saldo Dezembro: €{saldo_dezembro:.2f}")
print(f"  Saldo Total: €{saldo_geral:.2f}")
print()
print(f"Diferença causada por Transferência Interna:")
print(f"  Novembro: €{-473.82 - saldo_novembro:.2f}")
print(f"  Dezembro: €{-553.05 - saldo_dezembro:.2f}")
print(f"  Total: €{-1026.87 - saldo_geral:.2f}")
