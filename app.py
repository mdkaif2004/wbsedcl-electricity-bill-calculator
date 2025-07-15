from flask import Flask, render_template, request

app = Flask(__name__)

# Slab-based energy and subsidy rates
def get_energy_rate(units):
    if units <= 200:
        return 5.49
    elif units <= 400:
        return 6.30
    else:
        return 6.60

def get_subsidy_rate(units):
    if units <= 200:
        return 1.07
    elif units <= 400:
        return 0.91
    else:
        return 0.87

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        try:
            units = int(request.form["units"])
            if units < 0:
                raise ValueError("Units must be positive")

            # Rates
            energy_rate = get_energy_rate(units)
            subsidy_rate = get_subsidy_rate(units)

            # Charges
            energy_charge = units * energy_rate
            fixed_charge = 90.00
            meter_rent = 30.00
            subsidy = -(units * subsidy_rate)
            adjustments = -0.60
            special_rebate = -(units * 0.10)
            monthly_rebate = -7.80
            epay_discount = -23.00

            gross_amount = energy_charge + fixed_charge + meter_rent + subsidy
            final_amount = gross_amount + adjustments + special_rebate
            amount_with_rebate = final_amount + monthly_rebate
            epay_amount = amount_with_rebate + epay_discount

            result = {
                "units": units,
                "energy_rate": energy_rate,
                "energy_charge": round(energy_charge, 2),
                "fixed_charge": fixed_charge,
                "meter_rent": meter_rent,
                "subsidy": round(subsidy, 2),
                "gross_amount": round(gross_amount, 2),
                "adjustments": adjustments,
                "special_rebate": round(special_rebate, 2),
                "final_amount": round(final_amount, 2),
                "amount_with_rebate": round(amount_with_rebate, 2),
                "epay_amount": round(epay_amount, 2)
            }

        except ValueError:
            result = {"error": "Please enter a valid number of units."}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
