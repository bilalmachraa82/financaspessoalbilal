#!/usr/bin/env python3
"""
Mapeamento de Categorias - Estrutura Oficial vs Setembro 2025
Preserva todas as categorias existentes e mapeia para estrutura oficial
"""

import pandas as pd
import json
from datetime import datetime
from collections import defaultdict

def definir_estrutura_oficial():
    """Define a estrutura oficial de categorias conforme especificado"""
    return {
        "Casa": [
            "Casa - Renda Fontanelas",
            "Casa - Renda Monte da Caparica", 
            "Casa - Supermercado Bilal",
            "Casa - Supermercado Daniela",
            "Casa - Luz",
            "Casa - Internet (Net)",
            "Casa - Limpeza",
            "Casa - Outros"
        ],
        "Pessoal Bilal": [
            "Pessoal Bilal - Comer fora",
            "Pessoal Bilal - Vestuário/calçado",
            "Pessoal Bilal - Férias/viagens/Passeios",
            "Pessoal Bilal - Livros/Cinema/Concertos",
            "Pessoal Bilal - Donativos/Quotas",
            "Pessoal Bilal - Barbeiro",
            "Pessoal Bilal - Presentes",
            "Pessoal Bilal - Outros"
        ],
        "Créditos/Seguros Bilal": [
            "Créditos/Seguros Bilal - Pessoal Millennium",
            "Créditos/Seguros Bilal - Wizink",
            "Créditos/Seguros Bilal - Seg vida",
            "Créditos/Seguros Bilal - Cliente frequente",
            "Créditos/Seguros Bilal - Despesas bancárias Bilal"
        ],
        "Deslocações Bilal": [
            "Deslocações Bilal - Transportes",
            "Deslocações Bilal - Via Verde",
            "Deslocações Bilal - Carro",
            "Deslocações Bilal - Combustível",
            "Deslocações Bilal - Estacionamento",
            "Deslocações Bilal - ACP"
        ],
        "Saúde": [
            "Saúde - Consultas Bilal",
            "Saúde - Consultas Daniela",
            "Saúde - Farmácia/Prod.Nat./Exames",
            "Saúde - Pruvit",
            "Saúde - Lifewave"
        ],
        "Noah": [
            "Noah - Pensão de alimentos",
            "Noah - Desporto",
            "Noah - Consultas",
            "Noah - Roupa",
            "Noah - Outros"
        ],
        "Despesas Profissionais Bilal": [
            "Despesas Profissionais Bilal - Mensalidades (Replit, GPT, etc.)",
            "Despesas Profissionais Bilal - Formação Bilal",
            "Despesas Profissionais Bilal - Seg. Social Bilal",
            "Despesas Profissionais Bilal - Produtos (Lifewave/Pruvit, etc.)",
            "Despesas Profissionais Bilal - Marketing digital",
            "Despesas Profissionais Bilal - BNI"
        ],
        "Receitas": [
            "Receitas - Sessões Bilal",
            "Receitas - Limpezas Espaços",
            "Receitas - Workshop TMD",
            "Receitas - Aulas Individuais",
            "Receitas - Soluções IA",
            "Receitas - Lifewave",
            "Receitas - Pruvit",
            "Receitas - Rendas Fontanelas",
            "Receitas - Electricidade Fontanelas",
            "Receitas - Renda Monte da Caparica",
            "Receitas - Outros"
        ]
    }

def carregar_dados_setembro():
    """Carrega dados de setembro"""
    try:
        df = pd.read_csv('/Users/bilal/Programaçao/financas pessoais/septembro/septembro completo.csv')
        print(f"✅ Dados carregados: {len(df)} transações")
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return None

