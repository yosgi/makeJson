 <div class="data_tit  data_tit_<?php echo $c2_id;?>" style="margin:0;" id="list_<?php echo $c1_id;?>_<?php echo $c3_id;?>">
 	<table width="100%" border="0" cellspacing="0" cellpadding="0">
 		<tr>
 			<td><span class="white"><a name="<?php echo $c3_id;?>" style="margin-left:10px;" href="javascript:void(0);"><?php echo $c3_name; ?></a></span></td>
 			<td><div align="right"><span class="white"><a href="#top" style="margin-right:10px;">#top</a></span></div></td>
 		</tr>
 	</table>
 	<table class="data_con" border="0" cellpadding="0" cellspacing="0" style="float:left; margin:0; color:#000; font-family:Arial, Helvetica, sans-serif; color:#000;">
 		<tr>
 			<th width="234" align="left">索引</th>
 			<th width="60" align="center" class="st-td">文档版本</th>
 			<th width="80" align="center" class="st-td">发布时间</th>
 			<th width="90" align="center" class="st-td">英文文档</th>
 			<th width="90" align="center" class="st-td">中文译文</th>
 			<th width="90" align="center" class="st-td">附件</th>
 			<th width="60" align="center" class="noline st-td">附件版本</th>
 		</tr>
 		<?php foreach($c3_docs as $k=>$dt) { ?>			
 		<tr class="blue1">
 			<td style="background:#fff;"><?php echo $dt['title']; ?></td>
 			<td align="center" style="background:#fff;"><?php echo $dt['version']; ?></td>
 			<td align="center" style="background:#fff;"><?php $date = (!empty($dt['time_update'])? $dt['time_update']:$dt['time_create'] ); echo date('Y/m',$date); ?></td>
 			<td align="center" style="background:#fff;">
 				<?php if (!empty($dt['file_en'])) {  
 					foreach ($dt['file_en'] as $file) { ?>
 					<a href="<?php echo $file['fileurl'];?>"  target="_blank" class="txtline" title="<?php echo $file['title'];?>">
 						<img src="images/ico/<?php echo $file['ico'];?>" alt="" align="absmiddle" /></a>
 				<?php }
 					 }else{
 						echo "无";
 					 } 
 				?>
 			</td>
 			<td align="center" style="background:#fff;">
 				<?php if (!empty($dt['file_cn'])) {  
 						foreach ($dt['file_cn'] as $file) { ?>

 						<a href="<?php echo $file['fileurl'];?>"  target="_blank" class="txtline" title="<?php echo $file['title'];?>">
 							<img src="images/ico/<?php echo $file['ico'];?>" alt="" align="absmiddle" /></a>
 				<?php }
 					}else{
 							echo "无";
 					} 
 				?>
 			</td>
 			<td align="center"  style="background:#fff;">

 				<?php if (!empty($dt['file_attachment'])) {  
 					foreach ($dt['file_attachment'] as $file) { ?>

 						<a href="<?php echo $file['fileurl'];?>"  target="_blank" class="txtline" title="<?php echo $file['title'];?>">
 								<img src="images/ico/<?php echo $file['ico'];?>" alt="" align="absmiddle" /></a>
 				<?php }
 					}else{
 						echo "无";
 					} 
 				?>					  			  	  			  
 			</td>
 			<td align="center"  class="noline" style="background:#fff;"><?php echo $dt['att_version'];?></td>	
 			</tr>
 			<tr class="blue1">
 				<td colspan="7" style="background:#fff; border-bottom:1px dotted #000; padding-bottom:8px;color:#000;">
 					文档说明：<?php echo $dt['description'];?>
 				</td>
 			</tr>
 			<?php } ?>	
 	</table>		
 </div>