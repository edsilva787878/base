from flask import Flask, render_template, request
import pandas as pd
import os

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

    resultados = []

    if termo:

        filtro = df.apply(
            lambda linha: linha.astype(str)
            .str.contains(termo, case=False, na=False)
            .any(),
            axis=1
        )

        resultados = (
            df[filtro]
            .head(500)
            .to_dict(orient="records")
        )

    colunas = df.columns.tolist()

    return render_template(
        "index.html",
        resultados=resultados,
        colunas=colunas,
        termo=termo,
        total=len(resultados)
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=9000,
        debug=True
    )