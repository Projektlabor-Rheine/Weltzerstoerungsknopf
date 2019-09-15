//Bottom thing
difference() {
    cube([156,18,10]);
    translate([4,6,7]) cube([146,6,4]);
}
//Ontop
difference(){
    translate([0,0,10])
    cube([156,18,5]);
    translate([3,7.4,10])
    cube([150,3.2,10]);
}
//Acrylglas
color([0.9,0,0,0.6])
translate([3,7.5,10])
cube([150,3,70]);

//Top
difference(){
    translate([0,0,75])
    cube([156,18,5]);
    translate([3,7.4,75])
    cube([150,3.2,10]);
}
//Ontop
translate([0,0,80])
cube([156,18,7]);

translate([170,0,0]){
    difference() {
        cube([156,18,10]);
        translate([4,6,7])    cube([146,6,4]);
    }
    translate([0,20,0]){
        //Ontop
        difference(){
            translate([0,0,10])
            cube([156,18,5]);
            translate([3,7.4,10])
            cube([150,3.2,10]);
        }
    }
    translate([0,40,0]){
        //Acrylglas
        color([0.9,0,0,0.6])
        translate([3,7.5,10])
        cube([150,3,70]);
    }
    translate([0,60,0]){
    //Top
        difference(){
            translate([0,0,75])
            cube([156,18,5]);
            translate([3,7.4,75])
            cube([150,3.2,10]);
        }
    }
    translate([0,80,0]){
        //Ontop
        translate([0,0,80])
        cube([156,18,7]);
    }
        
}
