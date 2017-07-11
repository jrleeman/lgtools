from flask import Flask, render_template, redirect, url_for, request, Markup
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField
from wtforms.ext.dateutil.fields import DateTimeField
from wtforms.validators import DataRequired
import datetime
from datetime import timedelta
from longmantide import longmantide
from datetime import datetime
import plotly
from plotly.graph_objs import Scatter, Layout

app = Flask(__name__)
app.secret_key = 'NTOBiFxcjaehKa9nvgTmv5dslPUay7l4QDauEGIV3pSwpZKhpFGqJzestVyGODNT7BL8mauL38xyzgukYV3cIMix9eO8Jgb3bhvo'


class ModelParamsForm(FlaskForm):
    intervalfield = SelectField('Inteval',
                                choices=[(1, '1 minute'), (5, '5 minutes'),
                                         (10, '10 minutes'), (15, '15 minutes'),
                                         (30, '30 minutes'), (60, '1 hour')],
                                default=10)

    startfield = DateTimeField(default=datetime.utcnow() - timedelta(days=3))

    durationfield = FloatField('Duration (days)', default=7)
    lonfield = FloatField('Longitude', default=262.25)
    latfield = FloatField('Latitude', default=30.28)
    elevationfield = FloatField('Elevation', default=190.)
    #start_time = datetime.utcnow() - timedelta(days=3)
    #start_time = datetime(start_time.year, start_time.month, start_time.day, start_time.hour)
    # Set start time
    #startfield.data = start_time


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/longmantide', methods=['GET', 'POST'])
def ltpage():
    form = ModelParamsForm()
    # By default run 3 days before and after the present

    model = longmantide.TideModel()  # Make a model object
    model.increment = 60 * int(form.intervalfield.data)  # Run every 10 minutes
    model.latitude = 30.282  # Station Latitude
    model.longitude = 262.259  # Station Longitude
    model.altitude = 190.  # Station Altitude [meters]
    model.start_time = form.startfield.data
    model.duration = form.durationfield.data  # Model run duration [days]
    model.run_model()  # Do the run

    time = model.results.model_time
    moon = model.results.gravity_moon
    sun = model.results.gravity_sun
    total = model.results.gravity_total

    plot_html = plotly.offline.plot({
                "data": [Scatter(x=time, y=total, name='Total'),
    			         Scatter(x=time, y=moon, name='Moon'),
    					 Scatter(x=time, y=sun, name='Sun')],
                    "layout": Layout(title="Gravitational Tide")
                    }, output_type='div')


    return render_template("longmantide.html", plot_div=Markup(plot_html), model_form = form)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
