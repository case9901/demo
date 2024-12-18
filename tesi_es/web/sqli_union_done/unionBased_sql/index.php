<?php
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

if (isset($_GET['search'])) {
    $search = $_GET['search'];
    $sql = "SELECT name, description, price, image FROM products WHERE name LIKE '%$search%'";

    // Gestione degli errori con try-catch
    try {
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            echo "<table><tr><th>Name</th><th>Description</th><th>Price</th><th>Image</th></tr>";
            while ($row = $result->fetch_assoc()) {
                echo "<tr><td>" . $row["name"] . "</td><td>" . $row["description"] . "</td><td>" . $row["price"] . "</td><td><img src='" . $row["image"] . "' alt='" . $row["name"] . "' width='100'></td></tr>";
            }
            echo "</table>";
        } else {
            echo "0 risultati";
        }
    } catch (mysqli_sql_exception $e) {
        echo "Errore nella query SQL: " . $e->getMessage();
    }
}
?>

<form method="get">
    <p>Benvenuto alla Banca Dati Segreta dei Ninja di Konoha. Usa il campo di ricerca per trovare attrezzature ninja.</p>
    <input type="text" name="search" placeholder="Cerca attrezzature ninja...">
    <input type="submit" value="Cerca">
</form>


