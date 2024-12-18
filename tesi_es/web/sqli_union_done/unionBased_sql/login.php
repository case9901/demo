l<?php
session_start();
$servername = "localhost";
$username = "root";
$unix_socket = "/var/run/mysqld/mysqld.sock";
$dbname = "naruto_db";

// Crea connessione
$conn = new mysqli($servername, $username, '', $dbname, null, $unix_socket);

// Controlla connessione
if ($conn->connect_error) {
    die("Connessione fallita: " . $conn->connect_error);
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    $sql = "SELECT * FROM users WHERE username='$username' AND password='$password'";
    $result = $conn->query($sql);

    if ($result->num_rows == 1) {
        $_SESSION['username'] = $username;
        header('Location: flag.php');
        exit();
    } else {
        echo "Credenziali non valide";
    }
}
?>

<form method="post">
    <p>Solo i veri ninja possono accedere alle informazioni segrete. Inserisci le tue credenziali per entrare.</p>
    <input type="text" name="username" placeholder="Nome Utente">
    <input type="password" name="password" placeholder="Password">
    <input type="submit" value="Accedi">
</form>

