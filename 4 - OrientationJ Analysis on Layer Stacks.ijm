
// number of images in stack
Stacksize = 1001;

// into how many stacks of 200 can or should the stack be split (last round is open ended and can be greater than 200) ~ Stacksize/200
Totalloops = 5

// layer polgyon stacks
layer_1 = "D:/Hanna Vasculature/Data Set 3 (V2)/Polygon Stacks/layer1 straight.tif"
layer_2 = "D:/Hanna Vasculature/Data Set 3 (V2)/Polygon Stacks/layer2 straight.tif"
layer_3 = "D:/Hanna Vasculature/Data Set 3 (V2)/Polygon Stacks/layer3 straight.tif"
layer_4 = "D:/Hanna Vasculature/Data Set 3 (V2)/Polygon Stacks/layer4 straight.tif"



function polygon_analysis(file, stacksize, totalloops, layer) { 
	// first slice that is deleted in first loop -> 200+1; deleting the end of the stack
	Forward_delete = 201;
	// last slice that is deleted from the second loop on; deleting the beginning of the stack
	Backward_delete = 0;
	for (i = 0; i < totalloops; i++) {
		
		open(file);
		
		if (i==0) {run("Delete Slice Range", "first=Forward_delete last=stacksize");
		}
		if (i<totalloops-1 && i>0) {		
			run("Delete Slice Range", "first=Forward_delete last=stacksize");
			run("Delete Slice Range", "first=1 last=Backward_delete");
		}
		if (i==totalloops-1) {
			run("Delete Slice Range", "first=1 last=Backward_delete");
		}
		
		run("OrientationJ Distribution", "tensor=6.0 gradient=0 radian=on table=on min-coherency=0.0 min-energy=1.0 ");
		Table.rename("OJ-Distribution-1", "Results");
		
		if (layer==1) {run("Read and Write Excel","sheet=1");}
		if (layer==2) {run("Read and Write Excel","sheet=2");}
		if (layer==3) {run("Read and Write Excel","sheet=3");}
		if (layer==4) {run("Read and Write Excel","sheet=4");}
		
		run("Close All");
		
		Forward_delete = Forward_delete+200;
		Backward_delete = Backward_delete+200;
	}
}

polygon_analysis(layer_1, Stacksize, Totalloops, 1);
polygon_analysis(layer_2, Stacksize, Totalloops, 2);
polygon_analysis(layer_3, Stacksize, Totalloops, 3);
polygon_analysis(layer_4, Stacksize, Totalloops, 4);
