

Table.open("C:/Users/i6235702/Desktop/V1 Layer4 StraightCoor.csv");


stacksize = 1001


newImage("Straight Stack", "8-bit grayscale-mode", 2048, 1000, 1, 1001, 1);
open("D:/Hanna Vasculature/Data Set 3 (V2)/Polygon Stacks/layer4.tif");


for (imagenumber = 1; imagenumber < stacksize+1; imagenumber++){
	x1 = Table.get("C2", imagenumber);
	y1 = Table.get("C3",imagenumber);
	x2 = Table.get("C4",imagenumber);
	y2 = Table.get("C5",imagenumber);
	x3 = Table.get("C6",imagenumber);
	y3 = Table.get("C7",imagenumber);
	x4 = Table.get("C8",imagenumber);
	y4 = Table.get("C9",imagenumber);
	x5 = Table.get("C10",imagenumber);
	y5 = Table.get("C11",imagenumber);
	x6 = Table.get("C12",imagenumber);
	y6 = Table.get("C13",imagenumber);
	x7 = Table.get("C14",imagenumber);
	y7 = Table.get("C15",imagenumber);
	x8 = Table.get("C16",imagenumber);
	y8 = Table.get("C17",imagenumber);
	x9 = Table.get("C18",imagenumber);
	y9 = Table.get("C19",imagenumber);
	x10 = Table.get("C20",imagenumber);
	y10 = Table.get("C21",imagenumber);
	x11 = Table.get("C22",imagenumber);
	y11 = Table.get("C23",imagenumber);
	x12 = Table.get("C24",imagenumber);
	y12 = Table.get("C25",imagenumber);
	x13 = Table.get("C26",imagenumber);
	y13 = Table.get("C27",imagenumber);
	
	setForegroundColor(0, 0, 0);
	selectWindow("layer4.tif");
	setSlice(imagenumber);
	makeLine(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,x8,y8,x9,y9,x10,y10,x11,y11,x12,y12,x13,y13);
	run("Straighten...", "title=straight.tif line=1000");
	selectWindow("straight.tif");
	run("Copy");
	selectWindow("Straight Stack");
	setSlice(imagenumber);
	run("Paste");
	selectWindow("straight.tif");
	close();
	
}


