<?php

require 'config.php';

$filename = $_GET['filename'];
$data = $_GET['data'];

$sql = "SELECT data FROM files WHERE filename='$filename'";
$result = mysqli_query ($conn,$sql);
$array = mysqli_fetch_array ($result);

if (isset($array)){
    $sql = "UPDATE files SET data='$data' WHERE filename='$filename'";
    mysqli_query ($conn,$sql);
}
else
{
    $sql = "INSERT INTO files (filename,data) VALUES ('$filename','$data')";
    mysqli_query ($conn,$sql);
}

?>