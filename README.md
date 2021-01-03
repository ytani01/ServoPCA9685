# Python3 library for I2C Servo Motor Driver PCA9685

サーボモータードライバ PCA9685用 Python3ライブラリ

* PCA9685用
* 複数のサーボを同時に制御できる。


## 動作環境

* 本体: Raspberry Pi
* モータードライバー: PCA9685
* サーボモーター: SG-90 (および互換品)
* プログラミング言語: Python3
* GPIO制御ライブラリ: pigpio

## TL;DR

Install
```bash
$ cd ~
$ python3 -m venv env1
$ cd env1
$ . ./bin/activate

(env1)$ git clone https://github.com/ytani01/ServoPCA9685.git
(env1)$ cd ServoPCA9685

(env1)$ pip install -U pip setuptools wheel
(env1)$ hash -r
(env1)$ pip install .
```

Run [sample.py](sample.py)
```bash
(env1)$ sudo pigpiod
(env1)$ ./sample.py
```


## API

```bash
python3 -m pydoc servoPCA9685
```


## A. 参考

* [pigpio/Examples/Python code](http://abyz.me.uk/rpi/pigpio/examples.html#Python%20code)
