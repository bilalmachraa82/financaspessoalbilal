#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏺 DASHBOARD DE VALIDAÇÃO - NOVEMBRO E DEZEMBRO 2025
Validação manual com sistema de aprendizagem automático
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path

class GestorAprendizagem:
    """Gere a gravação automática de validações no sistema de aprendizagem"""

    def __init__(self, ficheiro='APRENDIZAGEM_MANUAL_NOVEMBRO_DEZEMBRO.json'):
        self.ficheiro = ficheiro
        self.aprendizagem = self._carregar()
        self.sessao_atual = None

    def _carregar(self):
        if os.path.exists(self.ficheiro):
            try:
                with open(self.ficheiro, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"sessoes": [], "metadata": {"criado": datetime.now().isoformat()}}
        return {"sessoes": [], "metadata": {"criado": datetime.now().isoformat()}}

    def _salvar(self):
        self.aprendizagem['metadata']['ultima_atualizacao'] = datetime.now().isoformat()
        with open(self.ficheiro, 'w', encoding='utf-8') as f:
            json.dump(self.aprendizagem, f, indent=2, ensure_ascii=False)

    def iniciar_sessao(self):
        if self.sessao_atual is None or self.sessao_atual.get('finalizada', False):
            self.sessao_atual = {
                "inicio": datetime.now().isoformat(),
                "tipo": "validacao_dashboard",
                "escolhas": [],
                "finalizada": False
            }
            self.aprendizagem['sessoes'].append(self.sessao_atual)

    def registar_escolha(self, transacao_row, categoria_antiga, categoria_nova,
                         sugestao_sistema=None, confianca_sugestao=0.0):
        self.iniciar_sessao()

        entrada = {
            "timestamp": datetime.now().isoformat(),
            "transacao": {
                "data": str(transacao_row['Date']),
                "banco": str(transacao_row['Bank']),
                "descricao": str(transacao_row['Description']),
                "valor": float(transacao_row['Valor']),
                "tipo": "credit" if transacao_row.get('Credit', 0) > 0 else "debit"
            },
            "sugestao_sistema": {
                "categoria": sugestao_sistema,
                "confianca": float(confianca_sugestao)
            },
            "escolha_utilizador": {
                "categoria": categoria_nova,
                "confianca": 0.95,
                "tipo": "aceite_sugestao" if categoria_nova == sugestao_sistema else "escolha_manual"
            },
            "categoria_anterior": categoria_antiga
        }

        self.sessao_atual['escolhas'].append(entrada)
        self._salvar()

    def finalizar_sessao(self, total_mudancas):
        if self.sessao_atual and not self.sessao_atual.get('finalizada', False):
            self.sessao_atual['finalizada'] = True
            self.sessao_atual['fim'] = datetime.now().isoformat()
            self.sessao_atual['total_escolhas'] = len(self.sessao_atual['escolhas'])
            self.sessao_atual['total_reclassificadas'] = total_mudancas
            self._salvar()

def carregar_categorias_disponiveis():
    """Carrega categorias do sistema V5_1"""
    with open('SISTEMA_MEMORIAS_REGRAS_CLASSIFICACAO_V5_1.json', 'r', encoding='utf-8') as f:
        sistema = json.load(f)
    
    regras = sistema['sistema_memorias_regras']['regras_classificacao_melhoradas']
    categorias_unicas = set()
    
    for regra_id, regra in regras.items():
        categorias_unicas.add(regra['categoria'])
    
    return sorted(list(categorias_unicas))

def carregar_regras_v5_1():
    with open('SISTEMA_MEMORIAS_REGRAS_CLASSIFICACAO_V5_1.json', 'r', encoding='utf-8') as f:
        sistema = json.load(f)
    return sistema['sistema_memorias_regras']['regras_classificacao_melhoradas']

@st.cache_data
def carregar_csv_local(caminho: str, mtime: float):
    return pd.read_csv(caminho)

