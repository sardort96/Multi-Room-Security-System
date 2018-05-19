from appfolder import appFlask
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from appfolder.forms import LoginForm, Settings
import RPi.GPIO as GPIO

Bootstrap(appFlask)

@appFlask.route('/', methods=['GET', 'POST'])
def index():	
	form = LoginForm()
	error = None
	if form.validate_on_submit():
		if form.username.data != 'admin' or form.password.data != '12345678':
			error = 'Invalid Credentials. Please try again.'
		else:
			return redirect(url_for('dashboard'))
	return render_template("index.html", form=form, error=error)


@appFlask.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	GPIO.setmode(GPIO.BCM)
	channel = 21
	channel2 = 20
	signal = 0
	signal2 = 0
	GPIO.setup(channel, GPIO.IN)
	GPIO.setup(channel2, GPIO.IN)
	form = Settings()
	message = False
	if form.validate_on_submit():
		GPIO.add_event_detect(channel, GPIO.RISING)
		GPIO.add_event_detect(channel2, GPIO.RISING)
		if form.power.data != True:
			message = False
		else:
			message = True
	while message:
		if GPIO.event_detected(channel):
			signal = 1
			message = False
		elif GPIO.event_detected(channel2):
			signal2 = 1
			message = False
	GPIO.remove_event_detect(channel)
	GPIO.remove_event_detect(channel2)
	return render_template("dashboard.html", form=form, signal=signal, signal2=signal2)


@appFlask.route('/logout')
def logout():
	return redirect(url_for('index'))
