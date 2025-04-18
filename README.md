# Simple Ecommerce

一個基於Django和Bootstrap的簡易電子商務網站。

## 功能

- 產品列表與分類瀏覽
- 產品詳情頁
- 購物車功能
- 響應式設計

## 技術棧

- Django 4.2
- Bootstrap 5
- SQLite

## 安裝與運行

1. 克隆此代碼庫
2. 創建並激活虛擬環境：
   ```
   python -m venv venv
   source venv/bin/activate  # Windows 使用 venv\Scripts\activate
   ```
3. 安裝依賴：
   ```
   pip install -r requirements.txt
   ```
4. 進行數據庫遷移：
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
5. 創建超級用戶：
   ```
   python manage.py createsuperuser
   ```
6. 運行開發服務器：
   ```
   python manage.py runserver
   ```
7. 訪問 http://127.0.0.1:8000/ 瀏覽網站
8. 訪問 http://127.0.0.1:8000/admin/ 進入管理後台

## 項目結構

- `/store` - 主要應用程序
- `/templates` - HTML模板
- `/static` - 靜態文件 (CSS, JS)
- `/media` - 用戶上傳的媒體文件 
