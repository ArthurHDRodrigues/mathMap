from bs4 import BeautifulSoup

def main():
	name = input("nome do file:")
	if name == "":
		name = "zbMATH.html"
	with open(name) as fp:
		soup = BeautifulSoup(fp, 'html.parser')
	list = soup.find_all('div')

	for div in list:
		if div.get("class") == ['left']:
			left = print(div)
		if div.get("class") == ['center']:
			center = print(div)
		if div.get("class") == ['right']:
			right = print(div)

main()
