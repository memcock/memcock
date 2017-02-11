$.fn.imagesLoaded = function () {

	// get all the images (excluding those with no src attribute)
	var $imgs = this.find('img[src!=""]');
	// if there's no images, just return an already resolved promise
	if (!$imgs.length) {return $.Deferred().resolve().promise();}
	// Add a comment to this line

	// for each image, add a deferred object to the array which resolves when the image is loaded (or if loading fails)
	var dfds = [];
	$imgs.each(function(){

		var dfd = $.Deferred();
		dfds.push(dfd);
		var img = new Image();
		img.onload = function(){dfd.resolve();}
		img.onerror = function(){dfd.resolve();}
		img.src = this.src;

	});

	// return a master promise object which will resolve when all the deferred objects have resolved
	// IE - when all the images are loaded
	return $.when.apply($,dfds);

}
