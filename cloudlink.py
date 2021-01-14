import requests
import datetime

JWT = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IjdZVzRJODB3Um8ySVJiQVZFUG9rSnciLCJleHAiOjE2NDI1MzU3NjAsImlhdCI6MTYxMDM5NTAyMn0.Kq2mrMvPrc8Ybeqlh-7x4awRak-BiKWSEztFBJTzers'

# Put your USER ID that you get from the API.
USERID = 'vBmFSXYwQcCkjmRTGIasKw'

headers = {
		'Authorization':
		'Bearer {}'.format(JWT),
		'content-type':
		'application/json',
	}

# Put your own download path here, I used an external hard drive so mine will differ from yours
PATH = '/Users/nicky/zoomdl'



def main():
	for year in range(2018,2022):
		for month in range(1,13):
			next_month = month + 1
			next_year = year

			if month == 12:
				next_month = 1
				next_year = year + 1

			start_date = datetime.datetime(year,month,1)
			next_date = datetime.datetime(next_year,next_month,1)

			get_recording(start_date, next_date)


def get_recording(start_date, next_date):

	date_string = '%Y-%m-%d'
	url = 'https://api.zoom.us/v2/users/{}/recordings?from={}&to={}&page_size=300&'.format(
				USERID,
				start_date.strftime(date_string),
				next_date.strftime(date_string)
			)

	print(url)

	response = requests.get(
		url,
		headers=headers
	)

	data = response.json()
	# print('page_count: ', data['page_count'])
	# print('page_size: ', data['page_size'])
	# print(len(data['meetings']))
	# print(data['from'])
	# print(data['to'])

	if 'meetings' in data:
		for meeting in data['meetings']:
			for record in meeting['recording_files']:
				if record['status'] != 'completed':
					continue

				download_recording(
					record['download_url'],
					record['recording_start'].replace(':','-')
				)
	else:
		print("No meetings in: ", url)


def download_recording(download_url, filename):
	print(download_url)
	download_access_url = '{}?access_token={}'.format(download_url, JWT)
	response = requests.get(download_access_url, stream=True)
	local_filename = '{}{}.mp4'.format(PATH, filename)

	with open(local_filename, 'wb') as f:
		for chunk in response.iter_content(chunk_size=8192):
			f.write(chunk)


if __name__ == '__main__':
	main()