@st.cache_data
def carregar_mapa_historico():
    fontes = [
        Path('OUTUBRO_2025_VALIDADO.csv'),
        Path('data/raw/dados_setembro_apenas.csv')
    ]

    frames = []
    for p in fontes:
        if not p.exists():
            continue
        try:
            df = pd.read_csv(p)
        except Exception:
            continue
        if 'Description' not in df.columns or 'Categoria' not in df.columns:
            continue

        tmp = df[['Description', 'Categoria']].copy()
        tmp['Categoria'] = tmp['Categoria'].fillna('').astype(str)
        tmp = tmp[tmp['Categoria'].str.strip().str.lower().ne('nao categorizado')]
        tmp['_desc_norm'] = tmp['Description'].astype(str).str.lower().str.strip()
        frames.append(tmp[['_desc_norm', 'Categoria']])

    if not frames:
        return {}

    hist = pd.concat(frames, ignore_index=True)
    catsets = hist.groupby('_desc_norm')['Categoria'].agg(lambda s: sorted(set(s)))
    return {desc: cats[0] for desc, cats in catsets.items() if len(cats) == 1}

def sugerir_categoria(row, regras):
    descricao = str(row['Description']).lower()
    valor = row['Valor']
    tipo_transacao = 'credit' if row.get('Credit', 0) > 0 else 'debit'

    melhor_categoria = None
    melhor_confianca = 0.0

    for _, regra in regras.items():
        if regra.get('tipo') not in [tipo_transacao, 'both']:
            continue

        palavras_chave = regra.get('palavras_chave', [])
        for palavra in palavras_chave:
            if palavra.lower() in descricao:
                confianca = float(regra.get('confianca', 0.5))

                valores_tipicos = regra.get('valores_tipicos', [])
                for v_tipico in valores_tipicos:
                    if abs(valor - v_tipico) / max(v_tipico, 0.01) < 0.15:
                        confianca += 0.1
                        break

                if confianca > melhor_confianca:
                    melhor_confianca = confianca
                    melhor_categoria = regra.get('categoria')
                break

    return melhor_categoria, melhor_confianca

