@echo off
title Senior Dev Engine - Proje Kurulumu
color 0b
echo [Senior Dev Engine] Modern Admin Paneli İskeleti Oluşturuluyor...
echo.

:: Klasör Yapısı Oluşturma
mkdir "src\layouts" 2>nul
mkdir "src\pages\admin" 2>nul
mkdir "src\components\admin" 2>nul
mkdir "src\lib" 2>nul
mkdir "bot_engine" 2>nul
mkdir "public\assets\admin" 2>nul
mkdir "scripts" 2>nul

:: Layouts
echo. > "src\layouts\AdminLayout.astro"
echo [+] Oluşturuldu: src\layouts\AdminLayout.astro

:: Pages (Ana Özellikler)
echo. > "src\pages\admin\dashboard.astro"
echo. > "src\pages\admin\bot-control.astro"
echo. > "src\pages\admin\content-gen.astro"
echo. > "src\pages\admin\scheduler.astro"
echo. > "src\pages\admin\seo-center.astro"
echo. > "src\pages\admin\settings.astro"
echo. > "src\pages\admin\analytics.astro"
echo. > "src\pages\admin\media.astro"
echo [+] Sayfa dosyaları oluşturuldu.

:: Components
echo. > "src\components\admin\Sidebar.astro"
echo. > "src\components\admin\TopBar.astro"
echo. > "src\components\admin\StatCard.astro"
echo. > "src\components\admin\NotificationCenter.astro"
echo. > "src\components\admin\Editor.astro"
echo. > "src\components\admin\WidgetManager.astro"
echo [+] Bileşen dosyaları oluşturuldu.

:: Lib / Backend Logic
echo. > "src\lib\api-vault.ts"
echo. > "src\lib\db-cleaner.ts"
echo. > "src\lib\auth.ts"
echo. > "src\lib\index-tracker.ts"
echo [+] Kütüphane dosyaları oluşturuldu.

:: Bot Engine (Python)
echo. > "bot_engine\core.py"
echo. > "bot_engine\image_gen.py"
echo. > "bot_engine\trend_tracker.py"
echo. > "bot_engine\git_handler.py"
echo. > "bot_engine\forum_bot.py"
echo [+] Bot motoru dosyaları oluşturuldu.

echo.
echo ---------------------------------------------------
echo Iskelet Basariyla Hazirlandi!
echo Simdi sirayla iclerini doldurmaya gecebiliriz.
echo ---------------------------------------------------
pause