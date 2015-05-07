<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>资料下载 - STM32/STM8技术社区</title>
        <link href="css/basic/ST.css" rel="stylesheet" type="text/css" />
        <link href="css/download/ST.css" rel="stylesheet" type="text/css" />
        <script src="js/jquery.min.js" type="text/javascript"></script>
        <script src="js/gotop.js" type="text/javascript"></script>
        <style type="text/css">
        span.hl_type{display:block;width:200px;background:#99C9FF;}
        table.data_con th.st-td {padding-left:0;text-align:center;}
        a#go-top {
	      background: url(images/gotop.jpg) no-repeat scroll 0 0 #FFFFFF;
	      height: 40px;
	      text-align: center;
	      text-decoration: none;
	      width: 40px;
	    }
	    a#go-top:hover{background-image:url(images/gotop_hover.jpg);}
	    body {
		    background: none;
		    display: table;
		    *position: relative;
		    *min-height: 780px;	
		}
		.body-inner {
		    display: table-cell;
		    vertical-align: middle;
		    *position: absolute;
		    *top: 50%;
		    *margin-top: -390px;
		    _top: 7%;
		    _margin-top: 0;
		}
        </style>
    </head>
<body>
	<div class="body-inner">
		<div class="header">
		    <a href="http://www.stmcu.org/" title="STM32/STM8技术社区" target="_blank" style="float: left; width: 260px; height: 76px; margin-right: 20px;"></a>
		    <img src="images/butterfly.jpg" style="float: left;">
		</div>

		<div class="one clearfix"><a name="top"></a>

		<div class="one_r">
		    <div class="r_box" id="leftmenu" >
		     	  <div class="r_box_t">资料下载（MCU）</div>
			  <div class="r_box_b">
			    <dl>
					<ul>
                    <?php foreach ($cates as $l1 => $l1_data) { ?>
                    <li id="li_one_<?php echo $l1_data['id']; ?>">
                        <span class="blue "><a href="<?php echo $l1_data['id']; ?>.html"><?php echo $l1_data['title']; ?></a></span>
                        <ul id="ul_<?php echo $l1_data['id']; ?>" style="display:none;">
                            <?php foreach ($l1_data['child'] as $l2=>$l2_data) { ?>
                            <li id="li_two_<?php echo $l2_data['id']; ?>">
                                <span class="blue"><a href="javascript:display_ul(<?php echo $l1_data['id']; ?>,<?php echo $l2_data['id']; ?>)"><?php echo $l2_data['title']; ?></a></span>
                                <ul id="zl_<?php echo $l2_data['id']; ?>" style="display:none;">
                                    <?php foreach ($l2_data['child'] as $l3 => $l3_data) { ?>
                                    <ol id="ol_<?php echo $l3_data['id']; ?>">
                                        <a href="#<?php echo $l3_data['id']; ?>" onclick="display_list(<?php echo $l1_data['id']; ?>,<?php echo $l2_data['id']; ?>,<?php echo $l3_data['id']; ?>);"><?php echo $l3_data['title']; ?></a>
                                    </ol>
                                     <?php } ?>
                                </ul>
                            </li>
                            <?php } ?>
                        </ul>
                    </li>
                    <?php } ?>
					</ul>
				</dl>
			  </div>
			  	</div>
			
			<script type="text/javascript">
				<!--  
				//获取对象的初始位置  
				var leftMenuStart = document.getElementById('leftmenu').offsetTop;  
				window.onscroll = function() {  
				    //IE与Mozilla为前者，Chrome取后者的值  
				    var scroll_top = document.documentElement.scrollTop || document.body.scrollTop;   
				    //滚动时分两种情况考虑，再赋值  
				    document.getElementById('leftmenu').style.top = scroll_top > leftMenuStart ? scroll_top - leftMenuStart +10 + 'px' : 0 +'px';  
				}
				var el_two = null;
				var el_three = null;
				function display_ul(id,twoid){
                    if (id && id > 0) {
                        $('#ul_'+id).show();
                    }else{
                        return;
                    }

                    if (!twoid || twoid <= 0){
                        return;
                    }
					var idstr = "zl_"+twoid;


					
					if(el_two==twoid){
						if($("#zl_"+el_two).css('display')=='none'){
							$("#zl_"+el_two).show();
							$("#li_two_"+twoid).css({"background":"url('images/arrow_up.gif') no-repeat scroll left 8px transparent"});
						}else{
							$("#zl_"+el_two).hide();
							$("#li_two_"+twoid).css({"background":"url('images/arrow.gif') no-repeat scroll left 8px transparent"});
						}
					}else{				
						if(el_two && el_two > 0){
							$("#zl_"+el_two).hide();
							$("#li_two_"+el_two).css({"background":"url('images/arrow.gif') no-repeat scroll left 8px transparent"});
						}
						$("#"+idstr).show();
						$("#li_two_"+twoid).css({"background":"url('images/arrow_up.gif') no-repeat scroll left 8px transparent"});
									
						el_two = twoid;			
						display_list_all(twoid);
						if(el_three) $("#ol_"+el_three+" a").css("font-weight","normal");
					}			
				}
				function display_list(id,twoid,threeid){
					var idstr = "list_"+id+"_"+threeid;
					//$("div.data_tit").hide();
					
					$("#title_"+twoid).show();
					$("#"+idstr).show();
					hl_list(threeid);
				}
				function hl_list(threeid){
					if(threeid==el_three) return;
					$("#ol_"+threeid+" a").css("font-weight","bold");
					if(el_three) $("#ol_"+el_three+" a").css("font-weight","normal");
					el_three = threeid;
				}
				function display_list_all(id){
					//$("div.data_tit").hide();
					$("#title_"+id).show();
					$("div.data_tit_"+id).show();
				}
				$(document).ready(function(){
					display_ul(<?php echo $c1; ?>,<?php echo $c2; ?>);
					//$("div.data_tit_"+383).show();
				});
				// -->
			</script>
		</div>
		  
		    <div class="one_l">
			<?php echo $content ?>
			</div>
		</div>
		
		<div style="background-color: #0093dd;">
			<div class="link-more">更多产品资讯，请访问：<a href="http://www.stmcu.org/" title="STM32/STM8技术社区" target="_blannk" style="color: #fff;">www.stmcu.org</a></div>
		</div>

		<div class="nav-st">
			<a class="first" href="http://www.stmcu.org/download/index.php?act=ziliao" target="_blank" title="资料下载"></a>
			<a href="http://www.stmcu.org/download/scheme.php" target="_blank" title="方案荟萃"></a>
			<a href="http://www.stmcu.org/wall/" target="_blank" title="FAQ"></a>
			<a href="http://www.stmcu.org/bbs/forumall_243.html" target="_blank" title="互动论坛"></a>
			<a href="http://www.stmcu.org/video/" target="_blank" title="视 频"></a>
		</div>
	</div>

<script>
/* <![CDATA[ */
(new GoTop()).init({
    pageWidth   :946,
    nodeId      :'go-top',
    nodeWidth   :40,
    distanceToPage  : 20,
    distanceToBottom  :70,
    hideRegionHeight  :70,
    text      :''
});
/* ]]> */
</script>
</body>
</html>
