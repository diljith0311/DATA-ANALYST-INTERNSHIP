from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

data = {
    'Asia': {
        'years': [2011, 2012, 2013, 2014, 2015, 2016, 2017],
        'units_sold': [13953, 6708, 5010, 4901, 14180, 6952, 8263],
        'profit': [893278, 846885, 632512, 122819, 1802771, 1208744, 606834]
    },
    'Australia and Oceania': {
        'years': [2010, 2012, 2013, 2014, 2015],
        'units_sold': [19830, 5908, 10336, 26353, 5898],
        'profit': [1678833, 337937, 1738959, 312186, 654242]
    },
    'Central America and the Caribbean': {
        'years': [2011, 2012, 2013, 2016, 2017],
        'units_sold': [8156, 2804, 1705, 7723, 15383],
        'profit': [127722, 248406, 296448, 526459, 1647870]
    },
    'Europe': {
        'years': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017],
        'units_sold': [18466, 273, 27901, 4750, 22195, 4120, 18597, 1815],
        'profit': [2588180, 6841, 3763320, 455335, 1594914, 617037, 1741735, 315574]
    },
    'Middle East and North Africa': {
        'years': [2010, 2011, 2012, 2013, 2015, 2016],
        'units_sold': [13350, 3784, 10427, 13955, 673, 6489],
        'profit': [1706934, 9119, 835410, 2079863, 1621, 1128242]
    },
    'North America': {
        'years': [2012, 2014, 2015],
        'units_sold': [6422, 6954, 5767],
        'profit': [160935, 1152486, 144521]
    },
    'Sub Saharan Africa': {
        'years': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017],
        'units_sold': [5822, 29248, 41254, 26782, 33762, 18842, 3395, 23765],
        'profit': [14031, 1909186, 3456561, 1459049, 2750307, 776344, 298656, 1519074]
    }
}

# Linear Regression Function
def linear_regression(x, y):
    n = len(x)
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
    denominator = sum((xi - x_mean) ** 2 for xi in x)
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    return slope, intercept

# Predict Function
def predict(year, slope, intercept):
    return slope * year + intercept

@app.route('/', methods=['GET', 'POST'])
def index():
    regions = list(data.keys())
    prediction = None
    if request.method == 'POST':
        year = int(request.form['year'])
        region = request.form['region']
        
        region_data = data.get(region)

        if region_data:
            years = region_data['years']
            units_sold = region_data['units_sold']
            profit = region_data['profit']

            # Perform linear regression for units sold
            slope_units_sold, intercept_units_sold = linear_regression(years, units_sold)
            # Perform linear regression for profit
            slope_profit, intercept_profit = linear_regression(years, profit)

            # Predict units sold and profit for the given year
            units_sold_pred = predict(year, slope_units_sold, intercept_units_sold)
            profit_pred = predict(year, slope_profit, intercept_profit)

            # Handle negative predictions
            if units_sold_pred < 0:
                units_sold_pred = 0

            prediction = {
                'units_sold': units_sold_pred,
                'profit': profit_pred
            }
    
    return render_template('index.html', regions=regions, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
