<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<title>Dummy Web Application</title>
	</head>

	<body>
		<h1>Dummy Web Application</h1>
		<h2>First Page</h2>

		<?php
			include 'db_query.php';

			$start_time = microtime(true); 

			$r = do_query(4, 8);

			$end_time = microtime(true);
			$elapsed_time = $end_time - $start_time;
			echo "<p>start time:   $start_time</p>";
			echo "<p>start time:   $end_time</p>";
			echo "<p>It took:      $elapsed_time seconds</p>";

			# Increment Page Views count
			require './libraries/datadogstatsd.php';
			Datadogstatsd::increment('web.page_views', 1, array('tagname' => 'support', 'tagname' => 'page_01'));

			# Record the page load time
			Datadogstatsd::histogram('web.page_load_time', $elapsed_time, 0.5, array('tagname' => 'support', 'tagname' => 'page_01'));

			echo "<p>Done</p>";
		?>

		<h3>Other Pages</h3>
		<ul>
		<li><a href="page_02.php">Page 02</a></li>
		<li><a href="page_03.php">Page 03</a></li>
		<li><a href="page_04.php">Page 04</a></li>
		<li><a href="page_05.php">Page 05</a></li>
		<li><a href="page_06.php">Page 06</a></li>
		<li><a href="page_07.php">Page 07</a></li>
		<li><a href="page_08.php">Page 08</a></li>
		<li><a href="page_09.php">Page 09</a></li>
		<li><a href="page_10.php">Page 10</a></li>
		</ul>

	</body>
</html>