def main():
    st.set_page_config(
        page_title="🏺 Validação Novembro/Dezembro 2025",
        page_icon="🏺",
        layout="wide"
    )

    st.title("🏺 Validação de Transações - Novembro/Dezembro 2025")
    
    st.sidebar.markdown("## 📚 Sistema de Aprendizagem")
    
    st.sidebar.info("""
    **Como o sistema aprende:**
    
    1. ✅ Validas cada transação manualmente
    2. 📝 Sistema grava as tuas escolhas automaticamente
    3. 🧯 Aplicas a aprendizagem às regras V5_1
    4. 🚀 Sistema melhora classificações futuras
    """)

    gestor = GestorAprendizagem()
    regras = carregar_regras_v5_1()

    caminho_default = str(Path('data/processed/novembro_dezembro_2025_classificado.csv'))

    st.sidebar.markdown("## 📂 Dados")
    usar_ficheiro_local = st.sidebar.checkbox(
        "Usar ficheiro local (recomendado)",
        value=os.path.exists(caminho_default)
    )

    uploaded_file = None
    if not usar_ficheiro_local:
        uploaded_file = st.file_uploader(
            "📂 Carregar ficheiro de transações",
            type=['csv'],
            help="Carregue um CSV no formato do sistema (colunas Date/Bank/Description/Valor/Debit/Credit/Categoria/Confianca/Observacao)"
        )

    df = None
    fonte_dados = None
    fonte_key = None
    if usar_ficheiro_local and os.path.exists(caminho_default):
        try:
            mtime = os.path.getmtime(caminho_default)
            df = carregar_csv_local(caminho_default, mtime).copy()
            fonte_dados = f"Ficheiro local: {caminho_default}"
            fonte_key = f"{caminho_default}:{mtime}"
        except Exception as e:
            st.error(f"Erro a ler ficheiro local: {e}")
    elif uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            fonte_dados = "Upload"
            fonte_key = "Upload"
        except Exception as e:
            st.error(f"Erro a ler CSV carregado: {e}")

    if df is not None:
        fonte_key = fonte_key or fonte_dados or "desconhecido"
        if st.session_state.get('fonte_key') != fonte_key or 'df_editado' not in st.session_state:
            st.session_state['df_editado'] = df.copy()
            st.session_state['fonte_key'] = fonte_key

        df = st.session_state['df_editado']

        st.caption(f"Fonte de dados: {fonte_dados}")
        df['Categoria'] = df['Categoria'].fillna('Nao Categorizado')

        categorias_disponiveis = carregar_categorias_disponiveis()
        categorias_disponiveis.insert(0, 'Nao Categorizado')

        st.sidebar.markdown("## 📊 Estatísticas")
        total = len(df)
        classificadas = len(df[df['Categoria'] != 'Nao Categorizado'])
        por_classificar = total - classificadas
        
        st.sidebar.metric("Total Transações", total)
        st.sidebar.metric("Classificadas", classificadas, delta=f"{classificadas/total*100:.1f}%")
        st.sidebar.metric("Por Classificar", por_classificar)

        st.sidebar.markdown("## ⚡ Atalhos")
        limiar_auto = st.sidebar.slider(
            "Confiança mínima para auto-aplicar",
            min_value=0.70,
            max_value=1.00,
            value=0.85,
            step=0.01
        )

        if st.sidebar.button("⚡ Auto-aplicar sugestões confiáveis", use_container_width=True):
            aplicadas = 0
            for idx, row in df[df['Categoria'] == 'Nao Categorizado'].iterrows():
                sugestao, confianca = sugerir_categoria(row, regras)
                if sugestao and confianca >= limiar_auto:
                    df.at[idx, 'Categoria'] = sugestao
                    df.at[idx, 'Confianca'] = round(float(confianca), 2)
                    df.at[idx, 'Observacao'] = 'Auto-aplicado (V5_1)'
                    aplicadas += 1

            if usar_ficheiro_local and aplicadas > 0:
                try:
                    df.to_csv(caminho_default, index=False)
                except Exception as e:
                    st.error(f"Erro a guardar CSV: {e}")
            
            st.sidebar.success(f"Aplicadas: {aplicadas}")
            st.rerun()

        if st.sidebar.button("📚 Preencher por histórico (match exato)", use_container_width=True):
            mapa = carregar_mapa_historico()
            aplicadas = 0
            if mapa:
                for idx, row in df[df['Categoria'] == 'Nao Categorizado'].iterrows():
                    desc_norm = str(row['Description']).lower().strip()
                    cat = mapa.get(desc_norm)
                    if cat:
                        df.at[idx, 'Categoria'] = cat
                        df.at[idx, 'Confianca'] = 0.95
                        df.at[idx, 'Observacao'] = 'Auto-aplicado (histórico)'
                        aplicadas += 1

            if usar_ficheiro_local and aplicadas > 0:
                try:
                    df.to_csv(caminho_default, index=False)
                except Exception as e:
                    st.error(f"Erro a guardar CSV: {e}")
            
            st.sidebar.success(f"Aplicadas: {aplicadas}")
            st.rerun()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total", total)
        col2.metric("Classificadas", classificadas)
        col3.metric("Por Classificar", por_classificar)

        st.subheader("🔍 Filtrar Transações")
        
        mes_selecionado = st.selectbox(
            "Mês",
            ["Todos", "Novembro", "Dezembro"],
            index=0
        )

        col_a, col_b = st.columns(2)
        filtro_categoria = col_a.selectbox(
            "Categoria",
            ["Todas"] + categorias_disponiveis,
            index=0
        )
        filtro_banco = col_b.selectbox(
            "Banco",
            ["Todos", "Millennium", "Revolut"],
            index=0
        )

        df_filtrado = df.copy()

        if mes_selecionado != "Todos":
            if mes_selecionado == "Novembro":
                df_filtrado = df_filtrado[df_filtrado['Date'].str.startswith('2025-11')]
            else:
                df_filtrado = df_filtrado[df_filtrado['Date'].str.startswith('2025-12')]

        if filtro_categoria != "Todas":
            df_filtrado = df_filtrado[df_filtrado['Categoria'] == filtro_categoria]

        if filtro_banco != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Bank'] == filtro_banco]

        df_filtrado = df_filtrado.copy()
        df_filtrado['_desc_norm'] = df_filtrado['Description'].astype(str).str.lower().str.strip()
        repeticoes = df_filtrado['_desc_norm'].value_counts()
        df_filtrado['Repeticoes'] = df_filtrado['_desc_norm'].map(repeticoes).fillna(1).astype(int)
        df_filtrado = df_filtrado.sort_values(by=['Repeticoes', 'Date'], ascending=[False, False])

        st.subheader(f"📋 Transações ({len(df_filtrado)} mostradas)")

        for idx, row in df_filtrado.iterrows():
            with st.expander(f"🔁 {row['Repeticoes']}x | 📅 {row['Date']} | {row['Bank']} | {row['Description'][:60]}...", expanded=False):
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.write(f"**Descrição:** {row['Description']}")
                    st.write(f"**Valor:** €{row['Valor']:.2f} {'(Crédito)' if row['Credit'] > 0 else '(Débito)'}")

                    sugestao_sistema, confianca_sistema = sugerir_categoria(row, regras)

                    if sugestao_sistema and confianca_sistema >= 0.70:
                        st.info(f"💡 Sugestão do sistema: **{sugestao_sistema}** (confiança: {confianca_sistema:.0%})")
                    else:
                        st.warning("⚠️ Sem sugestão com confiança suficiente")

                with col2:
                    nova_categoria = st.selectbox(
                        "Nova Categoria",
                        categorias_disponiveis,
                        index=categorias_disponiveis.index(row['Categoria']) if row['Categoria'] in categorias_disponiveis else 0,
                        key=f"cat_{idx}"
                    )

                with col3:
                    col3_1, col3_2 = st.columns(2)
                    
                    if col3_1.button("✅ Guardar", key=f"save_{idx}"):
                        if nova_categoria != row['Categoria']:
                            df.at[idx, 'Categoria'] = nova_categoria
                            df.at[idx, 'Observacao'] = 'Validado manualmente'
                            
                            gestor.registar_escolha(
                                row,
                                row['Categoria'],
                                nova_categoria,
                                sugestao_sistema,
                                confianca_sistema
                            )
                            
                            if usar_ficheiro_local:
                                try:
                                    df.to_csv(caminho_default, index=False)
                                except Exception as e:
                                    st.error(f"Erro a guardar CSV: {e}")
                            
                            st.success(f"✅ Categoria atualizada: {nova_categoria}")
                            st.rerun()
                        else:
                            st.info("Sem alterações para guardar.")

                    aplicar_lote = col3_2.button("🔁 Aplicar a iguais", key=f"save_all_{idx}")
                    if aplicar_lote:
                        desc_norm = str(row['Description']).lower().strip()
                        mask = (df['Bank'] == row['Bank']) & (df['Description'].astype(str).str.lower().str.strip() == desc_norm)
                        indices = df.index[mask].tolist()

                        alterados = 0
                        for i in indices:
                            if df.at[i, 'Categoria'] != nova_categoria:
                                old_cat = df.at[i, 'Categoria']
                                df.at[i, 'Categoria'] = nova_categoria
                                df.at[i, 'Observacao'] = 'Validado manualmente (lote)'

                                transacao_row = df.loc[i]
                                sugestao, confianca = sugerir_categoria(transacao_row, regras)

                                gestor.registar_escolha(
                                    transacao_row,
                                    old_cat,
                                    nova_categoria,
                                    sugestao,
                                    confianca if confianca else 0.0
                                )
                                alterados += 1

                        if usar_ficheiro_local and alterados > 0:
                            try:
                                df.to_csv(caminho_default, index=False)
                            except Exception as e:
                                st.error(f"Erro a guardar CSV: {e}")
                        
                        st.success(f"✅ Aplicado a {alterados} transações iguais ({row['Bank']})")
                        st.rerun()

        if st.button("💾 Guardar Todas as Mudanças e Descarregar"):
            if usar_ficheiro_local:
                try:
                    df.to_csv(caminho_default, index=False)
                except Exception as e:
                    st.error(f"Erro a guardar CSV: {e}")
            output = df.to_csv(index=False)
            st.download_button(
                label="📥 Descarregar CSV Validado",
                data=output,
                file_name=f"novembro_dezembro_2025_validado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            gestor.finalizar_sessao(len(df[df['Categoria'] != 'Nao Categorizado']))
            st.success("✅ Sessão de aprendizagem gravada!")
    else:
        if os.path.exists(caminho_default):
            st.info("Ativa 'Usar ficheiro local' na sidebar para carregar automaticamente.")
        else:
            st.info("Coloca o ficheiro em data/processed/novembro_dezembro_2025_classificado.csv ou faz upload.")

if __name__ == "__main__":
    main()
