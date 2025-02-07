from flask import Flask, render_template, request
import calendar
from datetime import datetime

app = Flask(__name__)

# Calculate working days
def calculate_working_days(month):
    year = 2025
    working_days = 0

    # Iterate through the working days of the month
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        date = datetime(year, month, day)

        if date.weekday() < 5:
            working_days += 1
    return working_days

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            month = int(request.form['mes'])
            deducted_days = int(request.form['dias_restados'])

            if month < 1 or month > 12:
                raise ValueError("The month must be between 1 and 12")

            working_days = calculate_working_days(month)
            remaining_working_days = working_days - deducted_days
            if remaining_working_days < 0:
                raise ValueError("The deducted working days cannot be greater than the total working days.")

            day_percentage = remaining_working_days * 0.40
            working_hours = remaining_working_days * 8
            hour_percentage = working_hours * 0.40

            return render_template('index.html', resultado=True, working_days=working_days,
                                   remaining_working_days=remaining_working_days,
                                   day_percentage=day_percentage, hour_percentage=hour_percentage)
        except ValueError as error:
            return render_template('index.html', error=str(error))

    return render_template('index.html', resultado=False)

if __name__ == '__main__':
    app.run(debug=True)
