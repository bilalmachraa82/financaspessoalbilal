# Dashboard de Classificação Financeira

Dashboard interativo para classificar e validar transações financeiras pessoais.

## Deploy Online

O dashboard está disponível online em: [Streamlit Cloud](https://share.streamlit.io)

### Como atualizar dados online

1. Classifique as transações no dashboard
2. As alterações são guardadas automaticamente no ficheiro CSV
3. Para sincronizar com o repositório local:
   ```bash
   git pull
   ```

## Estrutura do Projeto

```
.
├── dashboard_validacao_novembro_dezembro.py    # Dashboard principal
├── SISTEMA_MEMORIAS_REGRAS_CLASSIFICACAO_V5_1.json  # Regras de classificação
├── processar_novembro_dezembro_2025.py         # Processamento de dados
├── preparar_csvs_nov_dez.py                    # Preparação de CSVs
├── requirements.txt                            # Dependências Python
└── data/
    ├── raw/                                    # Dados brutos por banco/mês
    │   ├── novembro_2025/
    │   │   ├── millennium_novembro_2025.csv
    │   │   └── revolut_novembro_2025.csv
    │   └── dezembro_2025/
    │       ├── millennium_dezembro_2025.csv
    │       └── revolut_dezembro_2025.csv
    └── processed/                              # Dados processados
        └── novembro_dezembro_2025_classificado.csv
```

## Funcionalidades

### Dashboard Principal

- **Classificação automática:** Baseada em regras e histórico
- **Classificação manual:** Interface interativa para cada transação
- **Aplicação em lote:** Classificar todas as transações com a mesma descrição
- **Histórico:** Sugestões baseadas em classificações anteriores
- **Exportação:** Download do CSV validado

### Sistema de Regras V5.1

O sistema usa 34 categorias com 198 palavras-chave para auto-classificação.

**Categorias principais:**
- Despesas bancárias (imposto do selo, comissões)
- Deslocações de carro (Via Verde, ACP, autoestradas)
- Restauração e alimentação
- Supermercado e compras
- Créditos e seguros
- etc.

## Como Adicionar Novas Regras

Edite o ficheiro `SISTEMA_MEMORIAS_REGRAS_CLASSIFICACAO_V5_1.json`:

```json
{
  "nova_categoria": {
    "categoria": "Nome da Categoria",
    "tipo": "debit|credit",
    "palavras_chave": ["palavra1", "palavra2"]
  }
}
```

## Atualizar com Novos Dados

### 1. Exportar CSV dos bancos
- Millennium: Exportar para CSV
- Revolut: Exportar para CSV

### 2. Colocar na pasta correta
```bash
# Novembro
data/raw/novembro_2025/millennium_novembro_2025.csv
data/raw/novembro_2025/revolut_novembro_2025.csv

# Dezembro
data/raw/dezembro_2025/millennium_dezembro_2025.csv
data/raw/dezembro_2025/revolut_dezembro_2025.csv
```

### 3. Processar os dados
```bash
python3 processar_novembro_dezembro_2025.py
```

### 4. Atualizar no GitHub
```bash
git add data/
git commit -m "Atualização de dados"
git push
```

## Executar Localmente

### Instalar dependências
```bash
pip install -r requirements.txt
```

### Executar dashboard
```bash
streamlit run dashboard_validacao_novembro_dezembro.py
```

Aceder a: http://localhost:8501

## Soluções de Problemas

### Dashboard não carrega dados
- Verifique se o CSV existe em `data/processed/`
- Verifique o formato das colunas (Date, Bank, Description, Valor, Categoria)

### Classificações não se guardam
- Verifique permissões de escrita na pasta `data/processed/`
- No Streamlit Cloud, as alterações ficam no repositório

### Erro de parsing de valores
- O script `preparar_csvs_nov_dez.py` corrige formatos do Millennium
- Reexecute: `python3 preparar_csvs_nov_dez.py`

## Licença

Uso pessoal.
