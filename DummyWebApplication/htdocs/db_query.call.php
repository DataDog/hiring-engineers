<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
		<title>Call DB Query</title>
	</head>
	<body>
		<h1>Call DB Query</h1>
		<?php
			include 'db_query.php';
			
			$start_time = microtime(true); 
			
			$r = do_query(10, 30);
			
			$end_time = microtime(true);
			$elapsed_time = $end_time - $start_time;
			echo "<p>start time:   $start_time</p>";
			echo "<p>start time:   $end_time</p>";
			echo "<p>It took:      $elapsed_time seconds</p>";
	
			echo "<p>Done</p>";
		?>
	</body>
</html>

