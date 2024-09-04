# light360

## これはなに?
360度カメラで撮影した動画からフレームごとの光源の位置を推定し、球座標を返すツールです。

## つかいかた
OpenCVが必要です。

```sh
$ pip install opencv-python
```

処理したい動画ファイルを次のように指定します。
`-o`オプションを省略すると、JSON形式で標準出力に出力されます。

```sh
$ python3 light360.py -i source.mp4 -o light.json
```

出力されるデータのフォーマットは次の通りです。

- fps: 動画のFPS
- totalFrames: 総フレーム数
- totalDuration: 総再生時間(秒)
- frameInfo: 各フレームの情報
  - frameID: フレームの連番
  - x: 推測された光源のピクセル上のX座標
  - y: 推測された光源のピクセル上のY座標
  - lon: 経度(-180～180)
  - lat: 緯度(-90～90)
  - brightness: 輝度(0～255)

```json
{
  "fps": 30,
  "totalFrames": 734,
  "totalDuration": 24.466666666666665,
  "frameInfo": [
    {
      "frameID": 0,
      "x": 1528,
      "y": 450,
      "lon": -36.75,
      "lat": 47.8125,
      "brightness": 252
    },
    {
      "frameID": 1,
      "x": 1528,
      "y": 450,
      "lon": -36.75,
      "lat": 47.8125,
      "brightness": 252
    }
  ]
}
```

## ライセンス
MIT Licenseです。
