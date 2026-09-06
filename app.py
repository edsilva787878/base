from flask import Flask, render_template, request
import pandas as pd
import os
import re

app = Flask(__name__)

CSV_FILE = "consolidado.csv"

try:
    df = pd.read_csv(
        CSV_FILE,
        sep=";",
        encoding="utf-8",
        dtype=str,
        low_memory=False
    )
    df.fillna("", inplace=True)
except Exception as e:
    print(f"Erro ao carregar CSV: {e}")
    df = pd.DataFrame()


@app.route("/")
def index():
    termo = request.args.get("q", "").strip()
    modo = request.args.get("modo", "tudo")  # 'tudo' ou 'id'
    
    resultados = []
    is_numeric = False
    
    if termo:
        # Verifica se o termo parece um ID (números, hífens, letras hex)
        is_numeric = re.match(r'^[\d\-a-fA-F]{8,}$', termo) is not None
        
        if modo == "id" or (is_numeric and modo == "tudo"):
            # Busca APENAS nas colunas que contêm ID
            colunas_id = [
                col for col in df.columns 
                if 'ID' in col.upper() or 'id' in col.lower() or 'ACCOUNT' in col.upper()
            ]
            
            # Se não encontrou colunas com ID, usa todas
            if not colunas_id:
                colunas_id = df.columns.tolist()
            
            # Aplica o filtro apenas nas colunas de ID
            filtro = pd.Series([False] * len(df))
            for col in colunas_id:
                filtro = filtro | df[col].astype(str).str.contains(termo, case=False, na=False)
            
            resultados = df[filtro].head(500).to_dict(orient="records")
        else:
            # Busca em TODAS as colunas (comportamento original)
            filtro = df.apply(
                lambda linha: linha.astype(str)
                .str.contains(termo, case=False, na=False)
                .any(),
                axis=1
            )
            resultados = df[filtro].head(500).to_dict(orient="records")
    
    colunas = df.columns.tolist()
    
    # Identifica colunas de ID para exibição
    colunas_id = [col for col in colunas if 'ID' in col.upper() or 'id' in col.lower() or 'ACCOUNT' in col.upper()]
    
    return render_template(
        "index.html",
        resultados=resultados,
        colunas=colunas,
        colunas_id=colunas_id,
        termo=termo,
        total=len(resultados),
        modo=modo,
        is_numeric=is_numeric
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=9000,
        debug=True
    )