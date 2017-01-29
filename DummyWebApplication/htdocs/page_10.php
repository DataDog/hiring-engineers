<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
		<title>Page 10</title>
	</head>
	<body>
		<h1>Page 10</h1>
		<?php
			include 'db_query.php';
			
			$start_time = microtime(true); 
			
			$r = do_query(10, 12);
			
			$end_time = microtime(true);
			$elapsed_time = $end_time - $start_time;
			echo "<p>start time:   $start_time</p>";
			echo "<p>start time:   $end_time</p>";
			echo "<p>It took:      $elapsed_time seconds</p>";
	
	  		# Increment Page Views count
	  	  	require './libraries/datadogstatsd.php';
  			Datadogstatsd::increment('web.page_views', 1, array('tagname' => 'support', 'tagname' => 'page_10'));
  			
  			# Record the page load time
  			Datadogstatsd::histogram('web.page_load_time', $elapsed_time, 0.5, array('tagname' => 'support', 'tagname' => 'page_10'));
  			
			echo "<p>Done</p>";
		?>
	</body>
</html>
