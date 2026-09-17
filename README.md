このコードはアマゾン刊「Raspberry Pi 5でAI」で使用したプログラムを収容しています。

第１章　基礎としてのRaspberry Pi 5 OS

Ⅰ．Raspberry Pi 5について

  １　Raspberry Pi 5
  
  ２．OSのインストール
  
  ３．最初にやっておくこと
  
    １）立ち上げ、シャットダウン                 ２）raspi-configの操作方法
    
    ３）プログラムアップデートとアップグレード    ４）Control Centreの利用
    
    ５）ディスプレイ設定                        ６）SSH接続を可能にする
    
    ７）WiFi設定                               ８）エディターnanoのインストール
    
    ９）画面キャプチャー                        １０）Swapの設定
    
  ４．OSの設定
  
    １）日本語入力の設定方法
    
    ２）ブラウザの利用
    
  ５　リモート接続ツール
  
    １）SSH（Secure Shell）
    
    ２）SCP接続
    
    ３）VNC
    
  ６　Raspberry Pi Connect
  
    １）Raspberry Pi Connect
    
    ２）ホストPC側の接続設定
    
    ３）Raspberry Pi IDを作成する
    
    ４）スマートフォンからリモート操作する
    
Ⅱ． USBカメラ、CSI-Cameraを使用する

  １　GStreamerの利用
  
    １）　GStreamer
    
    ２）　gst-launch-1.0コマンドの使い方
    
    ３）　基本的な動作
    
    ４）　カメラの画像を表示させる
    
  ２　USBカメラ（UVC対応）の利用
  
    １）　使用するUSBカメラの概要
    
    ２）　USBカメラを利用するOSの現状把握
    
    ３）　ドライバーfswebcamのインストール
    
    ４）　V4l2について
    
  ３　USBカメラの画像を表示・キャプチャするアプリ
  
    １）　USBカメラの使用法
    
    ２）　cheese
    
    ３）　Snapshot（スナップショット）
    
    ４）　guvcview
    
    ５）　VNC
    
  ４　CSI-Camera
  
    １）　カメラ概要
    
    ２）　rpicam-apps
    
    ３）　CSI-Cameraの現状把握

    ４）　rpicam-apps のコマンド
    
第２章　Raspberry Pi 5のプログラミングの要素整備

Ⅰ． プログラミングの要素

  １　エディター
  
    １）エディターについて
    
    ２）　エディターGeany
    
  ２　Python環境の整備
  
    １）　Pythonの現状把握
    
    ２）　Thonnyについて
    
    ３）Thonnyの動作確認
    
  ３　OpenCVのインストール
  
    １）OpenCVのインストール
    
  ４　仮想環境とは
  
    １）　システム空間と仮想空間
    
    ２）　venvを使った仮想空間「Kasou」
    
第３章　Raspberry Pi 5でプログラミング

Ⅰ　Raspberry Pi 5でプログラミング

  １　電子工作プログラミング
  
    １）　GPIO端子でBlink
    
    ２）　MPU6050の出力をSSD1306に表示
    
    ３）既知の不具合に対するパッチ適用
    
Ⅱ　VSCでプログラミング

  １　VSCでCPPプログラミング
  
    １）　CPP
    
  ２　VSCのセットアップ
  
  ３　ターミナルでコンパイル・実行する
  
    １）ターミナルでコンパイル・実行する
    
  ４　Blink.cppライブラリを含むプログラミング
  
    １）プログラム概要
    
    ２）プログラムの作成
    
    ３）task.jsonの作成と編集
    
  ５　VSCでPythonプログラミング
  
    １）準備
    
    ２）CPU温度表示プログラム
    
Ⅲ　Pythonプログラミング

  １　OpenCV＋Pythonプログラミング
  
    １）　Pythonを使ってCSIカメラの画像を表示
    
    ２）　Pi Camera のカメラ出力をキャプチャ
    
    ３）　カメラ映像（動画）を表示する
    
    ４）　動画の撮影（保存）
    
    ５）　HDR（HDRモードで表示す
    
    ６）　白黒変換
    
    ７）　二値化処理
    
    ８）　エッジ検出（輪郭抽出）
    
  ２　顔検出プログラミング
  
    １）　顔検出
    
第４章　Raspberry Pi 5でAIプログラミング

Ⅰ　Raspberry PiでEdgeImpulse

  １　Raspberry Pi5でEdgeImpulse
  
    １）　EdgeImpulseとは
    
    ２）　システム要件
    
    ３）　セットアップ（準備）
    
    ４）　仮想環境
    
    ５）　EdgeImpiulseの事前準備
    
    ６）　WEBページEdgeImpulseで行う作業
    
    ７）　画像収集
    
    ８）ラベル付け
    
    ９）学習用、テスト用
    
    １０）「Image」 での作業
    
  ２　インパルスの作成
  
    １）　インパルスの作成
    
    ２）モデルトレーニング
    
  ３　デプロイ
  
    １）　デプロイ
    
  ４　推論実行　画面上に表示させる
  
    １）　推論プログラム「edge-impulse-linux」
    
    ２）　プログラムの変更
    
    ３）　プログラムの実行
    
  ５　Pythonを使った推論の実行
  
    １）　Pythonを使った推論プログラム
    
    ２）　推論プログラム
    
Ⅱ　YOLO v8で物体認識AI

１　YOLO v8で物体認識AI

    １）　YOLO v8
    
    ２）  Raspberry Pi 5にYOLOv8をインストール
    
    ３） YOLO v8の仮想環境へのインストール
    
  ２ 静止画で物体認識
  
  ３ カメラ出力で物体認識
  
添付ファイルの取り扱いについて

あとがき