def analisar_mapeamento(df, estrutura_oficial):
    """Analisa o mapeamento entre categorias de setembro e estrutura oficial"""
    
    print("\n" + "="*60)
    print("🔍 ANÁLISE DE MAPEAMENTO DE CATEGORIAS")
    print("="*60)
    
    # Categorias usadas em setembro
    categorias_setembro = df['Categoria'].value_counts()
    print(f"\n📊 Categorias encontradas em setembro: {len(categorias_setembro)}")
    
    # Todas as categorias oficiais (flatten)
    categorias_oficiais = []
    for grupo, cats in estrutura_oficial.items():
        categorias_oficiais.extend(cats)
    
    print(f"📋 Categorias na estrutura oficial: {len(categorias_oficiais)}")
    
    # Mapeamento
    mapeamento = {
        "correspondencias_exatas": [],
        "correspondencias_parciais": [],
        "categorias_setembro_nao_mapeadas": [],
        "categorias_oficiais_nao_usadas": []
    }
    
    # Verificar correspondências
    for cat_set in categorias_setembro.index:
        if cat_set in categorias_oficiais:
            mapeamento["correspondencias_exatas"].append({
                "categoria": cat_set,
                "transacoes": int(categorias_setembro[cat_set])
            })
        else:
            # Verificar correspondências parciais
            correspondencia_parcial = False
            for cat_oficial in categorias_oficiais:
                if any(palavra in cat_oficial.lower() for palavra in cat_set.lower().split()):
                    mapeamento["correspondencias_parciais"].append({
                    "categoria_setembro": cat_set,
                    "categoria_oficial_sugerida": cat_oficial,
                    "transacoes": int(categorias_setembro[cat_set])
                })
                    correspondencia_parcial = True
                    break
            
            if not correspondencia_parcial:
                mapeamento["categorias_setembro_nao_mapeadas"].append({
                    "categoria": cat_set,
                    "transacoes": int(categorias_setembro[cat_set])
                })
    
    # Categorias oficiais não usadas
    categorias_usadas = set(categorias_setembro.index)
    for cat_oficial in categorias_oficiais:
        if cat_oficial not in categorias_usadas:
            mapeamento["categorias_oficiais_nao_usadas"].append(cat_oficial)
    
    return mapeamento

def gerar_relatorio_mapeamento(mapeamento, estrutura_oficial):
    """Gera relatório detalhado do mapeamento"""
    
    print("\n" + "="*60)
    print("📋 RELATÓRIO DE MAPEAMENTO")
    print("="*60)
    
    # Correspondências exatas
    print(f"\n✅ CORRESPONDÊNCIAS EXATAS ({len(mapeamento['correspondencias_exatas'])})")
    print("-" * 40)
    for item in mapeamento['correspondencias_exatas']:
        print(f"  • {item['categoria']}: {item['transacoes']} transação(ões)")
    
    # Correspondências parciais
    print(f"\n🔄 CORRESPONDÊNCIAS PARCIAIS ({len(mapeamento['correspondencias_parciais'])})")
    print("-" * 40)
    for item in mapeamento['correspondencias_parciais']:
        print(f"  • Setembro: {item['categoria_setembro']}")
        print(f"    Oficial: {item['categoria_oficial_sugerida']}")
        print(f"    Transações: {item['transacoes']}")
        print()
    
    # Categorias de setembro não mapeadas
    print(f"\n⚠️  CATEGORIAS DE SETEMBRO NÃO MAPEADAS ({len(mapeamento['categorias_setembro_nao_mapeadas'])})")
    print("-" * 40)
    for item in mapeamento['categorias_setembro_nao_mapeadas']:
        print(f"  • {item['categoria']}: {item['transacoes']} transação(ões)")
    
    # Categorias oficiais não usadas
    print(f"\n📝 CATEGORIAS OFICIAIS NÃO UTILIZADAS ({len(mapeamento['categorias_oficiais_nao_usadas'])})")
    print("-" * 40)
    for grupo, categorias in estrutura_oficial.items():
        cats_nao_usadas = [cat for cat in categorias if cat in mapeamento['categorias_oficiais_nao_usadas']]
        if cats_nao_usadas:
            print(f"\n  {grupo}:")
            for cat in cats_nao_usadas:
                print(f"    • {cat}")

