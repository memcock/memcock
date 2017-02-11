function sleep (time) {
return new Promise((resolve) => setTimeout(resolve, time));
}

function getNext() {
	if (!$('#next').hasClass('disabled'))
	{
		$('#next').addClass('disabled');
		$.get("/learn/next", function ( data, textStatus, xhr ) {
			if (xhr.status == 200) {
				$('#imageWrapper').hide();
				$('#imageWrapper').html(data).imagesLoaded().then(function(){
					setMaxHeightImages()
					$('#imageWrapper').fadeIn(500, function () {
						placeButton();
						$('#next').show();
						setTimers();

					});
				});
			}
			else {
				window.location.replace("/recall");
			}
		});
	}
};

function enableNext() {
	$('#next').removeClass('disabled')
}
function disableNext() {
	$('#next').addClass('disabled')
}

var minTimer;
var maxTimer;
function setTimers() {
	window.clearTimeout(minTimer);
	window.clearTimeout(maxTimer);
	if (minTime <= 0) {
		enableNext();
	} else if (minTime == maxTime){
		$('#next').hide();
	} else {
		minTimer = setTimeout(function() {
			enableNext();
		}, minTime * 1000);
	}
	if (maxTime  > 0) {
		maxTimer = setTimeout(function() {
			enableNext();
			getNext();
		}, maxTime * 1000)
	}
}

$(function(){
	$(window).resize(function(){
		placeButton();
		setMaxHeightImages()
	});
	placeButton();
	$('#next').addClass('disabled');
	setMaxHeightImages()
	setTimers();
	// hide it before it's positioned
	// $('.btn').css('display','inline');
});

function placeButton() {
	var windHeight = $(window).height();
	var windWidth = $(window).width();
	var buttonHeight = $('.btn').height();
	var buttonWidth = $('.btn').width();
	var tOffset = (parseInt(windHeight) - parseInt(buttonHeight)) - 10;
	var lOffset = (parseInt(windWidth) / 2) - (parseInt(buttonWidth) / 2);
	$('#next').css('top',tOffset);
	// $('.btn').css('left', lOffset);
}

function setMaxHeightImages() {
	var windHeight = $(window).height();
	var navHeight = $('.nav-wrapper').height();
	var height = parseInt(windHeight) - 50;
	//  - parseInt(navHeight)
	$('.responsive').css('max-height', height + 'px')
}

function loadImages(images) {
    images.each(function(){
        $('<img/>')[0].src = this;
    });
}