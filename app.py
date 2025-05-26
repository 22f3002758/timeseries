from flask import Flask, request,redirect,render_template
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("agg")

app=Flask(__name__)


month="2013-01-01"

@app.route('/',methods=['GET','POST'])

def fcast():
    if request.method=='GET':
        return render_template('index.html')
    month=request.form.get('month')
    year=request.form.get('year')
    d=year+"-"+month+"-"+"01"
    file = open("Sales-forecast.csv", "r")
    lines = file.readlines()
    f=""
    for line in lines:
        if line.strip().split(",")[-1] == d:
            f = round(float(line.strip().split(",")[-2]),2)

    

    # Load your dataset
    df = pd.read_csv("Sales-forecast.csv")  # Replace with your filename
    df['Month'] = pd.to_datetime(df['Month'])

    # Constants
    cutoff_date = pd.to_datetime("2005-12-01")

    # Get user input
    
    user_date = pd.to_datetime(d)

    # Split data
    train_data = df[df['Month'] <= cutoff_date]
    forecast_data = df[(df['Month'] > cutoff_date) & (df['Month'] <= user_date)]

    # Plotting
    plt.figure(figsize=(12, 6))

    # Plot training sales
    plt.plot(train_data['Month'], train_data['Sales'], color='blue', label='Training Sales')

    # Plot forecast if any
    if not forecast_data.empty and forecast_data['forecast'].notna().any():
        plt.plot(forecast_data['Month'], forecast_data['forecast'], color='orange',
                linestyle='--', label='Forecast')

    # Highlight user date
    if user_date in df['Month'].values:
        y_val = df.loc[df['Month'] == user_date, 'forecast'].values[0]
        if pd.notna(y_val):
            plt.plot(user_date, y_val, 'ro', label=d)

    # Formatting
    plt.title("Sales and Forecast Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("./static/trend_chart.png")
    plt.close()


        
    return render_template('index.html',Result=f,p="./static/trend_chart.png",y=d.split("-")[0],d=d.split("-")[1])       

if __name__=='__main__':
    app.run(debug=True)
