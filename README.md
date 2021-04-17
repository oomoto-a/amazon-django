# Amazon Webツール(仮)　Django側
## 環境構築
- 仮想環境作成  
`python -m venv venv` 

- VSCODEのインタープリターに仮想環境のPythonを設定  
venv/Scripts/python.exe　を指定する  
ターミナルを起動して、先頭に(venv)がついていれば成功  

- ライブラリインストール  
プロジェクトルートにて以下を実行  
`pip install -r requirements.txt`

- コンテナの起動(MySQLが使用可能になる)  
あらかじめDockerをインストールしておく    
新しいターミナルを開き、プロジェクトルートにて以下を実行  
`docker-compose up`

DBの管理画面は、以下より参照可能  
http://localhost:10080/index.php


- 開発サーバー起動  
`python manage.py runserver`