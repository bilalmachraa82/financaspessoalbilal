import pandas as pd

df = pd.read_csv('/Users/bilal/Programaçao/financas pessoais/data/processed/novembro_dezembro_2025_classificado.csv')

df['Date'] = pd.to_datetime(df['Date'])

df_novembro = df[df['Date'].dt.month == 11]
df_dezembro = df[df['Date'].dt.month == 12]

def analisar_receitas(df, mes):
    print(f"\n{'='*80}")
    print(f"ANÁLISE DE RECEITAS - {mes.upper()}")
    print(f"{'='*80}")
    
    receitas = df[df['Credit'] > 0].copy()
    
    print(f"\nTotal de transações de crédito: {len(receitas)}")
    print(f"Total recebido: {receitas['Credit'].sum():.2f}€")
    
    print(f"\n{'='*80}")
    print("RECEITAS POR CATEGORIA")
    print(f"{'='*80}")
    
    receitas_por_categoria = receitas.groupby('Categoria').agg({
        'Credit': 'sum',
        'Description': 'count'
    }).rename(columns={'Credit': 'Total', 'Description': 'Nº Transações'})
    
    receitas_por_categoria = receitas_por_categoria.sort_values('Total', ascending=False)
    
    for categoria, row in receitas_por_categoria.iterrows():
        print(f"{categoria:50} {row['Total']:>10.2f}€ ({row['Nº Transações']:>2} transações)")
    
    print(f"\n{'='*80}")
    print("DETALHE DE TODAS AS RECEITAS")
    print(f"{'='*80}")
    
    receitas_sorted = receitas.sort_values('Date', ascending=True)
    
    for _, row in receitas_sorted.iterrows():
        print(f"{row['Date'].strftime('%Y-%m-%d')} | {row['Bank']:10} | {row['Credit']:>8.2f}€ | {row['Categoria']:50} | {row['Description']}")
    
    print(f"\n{'='*80}")
    print("ANÁLISE DE TRANSFERÊNCIAS INTERNAS (podem ser movimentos entre contas)")
    print(f"{'='*80}")
    
    transferencias = receitas[receitas['Categoria'] == 'Transferência Interna']
    
    if len(transferencias) > 0:
        print(f"\nTotal em transferências internas: {transferencias['Credit'].sum():.2f}€")
        print(f"Nº de transferências: {len(transferencias)}\n")
        
        for _, row in transferencias.iterrows():
            print(f"{row['Date'].strftime('%Y-%m-%d')} | {row['Bank']:10} | {row['Credit']:>8.2f}€ | {row['Description']}")
    else:
        print("\nNenhuma transferência interna encontrada.")
    
    return receitas_por_categoria

receitas_novembro = analisar_receitas(df_novembro, 'Novembro')
receitas_dezembro = analisar_receitas(df_dezembro, 'Dezembro')

print(f"\n{'='*80}")
print("RESUMO FINAL")
print(f"{'='*80}")
print(f"\nNovembro:")
print(f"  - Total Receitas: {df_novembro['Credit'].sum():.2f}€")
print(f"  - Total Despesas: {df_novembro['Debit'].sum():.2f}€")
print(f"  - Saldo: {(df_novembro['Credit'].sum() - df_novembro['Debit'].sum()):.2f}€")

print(f"\nDezembro:")
print(f"  - Total Receitas: {df_dezembro['Credit'].sum():.2f}€")
print(f"  - Total Despesas: {df_dezembro['Debit'].sum():.2f}€")
print(f"  - Saldo: {(df_dezembro['Credit'].sum() - df_dezembro['Debit'].sum()):.2f}€")

print(f"\nTotal Novembro + Dezembro:")
print(f"  - Total Receitas: {(df_novembro['Credit'].sum() + df_dezembro['Credit'].sum()):.2f}€")
print(f"  - Total Despesas: {(df_novembro['Debit'].sum() + df_dezembro['Debit'].sum()):.2f}€")
print(f"  - Saldo: {((df_novembro['Credit'].sum() + df_dezembro['Credit'].sum()) - (df_novembro['Debit'].sum() + df_dezembro['Debit'].sum())):.2f}€")
