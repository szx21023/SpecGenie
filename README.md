可以使用 --port 參數來指定 uvicorn 的埠號（port）。

範例指令：
```
uvicorn main:app --reload --port 8000
```
說明：
main:app：代表在 main.py 檔案中有一個名為 app 的 FastAPI 應用程式。

--reload：啟用開發模式，自動重新載入程式碼變更。

--port 8000：指定使用的埠號為 8000（預設是 8000）。
