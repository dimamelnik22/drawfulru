var canvas = document.getElementById("paint");
var ctx = canvas.getContext("2d");
var cvs_data = { "pencil": [], "line": [], "rectangle": [], "circle": [], "eraser": [] }; 

function hide_canvas (){
    document.getElementById("paint").style.visibility = "hidden";
}

function clear (){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

$( "p" ).click(function() {
    
    var img_fname = $(this).text();
    
    $("#fname").val(img_fname);

    show_image(img_fname);

});

function show_image (img_name){
    f = '{{files}}';
    for(var key in f){
        alert(img_name + " load");
        if(key == img_name){

            file_data = JSON.parse(f[key]);
            for(var ptool in file_data){

                if(file_data[ptool].length != 0){

                    for(var i = 0; i < file_data[ptool].length; i++){
                        cvs_data[ptool].push(file_data[ptool][i]);
                        shape_draw(ptool, file_data[ptool][i]);
                    }
                }
            }
        }
    }
}

function showImage (name){
    var text = name.replace(/&quot;/g, '\"');
    
    var file_data = JSON.parse(text);
    

    for(var ptool in file_data){

        if(file_data[ptool].length != 0){

            for(var i = 0; i < file_data[ptool].length; i++){
                cvs_data[ptool].push(file_data[ptool][i]);
                shape_draw(ptool, file_data[ptool][i]);

            }
        }
    }

}

function shape_draw (ctool, shape){
    if (ctool == 'pencil'){
        //alert(shape.startx+", "+shape.starty);
        //alert(shape.startx+", "+shape.starty);
        var bg_x = shape.startx, bg_y = shape.starty, x = shape.endx, y = shape.endy;
        ctx.lineWidth = shape.thick;
        ctx.strokeStyle = shape.color;
        ctx.beginPath();
        ctx.moveTo(bg_x, bg_y);
        ctx.lineTo(x, y);
        ctx.stroke();
    }
    else if (ctool == 'line'){
        ctx.beginPath();
        //alert(shape.startx+", "+shape.starty);
        var l_x = shape.startx;
        var l_y = shape.starty;
        //alert(shape.endx+", "+shape.endy);
        var lend_x = shape.endx;
        var lend_y = shape.endy;
        ctx.lineWidth = 2;
        ctx.strokeStyle = "#000000";
        ctx.moveTo(l_x, l_y);
        ctx.lineTo(lend_x, lend_y);
        ctx.stroke();
        ctx.closePath();
    }
    else if (ctool == 'rectangle'){
        var r_x = shape.startx, r_y = shape.starty, width = shape.width, height = shape.height;
        var stroke = shape.stroke, fill = shape.fill;
        ctx.beginPath();
        ctx.strokeStyle = shape.stroke_color;
        ctx.fillStyle = shape.fill_color;
        if(stroke)
            ctx.strokeRect(r_x, r_y, width, height);
        if(fill)
            ctx.fillRect(r_x, r_y, width, height);
        ctx.closePath();
    }
    else if (ctool == 'circle'){
        var c_x = shape.startx, c_y = shape.starty, width = shape.radius, stroke = shape.stroke, fill = shape.fill;
        ctx.beginPath();
        ctx.lineWidth = shape.thick;
        ctx.strokeStyle = shape.stroke_color;
        ctx.fillStyle = shape.fill_color;
        ctx.arc(c_x, c_y, Math.abs(width), 0, 2 * Math.PI, false);
        if (stroke)
            ctx.stroke();
        if (fill)
            ctx.fill();
        ctx.closePath();   
    }
    else if (ctool == 'eraser'){
        var e_x = shape.endx, e_y = shape.endy;
        ctx.lineWidth = shape.thick;
        ctx.clearRect(curX, curY, 20, 20);
    }
}