from bs4 import BeautifulSoup
from decimal import Decimal
import requests
import json
from flask import Flask, request, send_from_directory

app = Flask('scrapper')

all_sale_items = []

@app.route('/')
def index():
  	getClothingItems()
  	return send_from_directory('templates', 'index.html')


def getClothingItems():
	getColumbia()
	getNorthFace()
	getPatagonia()

	with open("static/clothes.json", "w+") as outfile:
		json.dump(all_sale_items, outfile)	


def getCategory(item_name):
	item_name = item_name.lower()

	sweatshirts = ["hoodie", "hoody", "crew", "pullover", "sweater", "1/4", "zip-neck"]
	jackets = ["jacket", "fleece", "windbreaker", "vest", "slicker", "thermoball"]
	coats = ["parka", "gore-tex", "coat", "anorak"]
	shirts = ["shirt", "polo"]
	bottoms = ["pants", "shorts", "tights", "overalls", "boxer"]
	shoes = ["shoe", "boot", "hiker", "sandal"]
	accessories = ["hat", "cap", "trad cap", "booney", "snap back"]

	if [ele for ele in sweatshirts if(ele in item_name)]:
		return "Sweatshirts"
	elif [ele for ele in jackets if(ele in item_name)]:
		return "Jackets"
	elif [ele for ele in coats if(ele in item_name)]:
		return "Coats"
	elif [ele for ele in shirts if(ele in item_name)]:
		return "Shirts"
	elif [ele for ele in bottoms if(ele in item_name)]:
		return "Bottoms"
	elif [ele for ele in shoes if(ele in item_name)]:
		return "Shoes"
	elif [ele for ele in accessories if(ele in item_name)]:
		return "Accessories"
	else:
		return "Other"


def getDepartment(item_name):
	item_name = item_name.lower()

	men = ["men", "m's"]
	women = ["women", "w's"]
	kids = ["kid", "baby", "girls", "boys"]

	if [ele for ele in women if(ele in item_name)]:
		return "Women"
	elif [ele for ele in men if(ele in item_name)]:
		return "Men"
	elif [ele for ele in kids if(ele in item_name)]:
		return "Kids"
	else:
		return "Other"


def getPatagonia():
	patagonia_url = "https://www.patagonia.com/shop/web-specials"
	patagonia_page = requests.get(patagonia_url)
	patagonia_soup = BeautifulSoup(patagonia_page.text, "html.parser")
	patagonia_products = patagonia_soup.findAll("div", {"class": "product-tile__cover"})
	patagonia_sale_prices = patagonia_soup.findAll("span", {"class": "sales"})
	patagonia_retail_prices = patagonia_soup.findAll("span", {"class": "strike-through list"})

	for i in range(0, len(patagonia_products)):
		product_image = patagonia_products[i].find("a").find("img")["data-src"]
		temp_product_name = patagonia_products[i].find("a").find("img")["title"]
		index = temp_product_name.rfind("-")
		product_name = temp_product_name[:index-1]
		sale_price = patagonia_sale_prices[i].find("span")["content"]
		retail_price = patagonia_retail_prices[i].find("span")["content"]
		product_link = patagonia_products[i].find("a")["href"]
		product_type = getCategory(product_name)
		department = getDepartment(product_name)

		json_entry = {
			"product_image": product_image,
			"product_name": product_name,
			"brand": "Patagonia",
			"sale_price": float(sale_price),
			"retail_price": retail_price,
			"product_link": "https://www.patagonia.com/" + product_link,
			"product_type": product_type,
			"department": department
		}

		if json_entry not in all_sale_items:
			all_sale_items.append(json_entry)


def getNorthFace():
	northface_url = "https://www.thenorthface.com/shop/seasonal-sale?facet=&beginIndex=0#facet=&beginIndex=0"
	northface_page = requests.get(northface_url)
	northface_soup = BeautifulSoup(northface_page.text, "html.parser")
	northface_products = northface_soup.findAll("a", {"class": "product-block-name-link"})
	northface_sale_prices = northface_soup.findAll("span", {"class": "product-block-price product-block-current-price current-price product-price-amount-js"})
	northface_retail_prices = northface_soup.findAll("span", {"class": "product-block-price product-block-original-price original-price"})
	northface_product_images = northface_soup.findAll("img", {"class": "product-block-views-selected-view-main-image product-block-views-selected-view-image product-views-selected-view-main-image main-view-js"})

	for i in range(0, len(northface_products)):
		product_image = northface_product_images[i]["srcset"][2:]
		product_name = northface_products[i]["title"]
		sale_price = northface_sale_prices[i]["data-amount"]
		retail_price = northface_retail_prices[i]["data-amount"]
		product_link = northface_products[i]["href"]
		product_type = getCategory(product_name)
		department = getDepartment(product_name)

		json_entry = {
			"product_image": "https://" + product_image,
			"product_name": product_name,
			"brand": "The North Face",
			"sale_price": float(sale_price),
			"retail_price": retail_price,
			"product_link": product_link,
			"product_type": product_type,
			"department": department
		}
		
		if json_entry not in all_sale_items:
			all_sale_items.append(json_entry)


def getColumbia():
	columbia_url = "https://www.columbia.com/sale-discount-outlet/?prefn1=productClass&prefv1=Jackets|Fleece|Insulated|Vests|Footwear|Headwear|Gloves|Accessories|Windbreaker&pgsize=123"
	columbia_page = requests.get(columbia_url)
	columbia_soup = BeautifulSoup(columbia_page.text, "html.parser")
	columbia_products = columbia_soup.findAll("a", {"class": "name-link"})
	columbia_sale_prices = columbia_soup.findAll("div", {"class": "product-discounted-price"})
	columbia_retail_prices = columbia_soup.findAll("span", {"class": "product-standard-price"})
	columbia_product_images = columbia_soup.findAll("img", {"class": "product-image"})
	
	for i in range(0, len(columbia_products)):
		# print(columbia_sale_prices[i])
		product_image = columbia_product_images[i]["src"]
		product_name = columbia_products[i]["title"].replace("\u2122", "")
		sale_price = columbia_sale_prices[i].find("span").text.replace("\n", "")
		retail_price = columbia_retail_prices[i].text.replace("\n", "")
		product_link = columbia_products[i]["href"]
		product_type = getCategory(product_name)
		department = getDepartment(product_name)

		json_entry = {
			"product_image": product_image,
			"product_name": product_name,
			"brand": "Columbia Sportswear",
			"sale_price": float(sale_price[1:]),
			"retail_price": retail_price,
			"product_link": product_link,
			"product_type": product_type,
			"department": department
		}
		
		if json_entry not in all_sale_items:
			all_sale_items.append(json_entry)
    

if __name__ == '__main__':
	app.run()
