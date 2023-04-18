<?php
    include_once 'template/database-test.php';
?>

<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        <?php
            $sql = "SELECT * FROM Customer;"; 
            $result  = mysqli_query($conn, $sql); 
            $resultCheck = mysqli_num_rows($result); 

            if ($resultCheck > 0) {
                while ($row = mysqli_fetch_assoc($result)) {
                    echo $row['Customer_ID'] . "<br";
                    echo $row['Customer_Name'] . "<br";
                    echo $row['Reg_Date'] . "<br";
                    echo $row['Customer_Bday'] . "<br";
                    echo $row['Customer_Email'] . "<br";
                    echo $row['Sales_Total'] . "<br";
                    echo $row['Rank'] . "<br";
                    echo $row['Visit_Count'] . "<br";
                    echo $row['Last_Visit_Data'] . "<br";
                }
            }

        ?>
    </body>
</html>

 