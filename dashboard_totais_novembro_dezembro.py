import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="📊 Totais Novembro/Dezembro 2025",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Totais Financeiros - Novembro/Dezembro 2025")

arquivo_dados = 'data/processed/novembro_dezembro_2025_classificado.csv'

if not Path(arquivo_dados).exists():
    st.error(f"Ficheiro não encontrado: {arquivo_dados}")
    st.stop()

df = pd.read_csv(arquivo_dados)
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

st.sidebar.header("⚙️ Opções")
incluir_transferencias = st.sidebar.checkbox(
    "Incluir Transferência Interna",
    value=False,
    help="Mostrar ou esconder transferências entre contas próprias"
)

if incluir_transferencias:
    df_filtrado = df.copy()
else:
    df_filtrado = df[df['Categoria'] != 'Transferência Interna'].copy()

df_novembro = df_filtrado[df_filtrado['Date'].dt.month == 11]
df_dezembro = df_filtrado[df_filtrado['Date'].dt.month == 12]

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
    'Estorno/Devolução',
    'Transferência Interna'
]

def criar_resumo(df, nome_mes):
    resumo = []
    total_debit = 0
    total_credit = 0
    
    for cat in ordem_categorias_excel:
        if not incluir_transferencias and cat == 'Transferência Interna':
            continue
            
        df_cat = df[df['Categoria'] == cat]
        if len(df_cat) > 0:
            debit = df_cat['Debit'].sum()
            credit = df_cat['Credit'].sum()
            total_debit += debit
            total_credit += credit
            
            saldo = credit - debit
            cor = "🟢" if saldo >= 0 else "🔴"
            
            resumo.append({
                'Categoria': cat,
                'Despesas (€)': debit,
                'Receitas (€)': credit,
                'Saldo (€)': saldo,
                'Status': cor
            })
    
    resumo_df = pd.DataFrame(resumo)
    
    total_saldo = total_credit - total_debit
    cor_total = "🟢" if total_saldo >= 0 else "🔴"
    
    total_row = pd.DataFrame([{
        'Categoria': f'TOTAL {nome_mes}',
        'Despesas (€)': total_debit,
        'Receitas (€)': total_credit,
        'Saldo (€)': total_saldo,
        'Status': cor_total
    }])
    
    resumo_df = pd.concat([resumo_df, total_row], ignore_index=True)
    resumo_df = resumo_df.round(2)
    
    return resumo_df, total_debit, total_credit, total_saldo

col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Novembro 2025")
    resumo_nov, nov_debit, nov_credit, nov_saldo = criar_resumo(df_novembro, "NOVEMBRO")
    st.dataframe(resumo_nov, use_container_width=True, hide_index=True)
    
    st.metric("Saldo Novembro", f"€{nov_saldo:.2f}", delta=f"{nov_saldo:.2f}")

with col2:
    st.subheader("📅 Dezembro 2025")
    resumo_dez, dez_debit, dez_credit, dez_saldo = criar_resumo(df_dezembro, "DEZEMBRO")
    st.dataframe(resumo_dez, use_container_width=True, hide_index=True)
    
    st.metric("Saldo Dezembro", f"€{dez_saldo:.2f}", delta=f"{dez_saldo:.2f}")

st.divider()

total_geral_debit = nov_debit + dez_debit
total_geral_credit = nov_credit + dez_credit
total_geral_saldo = total_geral_credit - total_geral_debit

col3, col4, col5 = st.columns(3)
with col3:
    st.metric("Total Despesas (2 meses)", f"€{total_geral_debit:.2f}")
with col4:
    st.metric("Total Receitas (2 meses)", f"€{total_geral_credit:.2f}")
with col5:
    st.metric("Saldo Total (2 meses)", f"€{total_geral_saldo:.2f}", delta=f"{total_geral_saldo:.2f}")

st.divider()

st.subheader("📊 Comparativo Mensal")

comparativo_df = pd.DataFrame({
    'Mês': ['Novembro', 'Dezembro', 'TOTAL'],
    'Despesas (€)': [nov_debit, dez_debit, total_geral_debit],
    'Receitas (€)': [nov_credit, dez_credit, total_geral_credit],
    'Saldo (€)': [nov_saldo, dez_saldo, total_geral_saldo]
}).round(2)

st.dataframe(comparativo_df, use_container_width=True, hide_index=True)

st.sidebar.markdown("---")
st.sidebar.header("📥 Exportar CSV")

if st.sidebar.button("Baixar Novembro"):
    resumo_nov, _, _, _ = criar_resumo(df_novembro, "NOVEMBRO")
    csv = resumo_nov.to_csv(index=False)
    st.sidebar.download_button(
        label="Baixar Novembro CSV",
        data=csv,
        file_name="novembro_2025_totais.csv",
        mime="text/csv"
    )

if st.sidebar.button("Baixar Dezembro"):
    resumo_dez, _, _, _ = criar_resumo(df_dezembro, "DEZEMBRO")
    csv = resumo_dez.to_csv(index=False)
    st.sidebar.download_button(
        label="Baixar Dezembro CSV",
        data=csv,
        file_name="dezembro_2025_totais.csv",
        mime="text/csv"
    )