def criar_regras_mapeamento(mapeamento):
    """Cria regras de mapeamento para preservar aprendizado"""
    
    regras = {
        "regras_exatas": {},
        "regras_parciais": {},
        "regras_aprendidas": {},
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Regras exatas (já estão corretas)
    for item in mapeamento['correspondencias_exatas']:
        regras["regras_exatas"][item['categoria']] = item['categoria']
    
    # Regras parciais (sugestões de mapeamento)
    for item in mapeamento['correspondencias_parciais']:
        regras["regras_parciais"][item['categoria_setembro']] = item['categoria_oficial_sugerida']
    
    # Regras aprendidas (categorias que precisam ser preservadas)
    for item in mapeamento['categorias_setembro_nao_mapeadas']:
        regras["regras_aprendidas"][item['categoria']] = {
            "preservar": True,
            "transacoes": item['transacoes'],
            "motivo": "Categoria específica aprendida em setembro"
        }
    
    return regras

def gerar_sugestoes_melhorias():
    """Gera sugestões de melhorias sem eliminar categorias"""
    
    print("\n" + "="*60)
    print("💡 SUGESTÕES DE MELHORIAS (SEM ELIMINAR CATEGORIAS)")
    print("="*60)
    
    sugestoes = [
        "1. Manter todas as categorias existentes como base de conhecimento",
        "2. Mapear categorias de setembro para estrutura oficial quando possível",
        "3. Preservar categorias específicas aprendidas em setembro",
        "4. Criar aliases para facilitar categorização futura",
        "5. Implementar sistema de sugestões baseado em histórico",
        "6. Adicionar validação para evitar duplicações",
        "7. Criar dashboard com ambas as estruturas para comparação"
    ]
    
    for sugestao in sugestoes:
        print(f"  {sugestao}")
    
    print(f"\n🎯 OBJETIVO: Preservar todo o conhecimento adquirido")
    print(f"📈 BENEFÍCIO: Sistema mais inteligente e preciso")

def main():
    """Função principal"""
    print("🏛️ SISTEMA DE MAPEAMENTO DE CATEGORIAS - PRESERVAÇÃO TOTAL")
    print("=" * 70)
    
    # Definir estrutura oficial
    estrutura_oficial = definir_estrutura_oficial()
    
    # Carregar dados
    df = carregar_dados_setembro()
    if df is None:
        return
    
    # Analisar mapeamento
    mapeamento = analisar_mapeamento(df, estrutura_oficial)
    
    # Gerar relatório
    gerar_relatorio_mapeamento(mapeamento, estrutura_oficial)
    
    # Criar regras
    regras = criar_regras_mapeamento(mapeamento)
    
    # Salvar regras
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_regras = f"regras_mapeamento_preservacao_{timestamp}.json"
    
    with open(filename_regras, 'w', encoding='utf-8') as f:
        json.dump(regras, f, indent=2, ensure_ascii=False)
    
    # Salvar mapeamento completo
    filename_mapeamento = f"mapeamento_completo_{timestamp}.json"
    resultado_completo = {
        "estrutura_oficial": estrutura_oficial,
        "mapeamento": mapeamento,
        "regras": regras,
        "timestamp": timestamp
    }
    
    with open(filename_mapeamento, 'w', encoding='utf-8') as f:
        json.dump(resultado_completo, f, indent=2, ensure_ascii=False)
    
    # Gerar sugestões
    gerar_sugestoes_melhorias()
    
    print(f"\n💾 Arquivos salvos:")
    print(f"  • {filename_regras}")
    print(f"  • {filename_mapeamento}")
    
    print(f"\n✅ Análise de mapeamento concluída!")
    print(f"🎯 Todas as categorias foram preservadas e mapeadas!")

if __name__ == "__main__":
    main()