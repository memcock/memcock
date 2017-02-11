function sleep (time) {
return new Promise((resolve) => setTimeout(resolve, time));
}

function startOver ()
{
	// sad little sissy has to start over :(
	if (failure_mode == 'learning') {
		window.location.replace("/learn");
	}
	if (failure_mode == 'testing') {
		window.location.replace("/recall");
	}
	if (failure_mode == 'everything') {
		window.location.replace("/learn")
	}
}

function newGame ()
{
	// sad little sissy has to start over :(
	window.location.replace("/");
}
function loadNext() {
	$.get("/recall/next", function (data) {
		$('#imageWrapper').fadeOut(1000, function() {
			$('#imageWrapper').html(data).imagesLoaded().then(function(){
				setMaxHeightImages()
				setMaxWidthImages();
				$('.hoverable').click(checkChoice);
				$('#imageWrapper').fadeIn(1000);
			});
		});
	})
}

function checkChoice(event) {
	cockId = $(this).data('cock');
	$.get("/recall/check/" + cockId, function ( data, textStatus, xhr ) {
		if (xhr.status == 200) {
			loadNext();
		}
		else {
			$('#modal-success').openModal({
			  dismissible: false,
			  in_duration: 500,
		  });

		  sleep(5000).then(newGame)
		}
	})
	.fail( function () {
		$('#modal-failure').openModal({
		  dismissible: false,
		  in_duration: 500,
	  	});

	  sleep(5000).then(startOver)
	});
}


$(function(){
	$(window).resize(function(){
		// placeButton();
		setMaxHeightImages();
		setMaxWidthImages();
	});
	// placeButton();
	setMaxHeightImages();
	setMaxWidthImages();
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
	$('.btn').css('top',tOffset);
	// $('.btn').css('left', lOffset);
}

function setMaxHeightImages() {
	var windHeight = $(window).height();
	var navHeight = $('.nav-wrapper').height();
	var height = parseInt(windHeight) - parseInt(navHeight) - 100;
	$('.responsive-choice').css('max-height', height + 'px');
}

function setMaxWidthImages() {
	var windWidth = $(window).width();
	var maxWidth = (parseInt(windWidth) - 30 ) / 4;
	$('.responsive-choice').css('max-width', maxWidth + 'px');
}
