<?php

header("Content-Type: application/json");

$command = escapeshellcmd('/usr/bin/python3 /opt/CipPools/untis2.py');
$output = shell_exec($command);
echo $output;
