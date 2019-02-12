var requestAjax=function(options){

	var object = {
		url:"http://localhost:5000/validate",
		type:"POST",
		datatype:'json',
        crossDomain:true,
	};

	$.extend(object,options);

	$.ajax(object).done(function(data){

		$('.loader').hide();

		if(data==null){
			console.log("No data found!!!");
		}
		else{
			univ.data=data;
			console.log(data['hits']['hits']);

			var result=data['hits']['hits'];
			if(univ.text_tab_detach){
				$(".text_result_cont>.result_Card").detach();
				univ.text_tab_detach=false;
			}
			
			for(key in result)
				processTextTab(result[key]);

			$('.lower').hide();
			$('.upper').hide();

			//console.log(imglist);
		}
	});
}

var processTextTab=function(data){
		
	var abs_path=data._source.abs_path;
	var extension=data._source.extension;
	var filename=data._source.filename;

	imglist.push({
		"filename":filename,
		"extension":extension,
		"abs_path":abs_path,
		"images":data._source.images
	});

	var content = data._source.text_content;

	var result_card = $("<div></div>",{
		"class":"result_Card"
	});

	var card_image_cont=$("<div></div>",{
		"class":"card_sub_cont card_image_cont"
	});

	var card_detail_cont=$("<div></div>",{
		"class":"card_sub_cont card_detail_cont"
	});

	var extension_image = $("<img/>",{
		"src":icon[extension]
	});

	var card_filename = $("<h3></h3>",{
		"text":filename
	});	
	var card_filepath = $("<h4></h4>",{
		"text":abs_path
	});

	var file_path=$("<a></a>",{
		"href":"file:///"+abs_path,
		"class":"file_path",
		"text":"Open File"
	});

	var search_text_cont=$("<div></div>",{
		"class":"search_text_cont"
	});

	var text=getExtraText(data,data.inner_hits.text_content.hits.hits[0]._source.section);

	var upper_para=$("<p></p>",{
		"class":"upper",
		"text":text[0]
	});
	var lower_para=$("<p></p>",{
		"class":"lower",
		"text":text[1]
	});

	var show_up_but=$("<button></button>",{
		"class":"upper_but",
		"text":"Show Upper Part",
		click:function(){$(this).prev().show();$(this).hide();}
	});
	var show_low_but=$("<button></button>",{
		"class":"lower_but",
		"text":"Show Lower Part",
		click:function(){$(this).next().show();$(this).hide();}
	});

	var text_para=$("<p></p>",{
		"class":"main_text",
		"text":data.inner_hits.text_content.hits.hits[0]._source.content
	});

	search_text_cont.append(upper_para);
	search_text_cont.append(show_up_but);
	search_text_cont.append(text_para);
	search_text_cont.append(show_low_but);
	search_text_cont.append(lower_para);

	card_image_cont.append(extension_image);
	card_detail_cont.append(card_filename);
	card_detail_cont.append(card_filepath);
	card_detail_cont.append(file_path);
	card_detail_cont.append(search_text_cont);

	result_card.append(card_image_cont);
	result_card.append(card_detail_cont);

	$(".text_result_cont").append(result_card);
}

var processImageTab=function(){

	if(univ.image_tab_detach){
		$(".image_result_cont>.image_result_Card").detach();
		univ.image_tab_detach=false;

		for(key in imglist){
		//console.log(imglist[key]);

			for(img in imglist[key].images){

				var image_result_card = $("<div></div>",{
					"class":"image_result_Card"
				});

				var image_card_image_cont=$("<div></div>",{
					"class":"image_card_sub_cont image_card_image_cont"
				});

				//if(imglist[key].images[img].split(".")[1]=='png'){
					var file_img=$("<img/>",{
						"src":"file:///"+imglist[key].images[img]
					});

					
				// }
				// else{
				// 	var file_vid=$("<video></video>");
				// 	var source=$("<source/>",{
				// 		"src":"file:///"+imglist[key].images[img],
				// 		"type":"video/m4v"
				// 	});
				// 	file_vid.append(source);
				// 	image_card_image_cont.append(file_vid);
				// }

				var image_card_detail_cont=$("<div></div>",{
					"class":"image_card_sub_cont image_card_detail_cont"
				});

				var detail_sub_cont1=$("<div></div>");
				var detail_sub_cont2=$("<div></div>");

				var exten_img=$("<img/>",{
					"src":icon[imglist[key].extension]
				});

				var img_filename = $("<h3></h3>",{
					"text":imglist[key].filename
				});

				var img_filepath = $("<h4></h4>",{
					"text":imglist[key].abs_path
				});

				detail_sub_cont1.append(exten_img);

				detail_sub_cont2.append(img_filename);
				detail_sub_cont2.append(img_filepath);

				image_card_image_cont.append(file_img);				

				image_card_detail_cont.append(detail_sub_cont1);
				image_card_detail_cont.append(detail_sub_cont2);

				image_result_card.append(image_card_image_cont);
				image_result_card.append(image_card_detail_cont);

				$(".image_result_cont").append(image_result_card);
			}
		}
	}
}

var getExtraText=function(data,index){

	//console.log(data._source.text_content[index]);

	var upper=index-2;
	var lower=index+2;

	if(upper<0){
		upper=0;
	}
	if(lower>data._source.text_content.length){
		lower=data._source.text_content.length-1;
	}

	var text=new Array(2);

	text[0]='';

	for (var i = upper; i <index; i++) {
		text[0]+=data._source.text_content[i].content;	
	}

	text[1]='';

	for (var i = index+1; i <=lower; i++) {
		text[1]+=data._source.text_content[i].content;	
	}

	return text;
}