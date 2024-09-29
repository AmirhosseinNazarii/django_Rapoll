<?php
// ایجاد ارتباط با دیتابیس
$servername = "localhost";
$username = "rapoll_ADprofira";
$password = "Amir1014Amir1014";
$dbname = "rapoll_Profira";

// اتصال به دیتابیس
$conn = new mysqli($servername, $username, $password, $dbname);

// بررسی ارتباط
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // ولیدیشن ایمیل
    if (isset($_POST['email']) && filter_var($_POST['email'], FILTER_VALIDATE_EMAIL)) {
        $email = htmlspecialchars(trim($_POST['email']));

        // آماده کردن کوئری برای جلوگیری از حملات SQL Injection
        $stmt = $conn->prepare("INSERT INTO UsersEmails (email) VALUES (?)");
        if ($stmt) {
            $stmt->bind_param("s", $email);

            // اجرای کوئری و بررسی نتیجه
            if ($stmt->execute()) {
                echo "ایمیل شما با موفقیت ثبت شد.";
            } else {
                // بررسی تکراری بودن ایمیل
                if ($conn->errno == 1062) {
                    echo "این ایمیل قبلاً ثبت شده است.";
                } else {
                    echo "مشکلی در ثبت ایمیل شما رخ داده است. لطفاً دوباره تلاش کنید.";
                }
            }

            $stmt->close();
        } else {
            echo "خطا در آماده‌سازی کوئری.";
        }
    } else {
        echo "لطفاً یک ایمیل معتبر وارد کنید.";
    }
}

$conn->close();
?>
