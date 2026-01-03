#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏺 PROCESSADOR DE NOVEMBRO E DEZEMBRO 2025
Aplica aprendizagem V5_1 para classificar transações
"""

import pandas as pd
import json
import csv
from datetime import datetime

class ProcessadorNovembroDezembro:
    def __init__(self):
        """Inicializa o processador com as regras V5_1"""
        with open('SISTEMA_MEMORIAS_REGRAS_CLASSIFICACAO_V5_1.json', 'r', encoding='utf-8') as f:
            self.sistema = json.load(f)

        self.regras = self.sistema['sistema_memorias_regras']['regras_classificacao_melhoradas']
        self.transacoes_processadas = []
        self.transacoes_em_duvida = []

    def classificar_transacao(self, transacao):
        """Classifica uma transação usando o sistema V5_1"""
        descricao = transacao['Description'].lower()
        valor = transacao['Valor']
        tipo_transacao = 'credit' if transacao['Credit'] > 0 else 'debit'

        melhor_categoria = None
        melhor_confianca = 0.0

        for _, regra in self.regras.items():
            if regra.get('tipo') not in [tipo_transacao, 'both']:
                continue

            palavras_chave = regra.get('palavras_chave', [])
            encontrou = False
            for palavra in palavras_chave:
                if palavra.lower() in descricao:
                    encontrou = True
                    break

            if not encontrou:
                continue

            confianca = float(regra.get('confianca', 0.5))

            valores_tipicos = regra.get('valores_tipicos', [])
            for v_tipico in valores_tipicos:
                if abs(valor - v_tipico) / max(v_tipico, 0.01) < 0.15:
                    confianca += 0.1
                    break

            if confianca > melhor_confianca:
                melhor_confianca = confianca
                melhor_categoria = regra.get('categoria')

        if melhor_categoria:
            transacao['Categoria'] = melhor_categoria
            transacao['Confianca'] = melhor_confianca
            transacao['Observacao'] = 'Classificado automaticamente'
            return True

        transacao['Categoria'] = 'Nao Categorizado'
        transacao['Confianca'] = 0.0
        transacao['Observacao'] = 'Necessita revisão manual'
        return False

    def processar_csv(self, caminho, mes_nome):
        """Processa ficheiro CSV de um mês"""
        print(f"\n📊 Processando {mes_nome}...")

        try:
            df = pd.read_csv(caminho)
            print(f"   ✅ Carregadas {len(df)} transações")

            classificadas = 0
            em_duvida = 0

            for idx, row in df.iterrows():
                transacao = {
                    'Date': row['Date'],
                    'Bank': row['Bank'],
                    'Description': row['Description'],
                    'Valor': row['Valor'],
                    'Debit': row['Debit'],
                    'Credit': row['Credit'],
                    'Categoria': None,
                    'Confianca': 0.0,
                    'Observacao': ''
                }

                classificada = self.classificar_transacao(transacao)

                if classificada:
                    classificadas += 1
                else:
                    em_duvida += 1

                self.transacoes_processadas.append(transacao)

            print(f"   ✅ Classificadas: {classificadas}")
            print(f"   ⚠️  Em dúvida: {em_duvida}")

            return True

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return False

    def consolidar_e_salvar(self, nome_arquivo):
        """Consolida todas as transações e salva em CSV"""
        print(f"\n💾 Salvando transações consolidadas...")

        df = pd.DataFrame(self.transacoes_processadas)

        output_path = f'data/processed/{nome_arquivo}'
        df.to_csv(output_path, index=False, encoding='utf-8')

        print(f"   ✅ Salvo: {output_path}")

        resumo = self.gerar_resumo(df)
        print("\n📈 RESUMO DA CLASSIFICAÇÃO:")
        print("=" * 60)
        print(f"Total de transações: {len(df)}")
        print(f"Classificadas automaticamente: {resumo['classificadas']}")
        print(f"Em dúvida: {resumo['em_duvida']}")
        print(f"\nDistribuição por categoria:")
        for cat, count in resumo['categorias'].items():
            if cat != 'Nao Categorizado':
                print(f"  - {cat}: {count}")

        return output_path

    def gerar_resumo(self, df):
        """Gera resumo estatístico"""
        classificadas = len(df[df['Categoria'] != 'Nao Categorizado'])
        em_duvida = len(df[df['Categoria'] == 'Nao Categorizado'])

        categorias = df['Categoria'].value_counts().to_dict()

        return {
            'total': len(df),
            'classificadas': classificadas,
            'em_duvida': em_duvida,
            'categorias': categorias
        }

def main():
    print("=" * 60)
    print("🏺 PROCESSADOR DE NOVEMBRO E DEZEMBRO 2025")
    print("=" * 60)

    processador = ProcessadorNovembroDezembro()

    arquivos = [
        ('data/raw/novembro_2025/millennium_novembro_2025.csv', 'Millennium Novembro'),
        ('data/raw/novembro_2025/revolut_novembro_2025.csv', 'Revolut Novembro'),
        ('data/raw/dezembro_2025/millennium_dezembro_2025.csv', 'Millennium Dezembro'),
        ('data/raw/dezembro_2025/revolut_dezembro_2025.csv', 'Revolut Dezembro')
    ]

    for arquivo, nome in arquivos:
        processador.processar_csv(arquivo, nome)

    output = processador.consolidar_e_salvar('novembro_dezembro_2025_classificado.csv')

    print("\n✅ PROCESSAMENTO CONCLUÍDO!")
    print(f"📁 Ficheiro salvo: {output}")
    print("\n💡 PRÓXIMOS PASSOS:")
    print("1. Revise as transações em dúvida no CSV")
    print("2. Corrija as categorias conforme necessário")
    print("3. Importe para o sistema de aprendizagem")

if __name__ == "__main__":
    main()
