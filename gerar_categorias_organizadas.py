import pandas as pd

processed_file = '/Users/bilal/Programaçao/financas pessoais/data/processed/novembro_dezembro_2025_classificado.csv'
df = pd.read_csv(processed_file)

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

df_sem_transferencias = df[df['Categoria'] != 'Transferência Interna']

ordem_categorias_excel = [
    'Casa - Renda Fontanelas',
    'Casa - Renda Monte da Caparica',
    'Casa - Supermercado Bilal',
    'Casa - Supermercado Daniela',
    'Casa - Luz',
    'Casa - Internet (Net)',
    'Casa - Limpeza',
    'Casa - Outros',
    'Pessoal Bilal - Comer fora',
    'Pessoal Bilal - Vestuário/calçado',
    'Pessoal Bilal - Férias/viagens/Passeios',
    'Pessoal Bilal - Livros/Cinema/Concertos',
    'Pessoal Bilal - Donativos/Quotas',
    'Pessoal Bilal - Barbeiro',
    'Pessoal Bilal - Presentes',
    'Pessoal Bilal - Outros',
    'Créditos/Seguros Bilal - Pessoal Millennium',
    'Créditos/Seguros Bilal - Wizink',
    'Créditos/Seguros Bilal - Seg vida',
    'Créditos/Seguros Bilal - Cliente frequente',
    'Créditos/Seguros Bilal - Despesas bancárias Bilal',
    'Créditos/Seguros Bilal - Despesas Bancárias Bilal',
    'Deslocações Bilal - Transportes',
    'Deslocações Bilal - Via Verde',
    'Deslocações Bilal - Carro',
    'Deslocações Bilal - Combustível',
    'Deslocações Bilal - Estacionamento',
    'Deslocações Bilal - ACP',
    'Saúde - Consultas Bilal',
    'Saúde - Consultas Daniela',
    'Saúde - Farmácia/Prod.Nat./Exames',
    'Saúde - Pruvit',
    'Saúde - Ginásio',
    'Saúde - Lifewave',
    'Noah - Pensão de Alimentos',
    'Noah - Pensão de alimentos',
    'Noah - Desporto',
    'Noah - Consultas',
    'Noah - Roupa',
    'Noah - Outros',
    'Despesas Profissionais Bilal - Mensalidades (Replit, GPT, etc.)',
    'Despesas Profissionais Bilal - Mensalidade (Replit, GPT, etc.)',
    'Despesas Profissionais Bilal - Formação Bilal',
    'Despesas Profissionais Bilal - Seg. Social Bilal',
    'Despesas Profissionais Bilal - Produtos (Lifewave/Pruvit, etc.)',
    'Despesas Profissionais Bilal - Marketing digital',
    'Despesas Profissionais Bilal - BNI',
    'Receitas - Sessões Bilal',
    'Receitas - Limpezas Espaços',
    'Receitas - Workshop TMD',
    'Receitas - Aulas Individuais',
    'Receitas - Soluções IA',
    'Receitas - Lifewave',
    'Receitas - Pruvit',
    'Receitas - Rendas Fontanelas',
    'Receitas - Electricidade Fontanelas',
    'Receitas - Renda Monte da Caparica',
    'Despesas de Crédito',
    'Pessoal Bilal - Transferências',
    'Estorno/Devolução'
]

df_novembro = df_sem_transferencias[df_sem_transferencias['Date'].dt.month == 11]
df_dezembro = df_sem_transferencias[df_sem_transferencias['Date'].dt.month == 12]

def gerar_resumo(df, nome_mes, arquivo_saida):
    resumo = []
    total_debit = 0
    total_credit = 0
    
    categorias_usadas = set(df['Categoria'].unique())
    
    for cat in ordem_categorias_excel:
        df_cat = df[df['Categoria'] == cat]
        if len(df_cat) > 0:
            debit = df_cat['Debit'].sum()
            credit = df_cat['Credit'].sum()
            total_debit += debit
            total_credit += credit
            resumo.append({'Categoria': cat, 'Debit': debit, 'Credit': credit})
    
    resumo_df = pd.DataFrame(resumo)
    
    total_row = pd.DataFrame([{
        'Categoria': 'TOTAL',
        'Debit': total_debit,
        'Credit': total_credit
    }])
    
    resumo_df = pd.concat([resumo_df, total_row], ignore_index=True)
    
    resumo_df.to_csv(arquivo_saida, index=False)
    
    print(f"\n{'='*80}")
    print(f"{nome_mes} 2025 - SEM TRANSFERÊNCIAS INTERNAS")
    print(f"{'='*80}")
    print(f"Total Despesas: €{total_debit:.2f}")
    print(f"Total Receitas: €{total_credit:.2f}")
    print(f"Saldo: €{total_credit - total_debit:.2f}")
    print(f"\n✅ Ficheiro gerado: {arquivo_saida}")

gerar_resumo(
    df_novembro, 
    'NOVEMBRO', 
    '/Users/bilal/Programaçao/financas pessoais/categorias_novembro_2025_organizadas.csv'
)

gerar_resumo(
    df_dezembro, 
    'DEZEMBRO', 
    '/Users/bilal/Programaçao/financas pessoais/categorias_dezembro_2025_organizadas.csv'
)

print(f"\n{'='*80}")
print("RESUMO COMPARATIVO")
print(f"{'='*80}")

total_novembro_debit = df_novembro['Debit'].sum()
total_novembro_credit = df_novembro['Credit'].sum()
total_dezembro_debit = df_dezembro['Debit'].sum()
total_dezembro_credit = df_dezembro['Credit'].sum()

print(f"Novembro:")
print(f"  Despesas: €{total_novembro_debit:.2f}")
print(f"  Receitas: €{total_novembro_credit:.2f}")
print(f"  Saldo: €{total_novembro_credit - total_novembro_debit:.2f}")
print()
print(f"Dezembro:")
print(f"  Despesas: €{total_dezembro_debit:.2f}")
print(f"  Receitas: €{total_dezembro_credit:.2f}")
print(f"  Saldo: €{total_dezembro_credit - total_dezembro_debit:.2f}")
print()

total_geral_debit = total_novembro_debit + total_dezembro_debit
total_geral_credit = total_novembro_credit + total_dezembro_credit

print(f"TOTAL (Nov + Dez):")
print(f"  Despesas: €{total_geral_debit:.2f}")
print(f"  Receitas: €{total_geral_credit:.2f}")
print(f"  Saldo: €{total_geral_credit - total_geral_debit:.2f}")
