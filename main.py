import json
from datetime import datetime

def transform_forecasts(*forecast_tuples):
    result = []

    # Split the input data into min and max parts
    min_forecasts = [item.split('@') for item in forecast_tuples[0].replace('{', '').replace('}', '').split(', ')]
    max_forecasts = [item.split('@') for item in forecast_tuples[1].replace('{', '').replace('}', '').split(', ')]

    # Iterate through min and max forecast data simultaneously
    for min_data, max_data in zip(min_forecasts, max_forecasts):
        date_min = datetime.strptime(min_data[1][:10], '%Y-%m-%d').date()

        # Extract min and max forecast values
        min_forecasted = int(min_data[0])
        max_forecasted = int(max_data[0])

        result.append({
            "date": date_min.strftime('%Y-%m-%d'),
            "min-forecasted": min_forecasted,
            "max-forecasted": max_forecasted
        })

    return json.dumps(result, indent=2)

# Example usage:
input_data = ('14@2018-01-01 08:00:00+01, 15@2018-01-02 08:05:00+01, 16@2018-01-03 08:10:00+01',
              '17@2018-01-01 08:00:00+01, 17.5@2018-01-02 08:05:00+01, 18@2018-01-03 08:10:00+01')

output_json = transform_forecasts(*input_data)
print(output_json)
