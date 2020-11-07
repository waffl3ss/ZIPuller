import requests, time, argparse, cloudscraper, pyfiglet

parser = argparse.ArgumentParser(description='Pull names from ZoomInfo.')
parser.add_argument('-u', dest='companyLink', required=True, help="eg: https://www.zoominfo.com/pic/google-inc/16400573")
parser.add_argument('-o', dest='outputFileName', default='', required=False, help="Output File Name")
parser.add_argument('-pn', dest='printNames', default=False, required=False, help="Print names to screen", action='store_true')
args = parser.parse_args()

companyLink = str(args.companyLink)
outputFileName = str(args.outputFileName)
printNames = args.printNames

def getSession(pageNum):
	zoomInfoSessionFirefox = cloudscraper.CloudScraper(browser={'browser': 'firefox', 'mobile': False, 'platform': 'windows'})
	getURL = str(str(companyLink) + '?pageNum=' + str(pageNum))
	try:
		zoomInfoGetPage = zoomInfoSessionFirefox.get(getURL, allow_redirects=True)
	except cloudscraper.exceptions.CloudflareChallengeError as e:
		print('\n[-] Error encountered, retrying request...\n')
		time.sleep(1)
		try:
			zoomInfoGetPage = zoomInfoSessionFirefox.get(getURL, allow_redirects=True)
		except:
			print('\n[-] Unrecoverable error, exiting...\n')
			pass
	return zoomInfoGetPage

def extractNames(companyLink, outputFileName):
	for pageNum in range(1, 6):
		zoomInfoGetPage = getSession(pageNum)
		zoomInfoResponseSplit = zoomInfoGetPage.text.split('</a>')
		for line in zoomInfoResponseSplit:
			if 'tableRow_personName' in line:
				personName = line.split('class="link amplitudeElement">')[1]
				if printNames:
					print(str(personName))
				if outputFileName != '':
					file = open(outputFileName,"a+")
					print(personName, file = file)
					file.close()
		time.sleep(2)

def main():
	prebanner = pyfiglet.figlet_format('Z.I.Puller')
	banner = prebanner + '   #Waffl3ss\n'
	print("\n" + banner)
	print('[+] Pulling employee names from ZoomInfo\n')
	extractNames(companyLink, outputFileName)

if __name__ == "__main__":
	main()
