import requests
import json
import csv
import time

# To Do: 
# - Rotating proxy support

urlinput = input('Enter input text file: ')
with open(urlinput, "r") as urls:
	outputcsv = input('Enter a filename (minus file extension): ') + '.csv'
	seconds = input('Enter number of seconds to wait between URL checks: ')
	usingproxy = input("Using a proxy? Enter 'Yes' or 'No': ")

	if usingproxy == "Yes":
		httporhttps = input('Is the proxy http or https?: ')
		proxyurl = input('Enter a proxy URL (scheme, url, and port): ')
		proxies = { httporhttps : proxyurl }

	google = 'https://structured-data-testing-tool.developers.google.com/sdtt/web/validate'
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
	headers = { 'User-Agent' : user_agent, 'Referer' : 'https://structured-data-testing-tool.developers.google.com/sdtt/web?', 'Origin' : 'https://structured-data-testing-tool.developers.google.com' }

	f = csv.writer(open(outputcsv, "w+", newline="\n", encoding="utf-8"))
	f.writerow(["URL", "Number of Errors"])

	for line in iter(urls):
		values = {'url' : line}
		if usingproxy == "Yes":
			data = requests.post(google, data=values, headers=headers, proxies=proxies, stream=True)
		elif usingproxy == "No":
			data = requests.post(google, data=values, headers=headers)
		else:
			print("You didn't answer 'Yes' or 'No'. Check case. Defaulting to 'No'.")
			data = requests.post(google, data=values, headers=headers)
		data.encoding = 'utf-8'
		respData = data.text
		data = respData[5:]
		j_obj = json.loads(data)
		total = sum(
			int(j_obj['tripleGroups'][i]['numErrors'])
			for i in range(len(j_obj['tripleGroups']))
		)

		f.writerow([j_obj['url'], total])
		print(f"Checked URL: {line}")
		print(f"Waiting {str(seconds)}" + " seconds until checking next URL.\n")
		time.sleep(float(seconds))
print(f"Writing to {outputcsv} complete.")