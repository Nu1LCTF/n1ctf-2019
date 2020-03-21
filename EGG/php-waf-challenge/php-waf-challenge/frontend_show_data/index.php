<?php
  $mysqli = new mysqli("cd-cdb-kc73wmz2.sql.tencentcdb.com", "root", "c127359176d04cb5d3d475d8e96bf03e09bdcb5d608c6d6167b16b089980ec32", "n1ctf",62865);
  $myquery = $mysqli->query("select * from rank order by score desc , time asc;");
  $rank = 0;
?>
<html>
<head>
    <!-- minify -->
<link href="https://unpkg.com/nes.css@2.2.0/css/nes.min.css" rel="stylesheet" />
<!-- latest -->
<link href="https://unpkg.com/nes.css@latest/css/nes.min.css" rel="stylesheet" />
<!-- core style only -->
<link href="https://unpkg.com/nes.css/css/nes-core.min.css" rel="stylesheet" />
</head>
<body>
<div class="nes-table-responsive">
  <table class="nes-table is-bordered is-dark">
  <tr>
    <th>Rank</th>
    <th>Team</th>
    <th>Best Score</th>
    <th>Last Best Score Change</th>
  </tr>

<?php while ($row = $myquery->fetch_assoc()) { $rank += 1; ?>
   <tr>
     <td><?php echo $rank; ?></td>
     <td><?php echo htmlspecialchars($row["team"]); ?></td>
     <td><?php echo $row["score"];?></td>
     <td><?php echo $row["change"];?></td>
   </tr>
   <?php } ?>
</table>
</div>
</body>
</html>