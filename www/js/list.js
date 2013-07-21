var serviceURL = "http://www.digitalissimo.it";

getlist();
function getlist() {
  $.ajax({
       url:serviceURL + "?json=1",
       dataType:"jsonp",
       success:function(result){
           posts = result.posts;
           console.log(posts);

           
           $('.ui-content ul li').remove();
           var category = "";
           $.each(posts, function(index, post) {
                cate = "";
                $.each(post.categories, function(index, category) {
                    cate += category.title + " "; 
                });
                $('.ui-content ul').append('<li data-form="ui-btn-up-a" data-swatch="a" data-theme="a" class="ui-li ui-li-static ui-btn-up-a"><img src="' + post.thumbnail + '" />'
                      + '<h1><a href="' + post.url + '" class="ui-link" target="_new">' + post.title + '</a></h1">'
                      + '<p>' + cate + '</p>'
                      + '</li>');
           });
           
           $(".ui-content ul").listview ("refresh");
              
           $(".ui-icon-loading").hide();
           
       };
       
       error: function(request,error) 	{
		   $('.ui-content ul').append ("<li>" + error + "</li>" );
		}
       
       
       
  });
    
}