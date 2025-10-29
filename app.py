from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        model = request.form.get("model")
        lam = float(request.form.get("lambda"))
        mu = float(request.form.get("mu"))
        K = request.form.get("K")
        K = int(K) if K else None

        rho = lam / mu
        results = {}

        # Modelo M/M/1
        if model == "MM1" and rho < 1:
            Lq = (rho**2) / (1 - rho)
            L = rho / (1 - rho)
            Wq = Lq / lam
            W = L / lam
            results = {
                "ρ (Utilización)": rho,
                "Lq (Clientes en cola)": Lq,
                "L (Clientes en el sistema)": L,
                "Wq (Tiempo en cola)": Wq,
                "W (Tiempo total en el sistema)": W
            }

        # Modelo M/M/1/K
        elif model == "MM1K" and K and rho != 1:
            P0 = (1 - rho) / (1 - rho**(K + 1))
            PK = ((1 - rho) * rho**K) / (1 - rho**(K + 1))
            L = rho * ((1 - (K + 1)*rho**K + K*rho**(K + 1)) / ((1 - rho)*(1 - rho**(K + 1))))
            W = L / (lam * (1 - PK))
            results = {
                "ρ (Utilización)": rho,
                "P₀ (Probabilidad 0 en el sistema)": P0,
                "Pₖ (Probabilidad sistema lleno)": PK,
                "L (Clientes en el sistema)": L,
                "W (Tiempo promedio en el sistema)": W
            }
        else:
            results = {"Error": "Parámetros inválidos o modelo no soportado."}

        return render_template("result.html", results=results, model=model)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)