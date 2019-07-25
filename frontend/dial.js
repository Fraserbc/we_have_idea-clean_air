var debug = false;

const pi = Math.PI;

// a function for printing an angle in the console (but only if debug is enabled)
function printAngle(name, value) {
	if (!debug) { return; }
	console.log(name.toString() + ": " + (value*(180/pi)).toString());
}

// a function to limit an angle to within 0 to 2pi
function clampAngle(angle) {
	while (angle > pi*2) {
		angle -= pi*2;
	}
	while (angle < 0) {
		angle  += pi*2;
	}
	return angle;
}

var c = document.getElementById("dial");
var ctx = c.getContext("2d");

function drawDial(fillamt, width) {
	
	// calculate the centre of the dial
	var x = width/2;
	var y = width/2;
	
	// make the radius slightly smaller so it fits in the canvas
	var r = width/2.1;
	
	// calculate the line width based on the width so it can scale to any size
	var lineW = width/40;
	
	// clear the canvas
	ctx.clearRect(0, 0, c.width, c.height);
	
	// convert the fill amount from the range 0 to 1000 to the range 0 to 1
	fillamt = fillamt/1000;

	// make sure it is in the range 0 to 1
	if (fillamt > 1) {
		fillamt = 1;
	}
	if (fillamt < 0) {
		fillamt = 0;
	}

	// make the dial fill 3/4 of a circle
	var totalAngle = 270*(pi/180);
	// calculate the start position of the dial
	var startAngle = (pi*3/2)-totalAngle/2;
	// calculate the end position of the dial
	var endAngle = (pi*3/2)+totalAngle/2;
	
	// calculate the angle the dial should fill to
	var finishAngle = totalAngle/2 + totalAngle*fillamt;

	// Draw empty dial
	ctx.beginPath();
	ctx.lineWidth = lineW;
	ctx.strokeStyle = "rgb(63, 63, 63)";
	ctx.arc(x, y, r, startAngle, endAngle);
	ctx.stroke();

	// create a pattern based on the gradient image
	var gradient = ctx.createPattern(document.getElementById("gradient"), "no-repeat");

	// Draw filled dial
	ctx.beginPath();
	ctx.lineWidth = lineW;
	ctx.strokeStyle = gradient;
	ctx.arc(x, y, r, startAngle, finishAngle);
	ctx.stroke();
}
