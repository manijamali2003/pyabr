<?php

require 'config.php';

$filename = $_GET['filename'];
$sql = "SELECT data FROM files WHERE filename='$filename'";
$result = mysqli_query ($conn,$sql);
$array = mysqli_fetch_array ($result);

if (isset($array)){
    $data = $array[0];
    echo $data;
}
else
{
    exit ("file not found.");
}

?>