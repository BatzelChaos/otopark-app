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
	
@app.route("/")
def home():
	tree = ET.parse(r"example_otopark_data/data1.xml")
	root = tree.getroot()
	
	floors_percentage_data = []
	
	for floor in root.findall("floor"):
		level = floor.attrib.get("level")
		grid_node=floor.find("grid")
		data = parsenode(grid_node)
		cells = get_cells(data)
		
		stats = stat_calculation(cells)
		
		floors_percentage_data.append({
			"level":level,
			"percentage_parking":stats["percentage_parking"],
			"total_cells":stats["total_cells"]
		})
	return render_template("home.html", floors=floors_percentage_data)


@app.route("/floor/<int:level>")
def show_floor(level):
	tree = ET.parse(r"example_otopark_data/data1.xml")
	root = tree.getroot()
	
	floor = root.find(f"./floor[@level='{level}']")
	if floor is None:
		return "There is no such floor, friend!", 404

	grid_node = floor.find("grid")
	data = parsenode(grid_node)
	cells = get_cells(data)
	
	stats= stat_calculation(cells)
	
	return render_template("index.html", node=data, cells=cells, level=level, stats=stats)
def stat_calculation(cells):
	total_cells = len(cells)
	occupied = sum(1 for c in cells if c["attributes"].get("status") == "occupied")
	#free = sum(1 for c in cells if c["attributes"].get("status") == "free")
	
	percentage_parking = (occupied/total_cells*100) if total_cells > 0 else 0 
	return {
		"percentage_parking":percentage_parking,
		"total_cells":total_cells
	}

app.run(debug=False)