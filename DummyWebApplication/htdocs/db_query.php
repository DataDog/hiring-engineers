<?php
	function do_query($min, $max) {	
		$r = rand($min, $max);

# 			$r = 10;	// 0.2 seconds
# 			$r = 30;	// 1.9 seconds
# 			$r = 60;	// 7.5 seconds

		echo "<p>min = $min, max = $max</p>";
		echo "<p>r = $r</p>";
		for ($i = 0; $i < 1000 * $r; $i++) {
			for ($j = 0; $j < 100 * $r; $j++) {
				# wait
			}
		}
	
		return $r;
	}
?>
