<?php
define("STORAGE", '/tmp/terrariumpi/');

function save_file($fullPath, $contents, $flags = 0 ) {
  $parts = explode( '/', $fullPath );
  array_pop( $parts );
  $dir = implode( '/', $parts );

  if( !is_dir( $dir ) ) {
    mkdir( $dir, 0777, true );
  }

  file_put_contents( $fullPath, $contents, $flags );
}

// Used for testing/debug. Comment out in production
ob_start();

// Read the data from TerrariumPI
$raw_json_data = file_get_contents('php://input');
// Try to load it to a PHP object from expected JSON data
$php_object = null;
try {
  $php_object = json_decode($raw_json_data,true);
} catch (Exception $e) {
  echo 'Error parsing post data',  $e->getMessage(), "\n";
  return false;
}

// No data received, so stop here.
if (null == $php_object || count($php_object) == 0) {
  return false;
}

// Loop over all the available fields with their data
// Use a nice padding...
$padding = max(array_map('strlen',array_keys($php_object)));
foreach ($php_object as $key => $value) {
  // For now, skip the files, will handle them later on.
  if ('files' != $key) {
    echo "Key: " . str_pad($key, $padding) . " = " . (is_bool($value) ? ($value ? "yes" : "no" ) : "$value") . "\n";
  }
}

// Proces the files
if (key_exists('files',$php_object)) {
  echo "\nSaving " . count($php_object['files']) ." file(s) to disk at location: " . STORAGE . "\n";
  foreach ($php_object['files'] as $file) {
    save_file(STORAGE . $file['name'],base64_decode($file['data']));
    echo "Saved file '" . $file['name'] . "' to disk on location: " . STORAGE . $file['name'] . " with filesize: " . filesize(STORAGE . $file['name']). " bytes\n";
  }
}

// Get debug data. Comment out in production (2 lines)
$data = ob_get_contents();
ob_end_clean();

// Mail debug output Comment out in production
// mail('me@address.com','TerrariumPI WebHook Test',$data);
?>

