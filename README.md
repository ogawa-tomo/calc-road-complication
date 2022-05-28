## ローカル環境構築

### ビルド（初回のみ）

```
$ docker-compose build
```

### コンテナ立ち上げ

```
$ docker-compose up -d
```

### コンテナに入る

```
$ docker-compose exec python3 bash
```

この環境でコードを実行できる

### Unittest

```
$ pytest -p no:warnings -s
```

### pythonパッケージの追加

```
# pip install [パッケージ]
```

追加したら、requirements.txtを更新しておく

```
# pip freeze > requirements.txt
```

次にコンテナ立ち上げるときはビルドしなおす

## 参考資料

色んな都市の街路の複雑度を比較した記事
https://geoffboeing.com/2018/07/comparing-city-street-orientations/

街路の方向を取得するコード
https://github.com/gboeing/osmnx-examples/blob/v0.11/notebooks/15-calculate-visualize-edge-bearings.ipynb

街路の複雑性を詳細に分析した論文
https://appliednetsci.springeropen.com/articles/10.1007/s41109-019-0189-1