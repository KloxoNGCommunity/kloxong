<?php 

include_once "lib/html/include.php";

if (!os_isSelfSystemOrLxlabsUser()) {
	print("Must be Root \n");

	exit;
}

if (!isset($argv[1])) {
	print("Usage: $argv[0] <master/slave> <password>\n");
	exit;
}

if ($argv[1] === 'master') {
	initProgram('admin');
	$login->password = crypt($argv[2], '$1$'.randomString(8).'$');
	$login->realpass = $argv[2];
	$login->setUpdateSubaction('password');
	$login->createSyncClass();
	$login->was();
} else if ($argv[1] === 'slave') {
	if (!lxfile_exists("$sgbl->__path_slave_db")) {
		print("Not Slave\n");

		exit;
		}
	$rmt = unserialize(lfile_get_contents("$sgbl->__path_slave_db"));
	$rmt->password = crypt($argv[2], '$1$'.randomString(8).'$');
	lfile_put_contents("$sgbl->__path_slave_db", serialize($rmt));
} else {
	print("first argument is master/slave\n");

	exit;
}
