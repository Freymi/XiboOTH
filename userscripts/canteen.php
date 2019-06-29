<?php

header("Content-Type: application/json");

$time = filter_input(INPUT_GET, "time");
$date = date("d.m.Y");
$week = (new DateTime())->format("W");

if($time == "noon") {
	$data = file_get_contents_utf8("http://www.stwno.de/infomax/daten-extern/csv/HS-R-tag/" . $week . ".csv");
} else if($time == "evening") {
	$data = file_get_contents_utf8("http://www.stwno.de/infomax/daten-extern/csv/HS-R-abend/" . $week . ".csv");
} else {
	die(json_encode(array("error" => "Missing or wrong time parameter. Possible values: noon, evening")));
}

$rows = explode("\n", $data);

for($i = 1; $i < sizeof($rows); $i++) {
    if(trim($rows[$i]) !== '') {
        $arr = str_getcsv($rows[$i], ";");
        if($arr[0] == $date) {
            if(substr($arr[2], 0, 2) == "HG") {
                $arr[2] = "Hauptgericht";
            } else if(substr($arr[2], 0, 1) == "B") {
                $arr[2] = "Beilage";
            } else if(substr($arr[2], 0, 1) == "N") {
                $arr[2] = "Nachspeise";
            }
            $csv[] = $arr;
        }
    }
}

$finalArray = array();
$finalArray['data'] = $csv;

echo json_encode($finalArray);

function file_get_contents_utf8($fn) {
     $content = file_get_contents($fn);
      return mb_convert_encoding($content, 'UTF-8',
          mb_detect_encoding($content, 'UTF-8, ISO-8859-1', true));
}

?>
