<?php
   // if(isset($_FILES['myfile'])){
   //    $errors= array();
   //    $file_name = $_FILES['myfile']['name'];
   //    $file_size =$_FILES['myfile']['size'];
   //    $file_tmp =$_FILES['myfile']['tmp_name'];
   //    $file_type=$_FILES['myfile']['type'];

   //    print_r($file_name);
   //    $file_ext=strtolower(end(explode('.',$_FILES['image']['name'])));
      
   //    $expensions= array("jpeg","jpg","png");
      
   //    if(in_array($file_ext,$expensions)=== false){
   //       $errors[]="extension not allowed, please choose a JPEG or PNG file.";
   //    }
      
   //    if($file_size > 2097152){
   //       $errors[]='File size must be excately 2 MB';
   //    }
      
   //    if(empty($errors)==true){
   //       move_uploaded_file($file_tmp,"imgStore/".$file_name);
   //       echo "Success";
   //    }else{
   //       print_r($errors);
   //    }
   // }else{
   //    echo "no";
   // }

$uploaddir = 'imgStore/';
$uploadfile = $uploaddir . basename($_FILES['file']['name']);
echo '<pre>';
if (move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile)) {
    echo "Файл корректен и был успешно загружен.\n";
    // Pack JSON with 
} else {
    echo "Возможная атака с помощью файловой загрузки!\n";
}
echo 'Некоторая отладочная информация:';
print_r($_FILES);
print "</pre>";

?>
