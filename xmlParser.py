import xml.etree.ElementTree as ET
from flask import Flask, render_template

app = Flask(__name__)

def parsenode(node):
	return {
		"tag": node.tag,
		"value": (node.text or "").strip(),
		"attributes": node.attrib,
		"children": [parsenode(child) for child in node]
	}

def get_cells(node):
	cells=[]
	
	if node["tag"]=="cell":
		cells.append(node)
	for child in node["children"]:
		cells.extend(get_cells(child))
	return cells

def stat_calculation(cells):
	"""Hücrelerin istatistiklerini hesapla"""
	total_cells = len(cells)
	occupied = sum(1 for c in cells if c["attributes"].get("status") == "occupied")
	percentage_parking = (occupied / total_cells * 100) if total_cells > 0 else 0
	return {
		"total_cells": total_cells,
		"occupied": occupied,
		"percentage_parking": percentage_parking
	}

def get_floors(root):
	floors = []
	for floor in root.findall("floor"):
		level = floor.attrib.get("level")
		grid_node = floor.find("grid")
		if grid_node is None:
			continue
		data = parsenode(grid_node)
		cells = get_cells(data)
	
		stats = stat_calculation(cells)
	
		floors.append({
			"level": level,
			"percentage_parking": stats["percentage_parking"],
			"total_cells": stats["total_cells"]
			})
	return floors
def get_otoparklar():
	
	otopark_list =  [
		{"id": 1, "dosya": "data1.xml"},
		{"id": 2, "dosya": "data2.xml"},
		{"id": 3, "dosya": "data3.xml"},
		{"id": 4, "dosya": "data4.xml"},
		{"id": 5, "dosya": "data5.xml"}
	]

	otoparklar = []

	for otopark in otopark_list:
		dosya_yolu = f"example_otopark_data/{otopark['dosya']}"
        
		otopark_data = {
			"id": otopark["id"],
			"isim": f"Otopark {otopark['id']}", 
			"dosya": otopark["dosya"],
			"doluluk": 0
		}

		try:
			tree = ET.parse(dosya_yolu)
			root = tree.getroot()

			otopark_node = root.find("otopark")
			if otopark_node is not None:
				otopark_data["isim"] = otopark_node.attrib.get("name", otopark_data["isim"])
                
				total_cells = 0
				occupied = 0

				for floor in otopark_node.findall("floor"):
					grid_node = floor.find("grid")
					if grid_node is None:
						continue
                    
					data = parsenode(grid_node)
					cells = get_cells(data)

					total_cells += len(cells)
					occupied += sum(1 for c in cells if c["attributes"].get("status") == "occupied")

				percentage = (occupied / total_cells * 100) if total_cells > 0 else 0
				otopark_data["doluluk"] = round(percentage, 2)

		except Exception as e:
			otopark_data["doluluk"] = 0

		otoparklar.append(otopark_data)

	return otoparklar

@app.route("/")
def otopark_listesi():
	otoparklar = get_otoparklar()
	
	return render_template("otoparklar.html", otoparklar=otoparklar)

@app.route("/otopark/<int:id>")
def otopark_detay(id):
	otoparklar = get_otoparklar()
	otopark = next((o for o in otoparklar if o["id"] == id), None)
	
	dosya_yolu = f"example_otopark_data/{otopark['dosya']}"
	tree = ET.parse(dosya_yolu)
	root = tree.getroot()
	
	if not otopark:
		return "Otopark bulunamadı", 404

	floors_percentage_data = []
	
	otopark_node = root.find("otopark")
	if otopark_node is None:
		return "Otopark verisi bulunamadı", 404

	floors_percentage_data = get_floors(otopark_node)
	
	return render_template("home.html", floors=floors_percentage_data, id=id)
    
@app.route("/otopark/<int:id>/floor/<int:level>")
def show_floor(id, level):

	otoparklar = get_otoparklar()
	otopark = next((o for o in otoparklar if o["id"] == id), None)

	if not otopark:
		return "Otopark bulunamadı", 404

	dosya_yolu = f"example_otopark_data/{otopark['dosya']}"
	tree = ET.parse(dosya_yolu)
	root = tree.getroot()

	floor = root.find(f".//floor[@level='{level}']")
	
	if floor is None:
		return "Bu kat yok", 404

	grid_node = floor.find("grid")
	data = parsenode(grid_node)
	cells = get_cells(data)
	stats = stat_calculation(cells)

	return render_template("index.html", node=data, cells=cells, level=level, stats=stats, otopark=otopark)

if __name__ == "__main__":
	app.run(debug=False)