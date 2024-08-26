<?php 

include_once "lib/html/include.php"; 

initProgram('admin');

$login->loadAllObjects('client');
$list = $login->getList('client');

log_cleanup("Fixing Mail Outgoing IP", $nolog);

$t = '';

$flgfile = "/usr/local/lxlabs/kloxo/etc/flag/manualoutgoingips.flg";

/*Note to remap ips for AWS or NAT hosting include pairs public_ip:internal_ip in file
eg. 
203.23.45.23:192.168.0.23
201.43.42.2:10.0.10.1
*/
$process=1;
$ipmap=array();
if (file_exists($flgfile)) {
	$ipsmap = file($flgfile);
	foreach($ipsmap as $iprow) {
		$ips = explode(':',$iprow);
		$ipmap[$ips[0]] = trim($ips[1]);
	}
	if(empty($ipmap)){
		$process=0;
	}
	else
	{
		print("- File '{$flgfile}' exists with ip remapping data\n");
	}	
	
}	
	
if(!$process){
		print("- No process because empty '{$flgfile}' exists\n");
} else {
	
	foreach($list as $c) {
		$dlist = $c->getList('domain');

		foreach($dlist as $l) {
			$dns = $l->getObject('dns');

			foreach($dns->dns_record_a as $drec) {
				if (($drec->ttype === 'a') && ($drec->hostname === '__base__')) {
					print("- For '{$dns->nname}' ('{$c->nname}') at '{$c->syncserver}'\n");

					if (stripos($drec->param, ":") !== false) {
						$ip = "[{$drec->param}]";
					} else {
						$ip = $drec->param;
					}
					if(array_key_exists($ip,$ipmap)){
						print("  map '{$ip}' to $ipmap[$ip]\n");
						$ip=trim($ipmap[$ip]);
					}
					
					$t .= "{$dns->nname}:{$ip}\n";
				}
			}

			$dns->was();
		}
	
		file_put_contents("/var/qmail/control/outgoingips", $t);
	}
}

