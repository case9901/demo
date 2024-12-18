<?php
session_start();

if ($_SESSION['username'] == 'admin') {
    echo "Flag: flag{secret_flag}";
} else {
    echo "Accesso negato";
}
?>

