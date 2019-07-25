var debug = false;

const pi = Math.PI;

function printAngle(name, value) {
	if (!debug) { return; }
	console.log(name.toString() + ": " + (value*(180/pi)).toString());
}

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
	var x = width/2;
	var y = width/2;

	var r = width/2.1;

	var lineW = width/40;

	ctx.clearRect(0, 0, c.width, c.height);

	fillamt = fillamt/1000;

	if (fillamt > 1) {
		fillamt = 1;
	}
	if (fillamt < 0) {
		fillamt = 0;
	}

	var totalAngle = 270*(pi/180);
	var startAngle = (pi*3/2)-totalAngle/2;
	var endAngle = (pi*3/2)+totalAngle/2;
	var totalLength = 2*pi*r*(totalAngle/(2*pi));

	var finishAngle = totalAngle/2 + totalAngle*fillamt;

	// Draw empty dial
	ctx.beginPath();
	ctx.lineWidth = lineW;
	ctx.strokeStyle = "rgb(63, 63, 63)";
	ctx.arc(x, y, r, startAngle, endAngle);
	ctx.stroke();

	var gradient = ctx.createPattern(document.getElementById("gradient"), "no-repeat");

	// Draw filled dial
	ctx.beginPath();
	ctx.lineWidth = lineW;
	ctx.strokeStyle = gradient;
	ctx.arc(x, y, r, startAngle, finishAngle);
	ctx.stroke();
}
