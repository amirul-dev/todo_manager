import datetime

def rem_time_calc(f):
	if f[4]=='checked':
		return '', 'Done'
	else:
		due_date = datetime.datetime.strptime(f[2], '%Y-%m-%d')
		dt = f[3].split(':')
		due_time = datetime.timedelta(hours=int(dt[0]), minutes=int(dt[1]))
		due_datetime = due_date+due_time
		current_datetime = datetime.datetime.now()
		rem_time = due_datetime - current_datetime
		days = abs(rem_time.days)
		seconds = rem_time.seconds
		hours = seconds//3600
		minutes = (seconds//60)%60
		if days==0:
			rem_time = f'{hours}hrs, {minutes}mins'
		else:
			rem_time = f'{days}days, {hours}hrs, {minutes}mins'
		if due_datetime > current_datetime:
			status = 'Due'
		else:
			status = 'Overdue'
		return ' by : '+rem_time, status

def check_overdue(due_date, due_time,status):
	if status=='checked':
		return ''
	else:
		due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d')
		dt = due_time.split(':')
		due_time = datetime.timedelta(hours=int(dt[0]), minutes=int(dt[1]))
		due_datetime = due_date+due_time
		current_datetime = datetime.datetime.now()
		if due_datetime < current_datetime:
			status = 'Overdue'
			return status
	
def format_date(d):
	d = datetime.datetime.strptime(str(d), '%Y-%m-%d')
	d = d.strftime("%a - %b %d, %Y")
	return d

def format_time(t):
	t = datetime.datetime.strptime(t, "%H:%M")
	t = t.strftime("%I:%M %p")
	return t
